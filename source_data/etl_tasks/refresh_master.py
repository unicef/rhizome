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

        self.submission_data = dict(SourceSubmission.objects\
            .filter(\
                document_id = self.document_id,
                process_status = 'TO_PROCESS')\
            .values_list('id','submission_json')[:self.ss_batch_size])

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

    def refresh_doc_meta(self):

        first_submission = json.loads(self.submission_data.values()[0])

        source_codes, region_codes, campaign_codes = \
            {'indicator' :first_submission.keys()}, [], []

        for ss_id, submission in self.submission_data.iteritems():

            submission_dict = json.loads(submission)
            region_codes\
                .append(submission_dict[self.db_doc_deets['region_column']])
            campaign_codes\
                .append(submission_dict[self.db_doc_deets['campaign_column']])

        source_codes['region'] = list(set(region_codes))
        source_codes['campaign'] = list(set(campaign_codes))

        source_object_map_ids = self.upsert_source_codes(source_codes)

    def refresh_submission_details(self):

        source_map_dict = self.get_document_meta_mappings()

        ss_id_list, ss_detail_batch = [],[]

        for ss_id, submission_json in self.submission_data.iteritems():

            submission_dict = json.loads(submission_json)
            region_column, campaign_column = self.db_doc_deets['region_column']\
                , self.db_doc_deets['campaign_column']

            region_id = source_map_dict.get(('location'\
                    ,submission_dict[region_column]),None)

            result_structure_id = source_map_dict.get(('result_structure'\
                    ,submission_dict[campaign_column]),None)

            ss_id_list.append(ss_id)
            ss_detail_batch.append(SourceSubmissionDetail(**{
                'document_id': self.document_id,
                'source_submission_id': ss_id,
                'region_code':submission_dict[region_column],
                'campaign_code':submission_dict[campaign_column],
                'location_id': region_id,
                'result_structure_id': campaign_id,
            }))

        SourceSubmissionDetail.objects.filter(id__in=ss_id_list).delete()
        SourceSubmissionDetail.objects.bulk_create(ss_detail_batch)

    def submissions_to_doc_datapoints(self):

        source_map_dict = self.get_document_meta_mappings()

        submissions_ready_for_sync = []

        ss_ids_in_batch = self.submission_data.keys()
        ready_for_doc_datapoint_sync = SourceSubmissionDetail.objects\
            .filter(
                 source_submission_id__in= ss_ids_in_batch,
                 region_id__isnull= False,
                 campaign_id__isnull= False
            ).values('region_id','campaign_id','source_submission_id')

        for row in ready_for_doc_datapoint_sync:
            doc_dps = self.process_source_submission(row['region_id'], \
                row['campaign_id'], row['source_submission_id'],source_map_dict)

        ## update these submissions to processed ##
        SourceSubmission.objects.filter(id__in=ss_ids_in_batch)\
            .update(process_status = 'PROCEESED')


    def sync_datapoint(self):

        dp_batch = []
        ss_id_list = self.submission_data.keys()

        doc_dps = DocDataPoint.objects.raw('''
                SELECT
                      MAX(id) as id
                    , region_id
                    , indicator_id
                    , campaign_id
                    , MAX(source_submission_id) as source_submission_id
                    , SUM(value) as value
                FROM doc_datapoint dd
                WHERE source_submission_id = ANY(%s)
                AND is_valid = 't'
                GROUP BY region_id, indicator_id, campaign_id;
            ''',[ss_id_list])

        for ddp in doc_dps:
            ddp_dict = dict(ddp.__dict__)
            del ddp_dict['_state']
            ddp_dict['cache_job_id'] = -1
            ddp_dict['changed_by_id'] = self.user_id
            dp_batch.append(DataPoint(**ddp_dict))

        DataPoint.objects.filter(source_submission_id__in = ss_id_list).delete()
        DataPoint.objects.bulk_create(dp_batch)

        pass

    ## main() helper methods ##
    def process_source_submission(self,region_id,campaign_id,ss_id,som_dict):

        doc_dp_batch = []

        submission  = json.loads(self.submission_data[ss_id])

        for k,v in submission.iteritems():
            doc_dp = self.process_submission_datapoint(k,v,region_id,\
                campaign_id,ss_id,som_dict)
            if doc_dp:
                doc_dp_batch.append(doc_dp)

        DocDataPoint.objects.filter(source_submission_id=ss_id).delete()
        DocDataPoint.objects.bulk_create(doc_dp_batch)


    def process_submission_datapoint(self, ind_str, val, region_id, \
        campaign_id, ss_id, som_dict): ## FIXME use kwargs..

            try:
                cleaned_val = self.clean_val(val)
            except ValueError:
                return None

            try:
                indicator_id = som_dict[('indicator',ind_str)]
            except KeyError:
                return None

            try:
                doc_dp = DocDataPoint(**{
                        'indicator_id':  indicator_id,
                        'value': cleaned_val,
                        'region_id': region_id,
                        'campaign_id': campaign_id,
                        'document_id': self.document_id,
                        'source_submission_id': ss_id,
                        'changed_by_id': self.user_id,
                        'is_valid': True,
                        'agg_on_region': True,
                    })
            except KeyError:
                return None

            return doc_dp


    def clean_val(self, val):

        try:
            cleaned_val = float(val)
        except ValueError:
            raise ValueError(' can not convert to float')

        if cleaned_val == float(0):
            raise ValueError('No Zeros Allowed in Doc Data Point')

        return cleaned_val



    def upsert_source_codes(self, source_codes):

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
