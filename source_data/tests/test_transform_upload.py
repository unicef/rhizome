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
        self.user = User.objects.get(username = 'test')
        self.document = Document.objects.get(doc_title = 'test')

        self.location_list = Location.objects.all().values_list('name',flat=True)
        self.test_file_location = 'ebola_data.csv'

    def test_doc_to_source_submission(self):
        '''
        Part of the set up method, this takes a csv and inserts it into the
        source submission table.  This method in context of this test represents
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

        dt = DocTransform(self.user.id, self.document.id\
            , self.test_file_location)

        source_submissions = dt.process_file()

        test_file = open(settings.MEDIA_ROOT + self.test_file_location ,'r')
        file_line_count = sum(1 for line in test_file) - 1 # for the header!

        self.assertEqual(len(source_submissions),file_line_count)

    def create_metadata(self):
        '''
        Creating the Indicator, location, Campaign, meta data needed for the
        system to aggregate / caclulate.
        '''
        campaign_df = read_csv('datapoints/tests/_data/campaigns.csv')
        location_df= read_csv('datapoints/tests/_data/locations.csv')
        indicator_df = read_csv('datapoints/tests/_data/indicators.csv')
        calc_indicator_df = read_csv\
            ('datapoints/tests/_data/calculated_indicator_component.csv')

        user_id = User.objects.create_user('test','john@john.com', 'test').id
        office_id = Office.objects.create(id=1,name='test').id

        cache_job_id = CacheJob.objects.create(id = -2, \
            date_attempted = '2015-01-01',is_error = False)

        status_id = ProcessStatus.objects.create(
                status_text = 'TO_PROCESS',
                status_description = 'TO_PROCESS').id

        document_id = Document.objects.create(
            doc_title = 'test',
            created_by_id = user_id,
            guid = 'test').id

        for ddt in ['uq_id_column','username_column','image_col',
            'campaign_column','location_column','location_display_name']:

            DocDetailType.objects.create(name=ddt)

        for rt in ["country","settlement","province","district","sub-district"]:
            DocDetailType.objects.create(name=rt)


        campaign_type = ResultStructureType.objects.create(id=1,name="test")

        location_ids = self.model_df_to_data(location_df,Location)
        campaign_ids = self.model_df_to_data(campaign_df,ResultStructure)
        indicator_ids = self.model_df_to_data(indicator_df,Indicator)
        calc_indicator_ids = self.model_df_to_data(calc_indicator_df,\
            CalculatedIndicatorComponent)

        ## create the uq_id_column configuration ##

        uq_id_config = DocumentDetail.objects.create(
            document_id = document_id,
            doc_detail_type_id = DocDetailType\
                .objects.get(name='uq_id_column').id,
            doc_detail_value = 'uq_id'
        )

        location_column_config = DocumentDetail.objects.create(
            document_id = document_id,
            doc_detail_type_id = DocDetailType\
                .objects.get(name='location_column').id,
            doc_detail_value = 'Wardcode'
        )

        campaign_column_config = DocumentDetail.objects.create(
            document_id = document_id,
            doc_detail_type_id = DocDetailType\
                .objects.get(name='campaign_column').id,
            doc_detail_value = 'Campaign'
        )


    def model_df_to_data(self,model_df,model):

        meta_ids = []

        non_null_df = model_df.where((notnull(model_df)), None)
        list_of_dicts = non_null_df.transpose().to_dict()

        for row_ix, row_dict in list_of_dicts.iteritems():

            row_id = model.objects.create(**row_dict)
            meta_ids.append(row_id)

        return meta_ids
