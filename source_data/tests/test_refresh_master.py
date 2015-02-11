import hashlib
import random

from django.test import TestCase
from django.contrib.auth.models import User
from pandas import read_csv

from source_data.etl_tasks.refresh_master import MasterRefresh
from source_data.models import Source, Document, SourceDataPoint, SourceRegion,\
    SourceCampaign, SourceIndicator, ProcessStatus
from datapoints.models import Indicator, Campaign, CampaignType,\
    Region, DataPoint, Office, RegionType



class RefreshMasterTestCase(TestCase):

    def __init__(self, *args, **kwargs):


        super(RefreshMasterTestCase, self).__init__(*args, **kwargs)

    def set_up(self):

        self.status = ProcessStatus.objects.create(
            status_text = 'test',
            status_description = 'test')

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

        self.indicator = Indicator.objects.create(
                name = self.indicator_string,
                source_id = self.source.id)

        self.office = Office.objects.create(name = 'Pakistan')

        self.campaign_type = CampaignType.objects.create(name='global')

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
            region_code = self.region_1_name)

        self.region_1 = Region.objects.create(
            name = self.region_2_name,
            region_type_id = self.region_type.id,
            office_id = self.office.id,
            source_id = self.source.id,
            region_code = self.region_2_name)

        self.source_datapoints = self.build_source_datapoint_list()


    def build_source_datapoint_list(self):

        sdp_df = read_csv('datapoints/tests/_data/source_datapoint_msd_chd.csv')

        sdp_ids = []
        sdp_insert_batch = []

        for sdp in sdp_df.iterrows():

            sdp_ix, sdp_data = sdp[0],sdp[1]

            sdp_dict = {
                'id': sdp_data['id'],
                'region_string': sdp_data['region_string'],
                'region_code': sdp_data['region_code'],
                'campaign_string': sdp_data['campaign_string'],
                'indicator_string': sdp_data['indicator_string'],
                'cell_value' : sdp_data['cell_value'],
                'row_number' : sdp_data['row_number'],
                'source_guid': sdp_data['guid'],
                'guid':hashlib.sha1(str(random.random())).hexdigest(),
                'source_id' : self.source.id,
                'document_id': self.document.id,
                'status_id': self.status.id
            }

            sdp_obj = SourceDataPoint(**sdp_dict)
            sdp_insert_batch.append(sdp_obj)

            sdp_ids.append(sdp_data.id)

        SourceDataPoint.objects.bulk_create(sdp_insert_batch)

        return sdp_ids

    # def test_refresh_master(self, indicator_id):
    def test_refresh_master(self):

        self.set_up()

        ## instatiate the master refresh ##
        mr = MasterRefresh(self.source_datapoints,self.user.id\
            ,self.document.id,self.indicator.id)

        ## create the source metadata ( we are testing this method) ##
        mr.create_source_meta_data()

        sc = SourceCampaign.objects.raw("""
            SELECT sd.id FROM source_datapoint sd\
            WHERE document_id = %s\
            AND NOT EXISTS (\
                SELECT 1 FROM source_campaign sc\
                WHERE sd.campaign_string = sc.campaign_string)\
            """, [self.document.id])

        missing_campaign_rows = sum(1 for result in sc)

        self.assertEqual(0,missing_campaign_rows)

        ## does every Indicator string has a cooresponding source_campaign? ##
        si = SourceIndicator.objects.raw("""
            SELECT sd.id FROM source_datapoint sd\
            WHERE document_id = %s\
            AND NOT EXISTS (\
                SELECT 1 FROM source_indicator si\
                WHERE sd.indicator_string = si.indicator_string)\
            """, [self.document.id])

        missing_indicator_rows = sum(1 for result in si)

        self.assertEqual(0,missing_indicator_rows)


        ## does every region CODE has a cooresponding source_region? ##
