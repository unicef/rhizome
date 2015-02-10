from django.test import TestCase
from django.contrib.auth.models import User
from pandas import read_csv

from source_data.models import Source, Document, SourceDataPoint

class RefreshMasterTestCase(TestCase):

    def __init__(self, *args, **kwargs):

        super(RefreshMasterTestCase, self).__init__(*args, **kwargs)

    def set_up(self):

        self.source = Source.objects.create(
            source_name = 'test',
            source_description = 'test')

        self.user = User.objects.create(username='test_user')

        self.document = Document.objects.create(
            doc_text = 'test_text',
            created_by_id  = self.user.id,
            guid = 'refresh_master_test')

        self.source_datapoints = self.build_source_datapoint_list()

        print self.source_datapoints

    def build_source_datapoint_list(self):

        sdp_df = read_csv('datapoints/tests/_data/source_datapoint_msd_chd.csv')

        print sdp_df[:5]

        sdp_list = []

        for sdp in sdp_df.iterrows():

            sdp_ix, sdp_data = sdp[0],sdp[1]

            sdp_dict = {
                'region_string': sdp_data['region_string'],
                'campaign_string': sdp_data['campaign_string'],
                'indicator_string': sdp_data['indicator_string'],
                'cell_value' : sdp_data['cell_value'],
                'row_number' : sdp_data['row_number'],
                'source_guid': sdp_data['guid'],
                'source_id' : self.source.id,
                'document_id': self.document.id,
            }

            sdp_obj = SourceDataPoint(**sdp_dict)
            sdp_list.append(sdp_obj)

        return sdp_list

    # def test_refresh_master(self, indicator_id):
    def test_refresh_master(self):

        self.set_up()

        self.assertEqual(1,1)
