from django.test import TestCase
from django.contrib.auth.models import User
from pandas import read_csv

from datapoints.models import Indicator, Campaign, CampaignType,\
    Region, DataPoint, Office, RegionType
from source_data.models import Source, Document, SourceDataPoint, SourceRegion,\
    SourceCampaign, SourceIndicator


class RefreshMasterTestCase(TestCase):

    def __init__(self, *args, **kwargs):

        super(RefreshMasterTestCase, self).__init__(*args, **kwargs)

    def set_up(self):

        self.region_1_name = 'Pakistan - Balochistan'
        self.region_2_name ='Pakistan - Lakki Marwat'
        self.indicator_string = 'Number of all missed children'
        self.campaign_string = 'Pakistan July 2014'

        self.source = Source.objects.create(
            source_name = 'test',
            source_description = 'test')

        self.user = User.objects.create(username = 'test_user')

        self.document = Document.objects.create(
            doc_text = 'test_text',
            created_by_id  = self.user.id,
            guid = 'refresh_master_test')

        # self.source_indicator = SourceIndicator.objects.create(
        #     indicator_string = self.indicator_string)


        # self.source_campaign= SourceCampaign.objects.create(
        #     campaign_string = self.campaign_string,
        #     document_id = self.document.id,
        #     office_id = self.office.id)

        # self.source_region_1 = SourceRegion.objects.create(
        #     region_string = self.region_1_name,
        #     document_id = self.document.id)
        #
        # self.source_region_2 = SourceRegion.objects.create(
        #     region_string = self.region_2_name,
        #     document_id = self.document.id)


        self.indicator = Indicator.objects.create(
                name = self.indicator_string,
                source_id = self.source.id)

        self.office = Office.objects.create(name = 'Pakistan')

        self.campaign_type = CampaignType.objects.create(name='global')


        ## need a source_campaign_id column in here ##
        self.campaign = Campaign.objects.create(
            office_id = self.office.id,
            start_date = '2014-07-01',
            end_date = '2014-07-01',
            campaign_type_id = self.campaign_type.id)

        self.region_type = RegionType.objects.create(name='district')

        self.region_1 = Region.objects.create(
            name = self.region_1_name,
            region_type_id = self.region_type.id,
            office_id = self.office.id,
            source_id = self.source.id,
            # source_region_id = self.source_region_1.id,
            region_code = self.source_region_1.region_string.replace(' ','-'))

        self.region_1 = Region.objects.create(
            name = self.region_2_name,
            region_type_id = self.region_type.id,
            office_id = self.office.id,
            source_id = self.source.id,
            # source_region_id = self.source_region_2.id,
            region_code = self.source_region_2.region_string.replace(' ','-'))

        self.source_datapoints = self.build_source_datapoint_list()


    def build_source_datapoint_list(self):

        sdp_df = read_csv('datapoints/tests/_data/source_datapoint_msd_chd.csv')

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
