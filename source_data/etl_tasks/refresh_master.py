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

        self.new_datapoints = []
        self.document_metadata = {
            ## these are defaults ##
            'agg_regions':True,
            'clean_source_campaigns':True,
            'office_id':1,

        }

        dmd_qs = DocumentDetail.objects.raw('''
            SELECT
                dd.id
                ,ddt.name as k
                ,dd.doc_detail_value as v
            FROM document_detail dd
            INNER JOIN document_detail_type ddt
            ON dd.doc_detail_type_id = ddt.id
            AND dd.document_id = %s;
            ''',[self.document_id])

        for row in dmd_qs:
            self.document_metadata[row.k] = row.v

        map_df_cols = ['master_object_id','source_object_code','content_type']

        sm_ids = DocumentSourceObjectMap.objects.filter(document_id =\
            self.document_id).values_list('source_object_map_id',flat=True)

        self.source_map_dict =  DataFrame(list(SourceObjectMap.objects\
            .filter(
                master_object_id__gt=0,
                id__in = sm_ids).values_list(*['master_object_id']))
            ,columns = ['master_object_id']\
            ,index= SourceObjectMap.objects.filter(master_object_id__gt=0
                ,id__in = sm_ids)\
                .values_list(*['content_type','source_object_code']))\
                .to_dict()['master_object_id']

        self.computed_datapoint_ids = self.main()

    def refresh_doc_meta(self):

        db_doc_deets = DocumentDetail.objects\
            .filter(document_id = self.document_id)\
            .values()

        ss_list = SourceSubmission.objects\
            .filter(document_id = self.document_id)\
            .values_list('id','submission_json')

        first_submission = ss_list[0][0]

        print first_submission


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
