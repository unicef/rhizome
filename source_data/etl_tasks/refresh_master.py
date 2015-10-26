import traceback
import locale

from decimal import InvalidOperation
from pprint import pprint
import json


from django.db import IntegrityError
from django.db import transaction
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from pandas import DataFrame
from bulk_update.helper import bulk_update

from source_data.models import *
from datapoints.cache_tasks import CacheRefresh
from datapoints.models import *

class MasterRefresh(object):
    '''
    Take source datapoints from a document_id and upsert into datapoints table
    based on mapping and audits from the doc_review app.
    '''

    def __init__(self,user_id,document_id):
        '''
        Batches run based on locations becasue some configurations low for regional
        aggregation and for that reaso, all locations within a document must be processed
        in the same batch.
        In order to grab the batch of data to process, we first find all of the location
        codes that have not been proessed yet, and take onlyt the first 'n' values.
        We then query submissions with this list of location_ids and create the
        self.submission_data variable with these list of ids.
        '''

        self.ss_location_code_batch_size = 50
        self.document_id = document_id
        self.user_id = user_id

        self.db_doc_deets = self.get_document_config()
        self.source_map_dict = self.get_document_meta_mappings()

        self.to_process_ss_ids = SourceSubmission.objects\
                .filter(document_id = self.document_id,\
                    process_status='TO_PROCESS')

        self.location_codes_to_process = list(set(SourceSubmission\
            .objects.filter(id__in = self.to_process_ss_ids)\
            .values_list('location_code',flat = True)))\
            [:self.ss_location_code_batch_size]

        self.campaign_codes_to_process = list(set(SourceSubmission.objects\
            .filter(document_id = self.document_id)\
            .values_list('campaign_code',flat = True)))

        self.file_header = Document.objects.get(id=self.document_id).file_header

        self.ss_ids_to_process, self.all_ss_ids =\
            self.refresh_submission_details()

        self.submission_data = dict(SourceSubmission.objects.filter(id__in = \
            self.ss_ids_to_process).values_list('id','submission_json'))

    ## __init__ HELPER METHOD ##

    def get_document_config(self):
        '''
        When ingesting a file the user must set the following configurtions:
            - unique_id_column
            - location_code_column
            - campaign_code_column
        The user can in addition add a number of optional configurations in order to both
        set up ingestion ( ex. odk_form_name, odk_host ) as well as enhance reporting
        of the data ( photo_column, uploaded_by_column, lat_column, lon_column )
        When the MasterRefresh object is intialized this method is called which queries
        the table containing these configurations and makes it available for use within
        this module.
        '''

        detail_types, document_details = {}, {}
        ddt_qs = DocDetailType.objects.all().values()

        for row in ddt_qs:
            detail_types[row['id']] = row['name']

        dd_qs = DocumentDetail.objects\
            .filter(document_id = self.document_id)\
            .values()

        for row in dd_qs:
            document_details[detail_types[row['doc_detail_type_id']]] =\
                row['doc_detail_value']

        return document_details

    def get_document_meta_mappings(self):
        '''
        Depending on the configuration of the required location and campagin column,
        query the source object map table and find the equivelant master_object_id_ids
        needed to go through the remainder of the ETL process.
        '''

        ## during the DocTransform process we associate new AND existing mappings between
        ## the metadata assoicated with this doucment.
        sm_ids = DocumentSourceObjectMap.objects.filter(document_id =\
            self.document_id).values_list('source_object_map_id',flat=True)

        # create a tuple dict ex: {('location': "PAK") : 3 , ('location': "PAK") : 3}
        source_map_dict =  DataFrame(list(SourceObjectMap.objects\
            .filter(
                master_object_id__gt=0,
                id__in = sm_ids).values_list(*['master_object_id']))
            ,columns = ['master_object_id']\
            ,index= SourceObjectMap.objects.filter(master_object_id__gt=0
                ,id__in = sm_ids)\
                .values_list(*['content_type','source_object_code']))\
                .to_dict()['master_object_id']

        return source_map_dict

    def main(self):

        self.refresh_submission_details()
        self.submissions_to_doc_datapoints()
        self.sync_datapoint()

        SourceSubmission.objects.filter(id__in=self.all_ss_ids)\
            .update(process_status = 'PROCESSED')

    ## MAIN METHODS ##

    def refresh_doc_meta(self):
        '''
        Based on mappings set the location and campaign id for an associated row.  If
        there is not a mapping for both then we know we do not have to process those rows.
        For instance if we have 100 rows in a csv and only 3 rows have both locatino and
        campaign mapped, then we can save 97 iterations through the associated json
        '''

        ## indicators available for mappings are all colum headers that havent been
        ## selected as a document config .. that is 'uq_ix' is not an indicator to map
        indicator_codes =  set([h for h in self.file_header]).difference(set(\
            [v for k,v in self.db_doc_deets.iteritems()]))

        source_codes = {
            'indicator': indicator_codes,
            'location': self.location_codes_to_process,
            'campaign': self.campaign_codes_to_process
        }

        source_object_map_ids = self.upsert_source_codes(source_codes)

    def upsert_source_codes(self, source_codes):
        '''
        From the above metadata items, create any new mappings as well as assign all
        this document_id a reference to mappings that have been created from other
        documents.
        '''

        som_batch = []
        for content_type, source_code_list in source_codes.iteritems():

            for source_code in list(set(source_code_list)):
                som_object, created = SourceObjectMap.objects.get_or_create(
                    source_object_code = source_code,
                    content_type = content_type,
                    defaults = {
                         'master_object_id' : -1,
                         'master_object_name': 'To Map!',
                         'mapped_by_id' : self.user_id
                    }
                )
                som_batch.append(DocumentSourceObjectMap(**{
                        'source_object_map_id': som_object.id,
                        'document_id': self.document_id
                    }))

        DocumentSourceObjectMap.objects\
            .filter(document_id = self.document_id)\
            .delete()

        DocumentSourceObjectMap.objects.bulk_create(som_batch)

    def refresh_submission_details(self):
        '''
        Based on new and existing mappings, upsert the cooresponding master_object_id_ids
        and determine which rows are ready to process.. since we need a master_location
        and a master_campaign in order to have a successful submission this method helps
        us filter the data that we need to process.
        Would like to be more careful here about what i delete as most things wont be
        touched when it comes to this re-processing, and thus the delete and re-insert
        will be for not.. however the benefit is that it's a clean upsert.. dont have to
        worry about old data that should have been blown away hanging around.
        '''

        ss_id_list_to_process, all_ss_ids = [],[]

        ## find soure_submission_ids based of location_codes to process then get the json
        ## of all of the related submissions .
        submission_qs = SourceSubmission.objects\
            .filter(document_id = self.document_id,
                location_code__in = self.location_codes_to_process,
                process_status = 'TO_PROCESS')

        for submission in submission_qs:
            all_ss_ids.append(submission.id)

            submission_dict = submission.submission_json

            location_column, campaign_column = str(self\
                .db_doc_deets['location_column'])\
                , str(self.db_doc_deets['campaign_column'])

            location_id = self.source_map_dict.get(('location'\
                    ,unicode(submission_dict[location_column])),None)

            campaign_id = self.source_map_dict.get(('campaign'\
                    ,unicode(submission_dict[campaign_column])),None)

            if location_id and campaign_id:

                ss_id_list_to_process.append(submission.id)
                location_code = submission_dict[location_column]
                campaign_code = submission_dict[campaign_column]
                location_id = location_id
                campaign_id =  campaign_id

        bulk_update(submission_qs)

        return ss_id_list_to_process,all_ss_ids

    def submissions_to_doc_datapoints(self):
        '''
        Send all rows queued for processing to the process_source_submission method.
        '''

        ss_ids_in_batch = self.submission_data.keys()

        for row in SourceSubmission.objects.filter(\
                 id__in = ss_ids_in_batch)\
            .values('location_id','campaign_id','source_submission_id'):

            doc_dps = self.process_source_submission(row)

    def sync_datapoint(self):

        dp_batch = []
        ss_id_list = self.submission_data.keys()

        dps = DataPoint.objects.raw('''
            DROP TABLE IF EXISTS _tmp_dp;
            CREATE TABLE _tmp_dp
            AS
            SELECT
                  MAX(id) as id
                , location_id
                , indicator_id
                , campaign_id
                , MAX(source_submission_id) as source_submission_id
                , SUM(value) as value
            FROM doc_datapoint dd
            WHERE source_submission_id = ANY(%s)
            AND is_valid = 't'
            GROUP BY location_id, indicator_id, campaign_id;

            DELETE FROM datapoint d
            USING _tmp_dp t
            WHERE d.location_id = t.location_id
            AND d.campaign_id = t.campaign_id
            AND d.indicator_id = t.indicator_id;

            INSERT INTO datapoint
            (location_id, campaign_id, indicator_id, value, cache_job_id, source_submission_id, created_at, changed_by_id)
            SELECT location_id, campaign_id, indicator_id, value, -1, source_submission_id, now(), %s
            FROM  _tmp_dp;

            SELECT d.id FROM datapoint d
            INNER JOIN _tmp_dp t
            ON d.location_id = t.location_id
            AND d.campaign_id = t.campaign_id
            AND d.indicator_id = t.indicator_id
            LIMIT 1;
        ''',[ss_id_list,self.user_id])

        for dp in dps:
            print dp.id


    ## main() helper methods ##
    def process_source_submission(self,row):

        location_id,campaign_id,ss_id = row['location_id'],row['campaign_id'],\
            row['source_submission_id']

        doc_dp_batch = []
        submission  = json.loads(self.submission_data[ss_id])

        for k,v in submission.iteritems():
            doc_dp = self.source_submission_row_to_doc_datapoints(k,v,location_id,\
                campaign_id,ss_id)
            if doc_dp:
                doc_dp_batch.append(doc_dp)

        DocDataPoint.objects.filter(source_submission_id=ss_id).delete()
        DocDataPoint.objects.bulk_create(doc_dp_batch)

    def source_submission_row_to_doc_datapoints(self, ind_str, val, location_id, \
        campaign_id, ss_id):
        '''
        This method prepares a batch insert into docdatapoint by creating a list of
        DocDataPoint objects.  The Database handles all docdatapoitns in a submission
        row at once in process_source_submission.
        '''

        try:
            cleaned_val = self.clean_val(val)
        except ValueError:
            return None

        try:
            indicator_id = self.source_map_dict[('indicator',ind_str)]
        except KeyError:
            return None

        doc_dp = DocDataPoint(**{
                'indicator_id':  indicator_id,
                'value': cleaned_val,
                'location_id': location_id,
                'campaign_id': campaign_id,
                'document_id': self.document_id,
                'source_submission_id': ss_id,
                'changed_by_id': self.user_id,
                'is_valid': True,
                'agg_on_location': True,
            })

        return doc_dp


    def clean_val(self, val):
        '''
        This needs alot of work but basically determines if a particular submission
        cell is alllowed.
        Big point of future controversy... what do we do with zero values?  In order to
        keep the size of the database manageable, we only accept non zero values.
        '''

        if val is None:
            return None

        locale.setlocale( locale.LC_ALL, 'en_US.UTF-8' )

        try:
            cleaned_val = locale.atoi(val) # 100,000 -> 100000.oo
        except AttributeError:
            cleaned_val = float(val)
        except ValueError:
            raise ValueError(' can not convert to float')

        if cleaned_val == float(0):
            raise ValueError('No Zeros Allowed in Doc Data Point')

        return cleaned_val
