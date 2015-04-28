import hashlib
import random

from django.test import TestCase
from django.contrib.auth.models import User
from pandas import read_csv

from source_data.etl_tasks.refresh_master import MasterRefresh,\
    create_source_meta_data
from source_data.models import Source, Document, SourceDataPoint, SourceRegion,\
    SourceCampaign, SourceIndicator, ProcessStatus, RegionMap, IndicatorMap,\
    CampaignMap
from datapoints.models import Indicator, Campaign, CampaignType,\
    Region, DataPoint, Office, RegionType



class RefreshMasterTestCase(TestCase):

    def __init__(self, *args, **kwargs):

        super(RefreshMasterTestCase, self).__init__(*args, **kwargs)

    def set_up(self):

        self.status = ProcessStatus.objects.create(
            status_text = 'test',
            status_description = 'test')

        self.region_1_name = 'Nigeria - Bauchi'
        self.region_2_name ='Pakistan - Lakki Marwat'

        self.region_1_code = 'Nigeria---Bauchi'
        self.region_2_code ='Pakistan---Lakki Marwat'

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
            region_code = self.region_1_code,
            region_type_id = self.region_type.id,
            office_id = self.office.id,
            source_id = self.source.id)

        self.region_2 = Region.objects.create(
            name = self.region_2_name,
            region_code = self.region_2_code,
            region_type_id = self.region_type.id,
            office_id = self.office.id,
            source_id = self.source.id)

        self.source_datapoints = self.build_source_datapoint_list()


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
    def test_refresh_master_init(self):

        self.set_up()

        ## instatiate the master refresh ##
        mr = MasterRefresh(self.source_datapoints,self.user.id\
            ,self.document.id,self.indicator.id)

        self.assertTrue(isinstance,(mr,MasterRefresh))
        self.assertEqual(self.document.id,mr.document_id)


    def test_source_metadata_creation(self):
        '''
        The first thing that should happen when the master refresh is
        instatiated.  For the source Datapoints
        '''

        self.set_up()

        ## create the source metadata ( we are testing this method) ##
        create_source_meta_data(self.document.id)

        sc = SourceCampaign.objects.raw("""
            SELECT sd.id FROM source_datapoint sd\
            WHERE document_id = %s\
            AND NOT EXISTS (\
                SELECT 1 FROM source_campaign sc\
                WHERE sd.campaign_string = sc.campaign_string)\
            """, [self.document.id])

        missing_campaign_rows = sum(1 for result in sc)

        ## does every Indicator string has a cooresponding source_indicator? ##
        si = SourceIndicator.objects.raw("""
            SELECT sd.id FROM source_datapoint sd\
            WHERE document_id = %s\
            AND NOT EXISTS (\
                SELECT 1 FROM source_indicator si\
                WHERE sd.indicator_string = si.indicator_string)\
            """, [self.document.id])

        missing_indicator_rows = sum(1 for result in si)

        ## does every region code has a cooresponding source_region? ##
        sr = SourceRegion.objects.raw("""
            SELECT sd.id FROM source_datapoint sd\
            WHERE document_id = %s\
            AND NOT EXISTS (\
                SELECT 1 FROM source_region sr\
                WHERE sd.region_code = sr.region_code)\
            """, [self.document.id])

        missing_region_rows = sum(1 for result in sr)

        ## does every source_db row have a a cooresponding source_region? ##

        self.assertEqual(0,missing_indicator_rows)
        self.assertEqual(0,missing_campaign_rows)
        self.assertEqual(0,missing_region_rows)


    def test_mapping(self):
        '''
        Here we ensure that after mapping all of the meta data that we have the
        expected number of rows with the appropiate data associated.
        '''

        self.set_up()

        mr = MasterRefresh(self.source_datapoints,self.user.id\
            ,self.document.id,self.indicator.id)

        ## create the source metadata ##
        create_source_meta_data(self.document.id)

        ## create mappings ( this is mimicking how bo would map metadata ) ##
        rm_1 = RegionMap.objects.create(
            mapped_by_id = self.user.id,
            source_id = SourceRegion.objects.get(region_code=self\
                .region_1_code).id,
            master_id = self.region_1.id)

        cm_1 = CampaignMap.objects.create(
            mapped_by_id = self.user.id,
            source_id = SourceCampaign.objects.get(campaign_string=\
                self.campaign_string).id,
            master_id = self.campaign.id)

        im_1 = IndicatorMap.objects.create(
            mapped_by_id = self.user.id,
            source_id = SourceIndicator.objects.get(indicator_string=\
                self.indicator_string).id,
            master_id = self.indicator.id)

        mr.source_dps_to_dps()

        x = DataPoint.objects.filter(
            region_id = self.region_1.id,
            campaign_id = self.campaign.id,
            indicator_id = self.indicator.id,
        )

        self.assertEqual(len(x),1)


    def test_unmapping(self):
        '''
        Here we ensure that if there is data in the datapoints table that
        cooresponds to a non existing mapping that we remove it.
        '''
        pass
