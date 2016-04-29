import locale
from django.utils import timezone

from collections import defaultdict
import json
import re
from pandas import DataFrame, concat, notnull
from bulk_update.helper import bulk_update
import math
from rhizome.models import *

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
        self.class_map_dict = self.get_class_indicator_mappings()
        self.file_header = Document.objects.get(id=self.document_id).file_header

        # self.to_process_ss_ids = SourceSubmission.objects\
        #         .filter(document_id = self.document_id,\
        #             process_status='TO_PROCESS')

        # self.location_codes_to_process = SourceSubmission\
        #     .objects.filter(id__in = self.to_process_ss_ids)\
        #     .values_list('location_code',flat = True).distinct()\
        #     [:self.ss_location_code_batch_size]

        # self.ss_ids_to_process, self.all_ss_ids =\
        #     self.refresh_submission_details()
        #
        # self.submission_data = dict(SourceSubmission.objects.filter(id__in = \
        #     self.ss_ids_to_process).values_list('id','submission_json'))

    ## __init__ HELPER METHOD ##

    def get_document_config(self):
        '''
        When ingesting a file the user must set the following configurtions:
            - unique_id_column
            - location_code_column
            - data_date
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

        # sm_ids = DocumentSourceObjectMap.objects.filter(document_id =\
        #     self.document_id).values_list('source_object_map_id',flat=True)

        # create a tuple dict ex: {('location': "PAK") : 3 , ('location': "PAK") : 3}
        source_map_dict =  DataFrame(list(SourceObjectMap.objects\
            .filter(
                master_object_id__gt=0)\
                # id__in = sm_ids)\
            .values_list(*['master_object_id']))
            ,columns = ['master_object_id']\
            ,index= SourceObjectMap.objects.filter(master_object_id__gt=0)
                # ,id__in = sm_ids)\
                .values_list(*['content_type','source_object_code']))\


        source_map_dict = source_map_dict.to_dict()['master_object_id']

        return source_map_dict

    def get_class_indicator_mappings(self):
        '''
        Using the meta mappings, map indicator ids to another dict, which maps all
        of the class indicator string values to their corresponding enum values.
        '''

        indicator_ids = self.source_map_dict.values()
        query_results = IndicatorClassMap.objects.filter(
            indicator_id__in = indicator_ids).values_list('indicator', 'string_value', 'enum_value')
        class_map_dict ={}

        for query in query_results:
            if query[0] not in class_map_dict:
                class_map_dict[query[0]] = {}
            class_map_dict[query[0]][query[1]] = query[2]

        return class_map_dict

    def main(self):

        # if len(self.ss_ids_to_process) == 0:
        #     return

        self.refresh_submission_details()
        self.submissions_to_doc_datapoints()
        self.delete_unmapped()
        self.sync_datapoint()

    def delete_unmapped(self):
        ## if a user re-maps data, we need to delete the
        ## old data and make way for the new

        som_data = SourceObjectMap.objects.filter(master_object_id__gt = 0,
            id__in = DocumentSourceObjectMap.objects\
                .filter(document_id = self.document_id)\
                .values_list('source_object_map_id',flat=True))\
                .values_list('content_type','master_object_id')

        som_lookup = defaultdict(list)

        for content_type,master_object_id in som_data:
            som_lookup[content_type].append(master_object_id)

        ## delete bad_indicator_data ##
        DataPoint.objects.filter(
            source_submission_id__document_id = self.document_id,
        ).exclude(indicator_id__in=som_lookup['indicator']).delete()

        ## delete bad_location_data ##
        DataPoint.objects.filter(
            source_submission_id__document_id = self.document_id,
        ).exclude(location_id__in=som_lookup['location']).delete()

        ## delete bad_campaign_data ##
        DataPoint.objects.filter(
            source_submission_id__document_id = self.document_id,
        ).exclude(location_id__in=som_lookup['campaign']).delete()


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

        ## find soure_submission_ids based of location_codes to process
        ## then get the json of all of the related submissions .
        submission_qs = SourceSubmission.objects\
            .filter(document_id = self.document_id)

        for submission in submission_qs:
            all_ss_ids.append(submission.id)

            location_id = submission.get_location_id()
            campaign_id = submission.get_campaign_id()

            if location_id > 0:
                ss_id_list_to_process.append(submission.id)
                submission.location_id = location_id
                submission.campaign_id = campaign_id

        if len(submission_qs) > 0:
            bulk_update(submission_qs)

        return ss_id_list_to_process,all_ss_ids

    def submissions_to_doc_datapoints(self):
        '''
        Send all rows queued for processing to the process_source_submission method.
        '''

        # ss_ids_in_batch = self.submission_data.keys()

        for row in SourceSubmission.objects.filter(document_id = self.document_id):

            row.location_id = row.get_location_id()
            row.campaign_id = row.get_campaign_id()
            ## if no mapping for campaign / location -- dont process
            if row.campaign_id == -1:
                row.process_status = 'missing campaign'
            elif row.location_id == -1:
                row.process_status = 'missing location'
            else:
                doc_dps = self.process_source_submission(row)

    def sync_datapoint(self, ss_id_list = None):
        #  python manage.py test rhizome.tests.test_transform_upload.TransformUploadTestCase --settings=rhizome.settings.test
        dp_batch = []
        if not ss_id_list:
            ss_id_list = SourceSubmission.objects\
                .filter(document_id = self.document_id).values_list('id',flat=True)

        doc_dp_df = DataFrame(list(DocDataPoint.objects.filter(
            document_id = self.document_id).values()))

        if len(doc_dp_df) == 0:
            return

        location_ids = doc_dp_df['location_id'].unique()
        indicator_ids = doc_dp_df['indicator_id'].unique()
        campaign_ids = doc_dp_df['campaign_id'].unique()

        # min_date, max_date = doc_dp_df['data_date'].min(),\
        #     doc_dp_df['data_date'].max()

        pontential_conflict_doc_dp_df = DataFrame(list(DocDataPoint\
            .objects.filter(
                indicator_id__in = indicator_ids,
                location_id__in = location_ids,
                campaign_id__in = campaign_ids
                # data_date__gte = min_date,
                # data_date__lte = max_date,
            ).values()))

        full_dp_df = concat([doc_dp_df,pontential_conflict_doc_dp_df])
        dp_df = full_dp_df.drop_duplicates()

        ss_columns = ['id','created_at']
        ss_dp_df = DataFrame(list(SourceSubmission.objects.filter(
            id__in = ss_id_list).values(*ss_columns)),columns=ss_columns)

        merged_df = dp_df.merge(ss_dp_df, left_on = 'source_submission_id', \
            right_on = 'id')

        ready_for_sync_tuple_dict = DataFrame(merged_df\
            .groupby(['location_id', 'indicator_id']).max())['created_at'].to_dict()

        dp_batch, dp_ids_to_delete = [],[]

        merged_df = merged_df.where((notnull(merged_df)), None)

        for ix, row in merged_df.iterrows():
            max_created_at = ready_for_sync_tuple_dict[(row.location_id, \
                row.indicator_id)]

            row_created_at = row.created_at.replace(tzinfo=None)


            if row_created_at == max_created_at or row.campaign_id is None:
                dp_batch.append(DataPoint(**{
                    'indicator_id' : row.indicator_id,
                    'location_id' : row.location_id,
                    'campaign_id' : row.campaign_id,
                    'data_date' : row.data_date,
                    'value' : row.value,
                    'source_submission_id' : row.source_submission_id,
                }))

            else:
                dp_ids_to_delete.append(row.id_x)

        DataPoint.objects.filter(id__in = dp_ids_to_delete).delete()
        DataPoint.objects.bulk_create(dp_batch)


    def process_source_submission(self,row):
        doc_dp_batch = []
        submission  = row.submission_json

        for k,v in submission.iteritems():
            doc_dp = self.source_submission_cell_to_doc_datapoint(row, k, v, \
                row.data_date)
            if doc_dp:
                doc_dp_batch.append(doc_dp)
        DocDataPoint.objects.filter(source_submission_id=row.id).delete()
        DocDataPoint.objects.bulk_create(doc_dp_batch)

    def source_submission_cell_to_doc_datapoint(self, row, indicator_string, \
            value, data_date):
        '''
        This method prepares a batch insert into docdatapoint by creating a list of
        DocDataPoint objects.  The Database handles all docdatapoitns in a submission
        row at once in process_source_submission.
        '''
        ## if no indicator row dont process ##
        try:
            indicator_id = self.source_map_dict[('indicator',indicator_string)]
        except KeyError:
            'can\'t find indicator!'
            return None

        cleaned_val = None
        #handle string 'class' type indicators
        if indicator_id in self.class_map_dict:
            try:
                cleaned_val = self.class_map_dict[indicator_id][value]
            except KeyError:
                return None
        #handle numbers
        else:
            try:
                cleaned_val = self.clean_val(value)
            except ValueError:
                return None

        if cleaned_val:
            doc_dp = DocDataPoint(**{
                'indicator_id':  indicator_id,
                'value': cleaned_val,
                'location_id': row.location_id,
                'campaign_id': row.campaign_id,
                'data_date': data_date,
                'document_id': self.document_id,
                'source_submission_id': row.id,
                'agg_on_location': True,
            })
            return doc_dp
        else:
            return None

    def clean_val(self, val):
        '''
        This needs alot of work but basically determines if a particular submission
        cell is alllowed.
        Big point of future controversy... what do we do with zero values?  In order to
        keep the size of the database manageable, we only accept non zero values.
        '''
        str_lookup = {'yes':1,'no':0}
        if val is None:
            return None

        #deal with percentages
        convert_percent = False
        if type(val) == unicode and '%' in val:
            try:
                val = float(re.sub('%','', val))
                convert_percent =True
            except ValueError:
                pass
        ## clean!  i am on a deadline rn :-/  ##

        locale.setlocale( locale.LC_ALL, 'en_US.UTF-8' )

        try:
            cleaned_val = locale.atoi(val) # 100,000 -> 100000.oo
        except AttributeError:
            cleaned_val = float(val)
        except ValueError:
            try:
                cleaned_val = float(val)
            except ValueError:
                try:
                    cleaned_val = str_lookup[val.lower()]
                except KeyError:
                    raise ValueError('Bad Value!')

        if convert_percent:
            cleaned_val = cleaned_val/100.0
        return cleaned_val
