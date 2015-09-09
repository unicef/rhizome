import hashlib
import random

from django.test import TestCase
from django.contrib.auth.models import User
from pandas import read_csv

from source_data.etl_tasks.transform_upload import DocTransform
from source_data.etl_tasks.refresh_master import MasterRefresh
from source_data.models import *
from datapoints.models import*

class RefreshMasterTestCase(TestCase):

    def __init__(self, *args, **kwargs):

        super(RefreshMasterTestCase, self).__init__(*args, **kwargs)

    def set_up(self):

        self.region_list = Region.objects.all().values_list('name',flat=True)
        self.user = User.objects.get(username='demo_user')

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

        self.source_datapoints = [] # self.build_source_datapoint_list()


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
#
