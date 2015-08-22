import hashlib
import random

from django.test import TestCase
from django.contrib.auth.models import User
from pandas import read_csv

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


        self.document = Document.objects.create(
            created_by=self.user,
            docfile='test-doc',
            guid='test-doc',
            doc_text='test-doc',
            is_processed=False,
        )

        self.source_datapoints = [] # self.build_source_datapoint_list()


    def build_source_datapoint_list(self):
        '''
        Part of the set up method, this takes a csv and inserts it into the
        source datapoints table.  This method in context of this test represents
        what would happen when a user uploads a csv and the data flows through
        "etl_tasks/transform_upload"

        i.e. this testing method should actually just call "transform_upload"
        with the csv directory below.
        '''

        sdp_df = read_csv('datapoints/tests/_data/source_datapoint_msd_chd.csv')
        sdp_ids = []

        return sdp_ids

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
