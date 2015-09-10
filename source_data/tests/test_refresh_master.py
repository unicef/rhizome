import hashlib
import random
import json

from django.test import TestCase
from django.contrib.auth.models import User
from pandas import read_csv, notnull

from source_data.etl_tasks.transform_upload import DocTransform
from source_data.etl_tasks.refresh_master import MasterRefresh
from source_data.models import *
from datapoints.models import*

class RefreshMasterTestCase(TestCase):

    def __init__(self, *args, **kwargs):

        super(RefreshMasterTestCase, self).__init__(*args, **kwargs)

    def set_up(self):

        self.region_list = Region.objects.all().values_list('name',flat=True)
        self.test_file_location = 'ebola_data.csv'

        self.create_metadata()
        self.user = User.objects.get(username = 'test')
        self.document = Document.objects.get(doc_title = 'test')

        dt = DocTransform(self.user.id, self.document.id\
            , self.test_file_location)

        self.source_submissions_ids = dt.process_file()

    def test_refresh_master_init(self):

        self.set_up()
        mr = MasterRefresh(self.user.id ,self.document.id)

        self.assertTrue(isinstance,(mr,MasterRefresh))

    def test_refresh_doc_meta(self):

        self.set_up()
        mr = MasterRefresh(self.user.id ,self.document.id)

        ## load this w read_csv(self.test_file_location) remove DocTransform
        source_submissions_data = SourceSubmission.objects\
            .filter(document_id = self.document.id)\
            .values('id','submission_json')

        raw_indicator_list = [k for k,v in json\
            .loads(source_submissions_data[0]['submission_json']).iteritems()]

        mr.refresh_doc_meta()

        source_indicator_id_for_this_doc = DocumentSourceObjectMap.objects\
            .filter(id__in= SourceObjectMap.objects.filter(\
                    content_type = 'indicator',
                    source_object_code__in = raw_indicator_list
                ).values_list('id',flat=True)
            )

        ## should be more specific here.. but this proves with a high degree ##
        ## of certainty that the source_object_map rows have been created ##
        self.assertEqual(len(source_indicator_id_for_this_doc)\
            ,len(raw_indicator_list))

    def test_submission_detail_refresh(self,):

        self.set_up()
        mr = MasterRefresh(self.user.id ,self.document.id)
        mr.refresh_doc_meta()

        source_submissions_data = SourceSubmission.objects\
            .filter(document_id = self.document.id)\
            .values('id','submission_json')

        mr.refresh_submission_details()

        submission_details = SourceSubmissionDetail.objects\
            .filter(document_id = self.document.id)

        self.assertEqual(len(source_submissions_data)\
            ,len(submission_details))


    # def test_source_submission_to_doc_datapoints(self):
    #     '''
    #     '''
    #     self.set_up()
    #
    #     mr = MasterRefresh(self.user.id, self.document.id)
    #     doc_datapoint_ids = mr.process_doc_datapoints(self.source_submissions)
    #
    #     self.assertTrue(doc_datapoint_ids)
    #
    # def test_mapping(self):
    #     '''
    #     Here we ensure that after mapping all of the meta data that we have the
    #     expected number of rows with the appropiate data associated.
    #     '''
    #
    # def test_unmapping(self):
    #     '''
    #     Here we ensure that if there is data in the datapoints table that
    #     cooresponds to a non existing mapping that we remove it.
    #     '''
    #     pass
    #
    # def test_re_mapping(self):
    #     '''
    #     When metadata assigned to a new master_id - make sure that datapoints do as well
    #     '''


    def create_metadata(self):
        '''
        Creating the Indicator, Region, Campaign, meta data needed for the
        system to aggregate / caclulate.
        '''
        campaign_df = read_csv('datapoints/tests/_data/campaigns.csv')
        region_df= read_csv('datapoints/tests/_data/regions.csv')
        indicator_df = read_csv('datapoints/tests/_data/indicators.csv')
        calc_indicator_df = read_csv\
            ('datapoints/tests/_data/calculated_indicator_component.csv')

        user_id = User.objects.create_user('test','john@john.com', 'test').id
        office_id = Office.objects.create(id=1,name='test').id

        cache_job_id = CacheJob.objects.create(id = -2,date_attempted = '2015-01-01',\
            is_error = False)

        status_id = ProcessStatus.objects.create(
                status_text = 'TO_PROCESS',
                status_description = 'TO_PROCESS').id

        document_id = Document.objects.create(
            doc_title = 'test',
            created_by_id = user_id,
            guid = 'test').id

        for ddt in ['uq_id_column','username_column','image_col',
            'campaign_column','region_column','region_display_name']:

            DocDetailType.objects.create(name=ddt)

        for rt in ["country","settlement","province","district","sub-district"]:
            DocDetailType.objects.create(name=rt)


        campaign_type = CampaignType.objects.create(id=1,name="test")

        region_ids = self.model_df_to_data(region_df,Region)
        campaign_ids = self.model_df_to_data(campaign_df,Campaign)
        indicator_ids = self.model_df_to_data(indicator_df,Indicator)
        calc_indicator_ids = self.model_df_to_data(calc_indicator_df,\
            CalculatedIndicatorComponent)

        rg_conif = DocumentDetail.objects.create(
            document_id = document_id,
            doc_detail_type_id = DocDetailType\
                .objects.get(name='region_column').id,
            doc_detail_value = 'Wardcode'
        )

        cp_conif = DocumentDetail.objects.create(
            document_id = document_id,
            doc_detail_type_id = DocDetailType\
                .objects.get(name='campaign_column').id,
            doc_detail_value = 'Campaign'
        )

        uq_id_config = DocumentDetail.objects.create(
            document_id = document_id,
            doc_detail_type_id = DocDetailType\
                .objects.get(name='uq_id_column').id,
            doc_detail_value = 'uq_id'
        )


    def model_df_to_data(self,model_df,model):

        meta_ids = []

        non_null_df = model_df.where((notnull(model_df)), None)
        list_of_dicts = non_null_df.transpose().to_dict()

        for row_ix, row_dict in list_of_dicts.iteritems():

            row_id = model.objects.create(**row_dict)
            meta_ids.append(row_id)

        return meta_ids
