import hashlib
import random

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

        self.create_metadata()

        self.region_list = Region.objects.all().values_list('name',flat=True)
        self.user = User.objects.get(username='test')

        self.indicator = Indicator.objects.get(name='Number of all missed children')
        self.campaign = Campaign.objects.get(slug='nigeria-2015-06-01')
        self.region = Region.objects.get(name='Bauchi (Province)')

        self.test_file_location = 'ebola_situation_report_vol_194.csv'

        self.document = Document.objects.create(
            created_by=self.user,
            docfile=self.test_file_location,
            guid='test-doc',
            doc_text='test-doc',
            is_processed=False,
        )

        self.create_metadata()

    def test_doc_to_source_submission(self):
        '''
        Part of the set up method, this takes a csv and inserts it into the
        source submissino table.  This method in context of this test represents
        what would happen when a user uploads a csv and the data flows through
        "etl_tasks/transform_upload"

        Uploading the csv to the server is itself a different task.. so for now
        we preform "transform_upload" on the test file.

        This method is in charge of one specific thing.. taking an input stream
        such as a csv, or an ODK submission, and creating one row in the
        database with the schema that it was received.  Later in the ingest
        process, users are allowed to specify settings to each file in order
        to translate them into data the application can consume and visualize.

        The Doc Transofrm Method is responsible for the following:
            1. Inserting one record into source_submission for each csv row
            2. Inserting any new mappings into source_object_map
            3. Associating *all* source_object_maps with self.document_id ( even
              those created in other documents)
            4. Inserting one record into source_submission_detail        '''

        self.set_up()

        dt = DocTransform(self.user_id, self.document.id)
        source_submissions = dt.process_file()

        test_file = open(settings.MEDIA_ROOT + self.test_file_location ,'r')
        file_line_count = sum(1 for line in test_file) - 1 # for the header!

        self.assertEqual(len(source_submissions),file_line_count)

    def test_source_data_points_to_doc_datapoints(self):

        mr = MasterRefresh(self.user.id, self.document.id)
        doc_datapoint_ids = mr.process_doc_datapoints(self.source_submissions)

        self.assertTrue(doc_datapoint_ids)

    def test_refresh_master_init(self):

        self.set_up()

        mr = MasterRefresh(self.user.id\
            ,self.document.id)

        self.assertTrue(isinstance,(mr,MasterRefresh))
        self.assertEqual(self.document.id,mr.document_id)


    def test_mapping(self):
        '''
        Here we ensure that after mapping all of the meta data that we have the
        expected number of rows with the appropiate data associated.
        '''

        self.set_up()
        self.assertEqual(1,1)


    def test_unmapping(self):
        '''
        Here we ensure that if there is data in the datapoints table that
        cooresponds to a non existing mapping that we remove it.
        '''
        pass

    def test_re_mapping(self):
        '''
        When metadata assigned to a new master_id - make sure that datapoints do as well
        '''

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
                status_text = 'test',
                status_description = 'test').id

        document_id = Document.objects.create(
            doc_title = 'test',
            created_by_id = user_id,
            guid = 'test').id

        region_type1 = RegionType.objects.create(id=1,name="country")
        region_type2 = RegionType.objects.create(id=2,name="settlement")
        region_type3 = RegionType.objects.create(id=3,name="province")
        region_type4 = RegionType.objects.create(id=4,name="district")
        region_type5 = RegionType.objects.create(id=5,name="sub-district")

        campaign_type = CampaignType.objects.create(id=1,name="test")

        region_ids = self.model_df_to_data(region_df,Region)
        campaign_ids = self.model_df_to_data(campaign_df,Campaign)
        indicator_ids = self.model_df_to_data(indicator_df,Indicator)
        calc_indicator_ids = self.model_df_to_data(calc_indicator_df,\
            CalculatedIndicatorComponent)


    def model_df_to_data(self,model_df,model):

        meta_ids = []

        non_null_df = model_df.where((notnull(model_df)), None)
        list_of_dicts = non_null_df.transpose().to_dict()

        for row_ix, row_dict in list_of_dicts.iteritems():

            row_id = model.objects.create(**row_dict)
            meta_ids.append(row_id)

        return meta_ids
