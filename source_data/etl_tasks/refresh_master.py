import traceback

from decimal import InvalidOperation
from pprint import pprint
import json

from django.db import IntegrityError
from django.db import transaction
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from pandas import DataFrame

from source_data.models import *
from datapoints.cache_tasks import CacheRefresh
from datapoints.models import *

class MasterRefresh(object):
    '''
    Take source datapoints from a document_id and upsert into datapoints table
    based on mapping and audits from the doc_review app.
    '''

    def __init__(self,user_id,document_id):

        self.ss_batch_size = 500
        self.document_id = document_id
        self.user_id = user_id

        self.db_doc_deets = self.get_document_config()
        self.source_map_dict = self.get_document_meta_mappings()

        self.submission_data = SourceSubmission.objects\
            .filter(document_id = self.document_id)\
            .values_list('id','submission_json')[:self.ss_batch_size]

    ## __init__ helper methods ##
    def get_document_config(self):

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

        sm_ids = DocumentSourceObjectMap.objects.filter(document_id =\
            self.document_id).values_list('source_object_map_id',flat=True)

        source_map_dict =  DataFrame(list(SourceObjectMap.objects\
            # tuple dict ex: {('region': "PAK") : 3 , ('region': "PAK") : 3}
            .filter(
                master_object_id__gt=0,
                id__in = sm_ids).values_list(*['master_object_id']))
            ,columns = ['master_object_id']\
            ,index= SourceObjectMap.objects.filter(master_object_id__gt=0
                ,id__in = sm_ids)\
                .values_list(*['content_type','source_object_code']))\
                .to_dict()['master_object_id']

        return source_map_dict

    ## main methods .. called by views and APIs in order to move data ##
    def refresh_doc_meta(self):

        ss_list = SourceSubmission.objects\
            .filter(document_id = self.document_id)\
            .values('id','submission_json')

        source_codes = {'indicators' :[k for k,v in json\
            .loads(ss_list[0]['submission_json']).iteritems()]}

        source_object_map_ids = self.upsert_source_codes(source_codes)

    def refresh_submission_details(self):

        ss_id_list, ss_detail_batch = [],[]

        for row in self.submission_data:

            ss_id, submission_dict = row[0],json.loads(row[1])

            region_column, campaign_column = self.db_doc_deets['region_column']\
                , self.db_doc_deets['campaign_column']

            try:
                region_id = self.source_map_dict[('region'\
                    ,submission_dict[region_column])]
            except KeyError:
                region_id = None

            try:
                campaign_id = self.source_map_dict[('campaign'\
                    ,submission_dict[campaign_column])]
            except KeyError:
                campaign_id = None

            ss_id_list.append(ss_id)
            ss_detail_batch.append(SourceSubmissionDetail(**{
                'document_id': self.document_id,
                'source_submission_id': ss_id,
                'region_code':submission_dict[region_column],
                'campaign_code':submission_dict[campaign_column],
                'region_id': region_id,
                'campaign_id': campaign_id,
            }))

        SourceSubmissionDetail.objects.filter(id__in=ss_id_list).delete()
        SourceSubmissionDetail.objects.bulk_create(ss_detail_batch)

    def submissions_to_doc_datapoints(self):

        print 'submissions_to_doc_datapoints\n' * 3

        submissions_ready_for_sync = []

        ss_ids_in_batch = [ss_id for ss_id, ss_json in self.submission_data]
        ready_for_doc_datapoint_sync = SourceSubmissionDetail.objects\
            .filter(
                 source_submission_id__in= ss_ids_in_batch,
                region_id__isnull= False,
                campaign_id__isnull= False
            ).values('region_id','campaign_id','source_submission_id')

        print 'LEN OF QS: %s' % len(ss_ids_in_batch)

        for row in ready_for_doc_datapoint_sync:
            print '==ST HEAVEN==\n' * 3
            print row


    ## main() helper methods ##

    def upsert_source_codes(self, source_codes):

        som_batch = []
        for source_code in source_codes['indicators']:
            som_object, created = SourceObjectMap.objects.get_or_create(
                source_object_code = source_code,
                content_type = 'indicator',
                defaults = {
                     'master_object_id' : -1,
                     'master_object_name': 'To Map!',
                     'mapped_by_id' : self.user_id
                }
            )

            doc_som_object = DocumentSourceObjectMap(**{
                'source_object_map_id': som_object.id,
                'document_id': self.document_id
            })
            #
            som_batch.append(doc_som_object)

        DocumentSourceObjectMap.objects\
            .filter(document_id = self.document_id)\
            .delete()

        DocumentSourceObjectMap.objects.bulk_create(som_batch)


    def main(self):
        '''
        from source_data.etl_tasks.refresh_master import MasterRefresh as mr
        x = mr(1,2)
        '''

        new_source_submission_ids = SourceSubmission.objects.filter(
            document_id = self.document_id
            ,process_status = 'TO_PROCESS'
        ).values_list('id',flat=True)

        to_process = new_source_submission_ids[:self.ss_batch_size]

        print '== source_submissions =='
        SourceSubmission.objects.filter(id__in=to_process)\
            .update(process_status = 'PROCESSED')

        ## john test the above ... ##

        print '== doc datapoints =='
        doc_datapoint_ids = self.process_doc_datapoints\
            (to_process)

        print '== sync datapoints =='
        datapoint_ids = self.sync_doc_datapoint()

        return datapoint_ids

    def process_doc_datapoints(self,source_submission_id_list):

        source_dp_json = SourceSubmission.objects.filter(
            id__in = source_submission_id_list).values()

        for i,(row) in enumerate(source_dp_json):
            self.process_source_submission(row)

        new_doc_dp_ids = DocDataPoint.objects.filter(document_id = \
            self.document_id).values_list('id',flat=True)

        return new_doc_dp_ids

    def sync_doc_datapoint(self):
        ## merge into datapoints from doc datapoints #

        new_dps = []
        # DataPoint.objects.raw('''
        #     SELECT * FROM fn_upsert_source_dps(%s,%s)
        # ''',[self.user_id, self.document_id])

        new_dp_ids = [dp.id for dp in new_dps]

        return DataPoint.objects.filter(id__in=new_dp_ids)

    def process_source_submission(self,ss_row):

        submission_data = json.loads(ss_row['submission_json'])
        region_code = submission_data[self.db_doc_deets['region_column']]
        campaign_code = submission_data[self.db_doc_deets['campaign_column']]

        dp_batch = []

        try:
            region_id = self.source_map_dict[('region',region_code)]
        except KeyError:
            return

        try:
            campaign_id = self.source_map_dict[('campaign',campaign_code)]
        except KeyError:
            return

        for k,v in submission_data.iteritems():

            dp_obj = self.process_submission_instance(region_id,campaign_id,k,v,ss_row['id'])

            if dp_obj:
                dp_batch.append(dp_obj)

        batch_result = DocDataPoint.objects.bulk_create(dp_batch)

    def process_submission_instance(self,region_id,campaign_id,ind_code,val,ss_id):

        try:
            indicator_id = self.source_map_dict[('indicator',ind_code)]
        except KeyError:
            return None

        try:
            cleaned_val = float(val)
        except ValueError:
            return

        doc_dp_obj = DocDataPoint(**{
            'document_id':self.document_id,
            'region_id':region_id,
            'campaign_id':campaign_id,
            'indicator_id':indicator_id,
            'value':val,
            'changed_by_id':self.user_id,
            'source_submission_id':ss_id,
            'is_valid':True, ## TODO # make this based off user input
            'agg_on_region':True
        })

        return doc_dp_obj


    def clean_cell_value(self,cell_value):

        if cell_value == None:
            return None

        try:
            cleaned = float(cell_value.replace(',',''))
        except ValueError:
            cleaned = None

        return cleaned

    def delete_un_mapped(self):

        datapoint_ids = MissingMapping.objects.filter(document_id=\
            self.document_id).values_list('datapoint_id',flat=True)

        MissingMapping.objects.filter(document_id=self.document_id).delete()

        DataPoint.objects.filter(id__in=datapoint_ids).delete()
