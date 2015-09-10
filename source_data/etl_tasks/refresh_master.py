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

        source_codes = {'indicator' :[k for k,v in json\
            .loads(self.submission_data[0][1]).iteritems()]}

        region_codes, campaign_codes = [],[]

        for ss_id, submission in self.submission_data:

            submission_dict = json.loads(submission)
            region_codes.append(submission_dict[self.db_doc_deets['region_column']])
            campaign_codes.append(submission_dict[self.db_doc_deets['campaign_column']])

        source_codes['region'] = list(set(region_codes))
        source_codes['campaign'] = list(set(campaign_codes))

        source_object_map_ids = self.upsert_source_codes(source_codes)

    def refresh_submission_details(self):

        source_map_dict = self.get_document_meta_mappings()

        ss_id_list, ss_detail_batch = [],[]

        for row in self.submission_data:

            ss_id, submission_dict = row[0],json.loads(row[1])
            region_column, campaign_column = self.db_doc_deets['region_column']\
                , self.db_doc_deets['campaign_column']

            try:
                region_id = source_map_dict[('region'\
                    ,submission_dict[region_column])]
            except KeyError:
                region_id = None

            try:
                campaign_id = source_map_dict[('campaign'\
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

        source_map_dict = self.get_document_meta_mappings()

        submissions_ready_for_sync = []

        ss_ids_in_batch = [ss_id for ss_id, ss_json in self.submission_data]
        ready_for_doc_datapoint_sync = SourceSubmissionDetail.objects\
            .filter(
                 source_submission_id__in= ss_ids_in_batch,
                 region_id__isnull= False,
                 campaign_id__isnull= False
            ).values('region_id','campaign_id','source_submission_id')

        for row in ready_for_doc_datapoint_sync:
            doc_dps = self.process_source_submission(row['region_id'], \
                row['campaign_id'], row['source_submission_id'],source_map_dict)


    ## main() helper methods ##

    def process_source_submission(self,region_id,campaign_id,ss_id,som_dict):

        doc_dp_batch = []
        ## dont make this query.. use self.submission_data ##
        submission  = SourceSubmission.objects.get(id=ss_id)\
            .submission_json
        print submission

        for k,v in submission.iteritems():

            try:
                doc_dp_batch.append(\
                    DocDataPoint(**{
                        'indicator_id':  som_dict[('indicator',k)],
                        'value': v,
                        'region_id': region_id,
                        'campaign_id': campaign_id,
                        'document_id': self.document_id,
                        'source_submission_id': ss_id,
                        'changed_by_id': self.user_id,
                        'is_valid': True,
                        'agg_on_region': True,
                    }))
            except KeyError:
                pass

        DocDataPoint.objects.filter(source_submission_id=ss_id).delete()
        DocDataPoint.objects.bulk_create(doc_dp_batch)


    def upsert_source_codes(self, source_codes):

        som_batch = []
        for content_type, source_code_list in source_codes.iteritems():

            for source_code in source_code_list:
                som_object, created = SourceObjectMap.objects.get_or_create(
                    source_object_code = source_code,
                    content_type = content_type,
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
