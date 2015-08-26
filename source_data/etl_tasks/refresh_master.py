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
    Take source datapoints from a document_id and upsert into datapoitns table
    based on mapping and audits from the doc_review app.
    '''

    def __init__(self,user_id,document_id):

        self.document_id = document_id
        self.user_id = user_id

        self.new_datapoints = []
        self.document_metadata = {
            'instance_guid':'uq_id',
            'file_type':'columns_are_indicators',
            'region_column':'Wardcode',
            'campaign_column':'Campaign',
            'agg_regions':True
        }

        map_df_cols = ['master_object_id','source_object_code','content_type']

        self.source_map_dict =  DataFrame(list(SourceObjectMap.objects.filter(master_object_id__gt=0)\
            .values_list(*['master_object_id']))\
            ,columns = ['master_object_id']\
            ,index= SourceObjectMap.objects.filter(master_object_id__gt=0)\
            .values_list(*['content_type','source_object_code']))\
            .to_dict()['master_object_id']

        self.computed_datapoint_ids = self.main()

    def main(self):
        '''
        from source_data.etl_tasks.refresh_master import MasterRefresh as mr
        x = mr(1,3)
        '''

        BATCH_SIZE = 25

        new_source_submission_ids = SourceSubmission.objects.filter(
            document_id = self.document_id
            ,process_status = 'TO_PROCESS'
        ).values_list('id',flat=True)

        to_process = new_source_submission_ids[:BATCH_SIZE]

        print '=== mapping === '
        source_object_map_ids = self.upsert_source_object_map\
            (to_process)

        print '== source_submissions =='
        SourceSubmission.objects.filter(id__in=to_process)\
            .update(process_status = 'PROCESSED')

        print '== doc datapoints =='
        doc_datapoint_ids = self.process_doc_datapoints\
            (to_process)

        print '== sync datapoints =='
        datapoint_ids = self.sync_doc_datapoint()

        print '== cache datapoints =='
        cr = CacheRefresh([d.id for d in datapoint_ids])
        computed_datapoint_ids = cr.main()

        return datapoint_ids

    def upsert_source_object_map(self,source_submission_id_list):
        '''
        TODO: save the source_strings so i dont have to iterate through
        the source_submission json.

        endpoint: api/v2/doc_mapping/?document=66
        '''

        source_dp_json = SourceSubmission.objects.filter(
            id__in = source_submission_id_list).values_list('submission_json')

        if len(source_dp_json) == 0:
            return

        all_codes = [('indicator',k) for k,v in json.loads(source_dp_json[0][0]).iteritems()]
        rg_codes, cp_codes = [],[]

        for row in source_dp_json:
            row_dict = json.loads(row[0])
            rg_codes.append(row_dict[self.document_metadata['region_column']])
            cp_codes.append(row_dict[self.document_metadata['campaign_column']])

        for r in list(set(rg_codes)):
            all_codes.append(('region',r))

        for c in list(set(cp_codes)):
            all_codes.append(('campaign',c))

        for content_type, source_object_code in all_codes:
            self.source_submission_meta_upsert(content_type, source_object_code)


    def source_submission_meta_upsert(self, content_type, source_object_code):
        '''
        Create new metadata if not exists
        Add a record tying this document to the newly inserted metadata
        '''

        sm_obj, created = SourceObjectMap.objects.get_or_create(\
            content_type = content_type\
           ,source_object_code = source_object_code\
           ,defaults = {
            'master_object_id':-1,
            'mapped_by_id':self.user_id
            })

        sm_obj, created = DocumentSourceObjectMap.objects.get_or_create\
            (document_id = self.document_id,source_object_map_id = sm_obj.id)

        return sm_obj.id


    def process_doc_datapoints(self,source_submission_id_list):

        source_dp_json = SourceSubmission.objects.filter(
            id__in = source_submission_id_list).values()

        for i,(row) in enumerate(source_dp_json):
            self.process_source_submission(row)

        new_doc_dp_ids = DocDataPoint.objects.filter(document_id = \
            self.document_id).values_list('id',flat=True)

        return new_doc_dp_ids

    def sync_doc_datapoint(self):
        ## merge into datapoitns from doc datapoints #

        new_dps = DataPoint.objects.raw('''
            SELECT * FROM fn_upsert_source_dps(%s,%s)
        ''',[self.user_id, self.document_id])

        new_dp_ids = [dp.id for dp in new_dps]

        return DataPoint.objects.filter(id__in=new_dp_ids)

    def process_source_submission(self,ss_row):

        submission_data = json.loads(ss_row['submission_json'])
        region_code = submission_data[self.document_metadata['region_column']]
        campaign_code = submission_data[self.document_metadata['campaign_column']]

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
