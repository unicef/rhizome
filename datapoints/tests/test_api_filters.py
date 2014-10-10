import time
import decimal
import pprint as pp
import urllib, urllib2,json

from django.test import TestCase
from django.contrib.auth.models import User
from tastypie.test import ResourceTestCase

from source_data.etl_tasks.refresh_master import MasterRefresh
from source_data.etl_tasks.transform_odk import VcmSummaryTransform
from source_data.models import *
from datapoints.models import *


class ApiFilterTestCase(ResourceTestCase):
    ''' this test goes through creating all of the metadata and mapping needed
    to create a datapoint.  the datapoint is not inserted here directly but all
    of the requisite data is first, finally allowing the "refresh_master" method
    to sync the DB '''

    def setUp(self):
        super(ApiFilterTestCase, self).setUp()


        self.user = User.objects.create(username='test_user')
        self.office = Office.objects.create(name='test_office')
        self.source = Source.objects.create(source_name='test_source')
        self.document = Document.objects.create(docfile='asfasfasf',created_by=self.user)
        self.to_process_status = ProcessStatus.objects.create(status_text='TO_PROCESS')
        self.success_insert_status = ProcessStatus.objects.create(status_text='SUCESS_INSERT')

        self.region_string = 'test region'
        self.indicator_string = 'test indicator'

        self.campaign_string_01 = '01'
        self.campaign_string_02 = '02'
        self.campaign_string_03 = '03'
        self.campaign_string_04 = '04'
        self.campaign_string_05 = '05'


        self.cell_value = '8.8'

        # create indicator (master)

        self.indicator = Indicator.objects.create(
            name = 'FAKE',
            description = 'this is a fake descriptino'
        )

        # create region (master)
        self.region = Region.objects.create(
            full_name = 'some region',
            region_code = 12414,
            office = self.office,
            latitude = 1.2,
            longitude = 2.1,
            source = self.source,
            source_guid = 'somethingfake'
        )


        # create source datapoint
        self.sdp_01 = SourceDataPoint.objects.create(
              region_string = self.region_string,
              campaign_string = self.campaign_string_01,
              indicator_string = self.indicator_string,
              cell_value = self.cell_value,
              row_number= 1,
              source_id = self.source.id,
              document_id = self.document.id,
              source_guid = 'thisisafakeguid1',
              status = self.to_process_status,
        )


        # create source datapoint
        self.sdp_02 = SourceDataPoint.objects.create(
              region_string = self.region_string,
              campaign_string = self.campaign_string_02,
              indicator_string = self.indicator_string,
              cell_value = self.cell_value,
              row_number= 2,
              source_id = self.source.id,
              document_id = self.document.id,
              source_guid = 'thisisafakeguid2',
              status = self.to_process_status,
        )

        # create source datapoint
        self.sdp_03 = SourceDataPoint.objects.create(
              region_string = self.region_string,
              campaign_string = self.campaign_string_03,
              indicator_string = self.indicator_string,
              cell_value = self.cell_value,
              row_number= 3,
              source_id = self.source.id,
              document_id = self.document.id,
              source_guid = 'thisisafakeguid3',
              status = self.to_process_status,
        )


        # create source datapoint
        self.sdp_04 = SourceDataPoint.objects.create(
              region_string = self.region_string,
              campaign_string = self.campaign_string_04,
              indicator_string = self.indicator_string,
              cell_value = self.cell_value,
              row_number= 4,
              source_id = self.source.id,
              document_id = self.document.id,
              source_guid = 'thisisafakeguid4',
              status = self.to_process_status,
        )

        # create source datapoint
        self.sdp_05 = SourceDataPoint.objects.create(
              region_string = self.region_string,
              campaign_string = self.campaign_string_05,
              indicator_string = self.indicator_string,
              cell_value = self.cell_value,
              row_number= 5,
              source_id = self.source.id,
              document_id = self.document.id,
              source_guid = 'thisisafakeguid5',
              status = self.to_process_status,
        )

        self.all_sdps = [self.sdp_01,self.sdp_02,self.sdp_03,self.sdp_04,self.sdp_05]


        ### MASTER CAMPAIGNS ###
        # create FIVE  (master)
        self.campaign_01 = SourceCampaign.objects.create(
            campaign_string = self.campaign_string_01,
            source_id = self.source.id
        )

        self.campaign_02 = SourceCampaign.objects.create(
            campaign_string = self.campaign_string_02,
            source_id = self.source.id
        )

        self.campaign_03 = SourceCampaign.objects.create(
            campaign_string = self.campaign_string_03,
            source_id = self.source.id
        )

        self.campaign_04 = SourceCampaign.objects.create(
            campaign_string = self.campaign_string_04,
            source_id = self.source.id
        )

        self.campaign_05 = SourceCampaign.objects.create(
            campaign_string = self.campaign_string_05,
            source_id = self.source.id
        )


        ### MASTER CAMPAIGNS ###
        # create FIVE  (master)
        self.campaign_01 = Campaign.objects.create(
            name = '2014-01-01',
            office = self.office,
            start_date = '2014-01-01',
            end_date = '2014-01-01',
        )

        self.campaign_02 = Campaign.objects.create(
            name = '2014-02-01',
            office = self.office,
            start_date = '2014-02-01',
            end_date = '2014-02-01',
        )

        self.campaign_03 = Campaign.objects.create(
            name = '2014-03-01',
            office = self.office,
            start_date = '2014-03-01',
            end_date = '2014-03-01',
        )

        self.campaign_04 = Campaign.objects.create(
            name = '2014-04-01',
            office = self.office,
            start_date = '2014-04-01',
            end_date = '2014-04-01',
        )

        self.campaign_05 = Campaign.objects.create(
            name = '2014-05-01',
            office = self.office,
            start_date = '2014-05-01',
            end_date = '2014-05-01',
        )


    def source_metadata_creation(self):
        ''' here we ensure that by creating source datapoitns
        with the strings and source ids above that the cooresponding
        metadata'''

        m = MasterRefresh(records = self.all_sdps ,user_id=self.user.id)
        m.get_mappings()

        src_reg = SourceRegion.objects.get(region_string=self.region_string,source_id=self.source.id)
        src_ind = SourceIndicator.objects.get(indicator_string=self.indicator_string,source_id=self.source.id)

        src_camp_01 = SourceCampaign.objects.get(campaign_string=self.campaign_string_01,source_id=self.source.id)
        src_camp_02 = SourceCampaign.objects.get(campaign_string=self.campaign_string_02,source_id=self.source.id)
        src_camp_03 = SourceCampaign.objects.get(campaign_string=self.campaign_string_03,source_id=self.source.id)
        src_camp_04 = SourceCampaign.objects.get(campaign_string=self.campaign_string_04,source_id=self.source.id)
        src_camp_05 = SourceCampaign.objects.get(campaign_string=self.campaign_string_05,source_id=self.source.id)



    def source_metadata_mapping(self):
        ''' here we create mappings based on the data created above
        and ensure that the IDs are such that we mapped them to '''

        dps = [self.sdp_01,self.sdp_02,self.sdp_03,self.sdp_04,self.sdp_05]
        m = MasterRefresh(records = dps ,user_id=self.user.id)

        # THIS STEP INSERTS THE SOURCE META DATA THAT WE WILL MAP#
        mappings_pre = m.get_mappings()


        rmap = RegionMap.objects.create(
            master_region = self.region,
            source_region = SourceRegion.objects.get(region_string=\
                self.region_string,source_id=self.source.id),
            mapped_by = self.user
        )

        imap = IndicatorMap.objects.create(
            master_indicator = self.indicator,
            source_indicator = SourceIndicator.objects.get(indicator_string=\
                self.indicator_string,source=self.source),
            mapped_by = self.user
        )

        cmap_01 = CampaignMap.objects.create(
            master_campaign = self.campaign_01,
            source_campaign = SourceCampaign.objects.get(campaign_string=\
                self.campaign_string_01,source=self.source),
            mapped_by = self.user
        )

        cmap_02 = CampaignMap.objects.create(
            master_campaign = self.campaign_02,
            source_campaign = SourceCampaign.objects.get(campaign_string=\
                self.campaign_string_02,source=self.source),
            mapped_by = self.user
        )

        cmap_03 = CampaignMap.objects.create(
            master_campaign = self.campaign_03,
            source_campaign = SourceCampaign.objects.get(campaign_string=\
                self.campaign_string_03,source=self.source),
            mapped_by = self.user
        )

        cmap_04 = CampaignMap.objects.create(
            master_campaign = self.campaign_04,
            source_campaign = SourceCampaign.objects.get(campaign_string=\
                self.campaign_string_04,source=self.source),
            mapped_by = self.user
        )

        cmap_05 = CampaignMap.objects.create(
            master_campaign = self.campaign_05,
            source_campaign = SourceCampaign.objects.get(campaign_string=\
                self.campaign_string_05,source=self.source),
            mapped_by = self.user
        )


        mappings_post = m.get_mappings()


        self.assertEqual(self.region.id,mappings_post['regions'][self.region_string])
        self.assertEqual(self.indicator.id,mappings_post['indicators'][self.indicator_string])

        self.assertEqual(self.campaign_01.id,mappings_post['campaigns'][self.campaign_string_01])
        self.assertEqual(self.campaign_02.id,mappings_post['campaigns'][self.campaign_string_02])
        self.assertEqual(self.campaign_03.id,mappings_post['campaigns'][self.campaign_string_03])
        self.assertEqual(self.campaign_04.id,mappings_post['campaigns'][self.campaign_string_04])
        self.assertEqual(self.campaign_05.id,mappings_post['campaigns'][self.campaign_string_05])


    def sdp_to_dp(self):
        '''  after all is mapped we try to create the source datapoitn
        here.  We make sure that TRUE=1, FALSE=0 and that the value
        stored in the cell was properly converted to a numeric.'''

        self.source_metadata_mapping()
        m = MasterRefresh(records = self.all_sdps ,user_id=self.user.id)
        # this refreshes master, so that newly mapped data makes it in!
        m.main()

        dp_01 = DataPoint.objects.get(source_datapoint_id = self.sdp_01.id)
        dp_02 = DataPoint.objects.get(source_datapoint_id = self.sdp_02.id)
        dp_03 = DataPoint.objects.get(source_datapoint_id = self.sdp_03.id)
        dp_04 = DataPoint.objects.get(source_datapoint_id = self.sdp_04.id)
        dp_05 = DataPoint.objects.get(source_datapoint_id = self.sdp_05.id)

        # Make Sure the Value is the same
        self.assertEqual(float(self.sdp_04.get_val()), float(dp_04.value))

    ### NOWWWWWW WE ACTUALLY TEST THE FUNCTIONALITY!!! ####

    def test_campaign_st_end(self):

        self.sdp_to_dp()

        base_url = '/api/v1/datapoint/'

        params = {}
        params['campaign_start'] = '2014-02-01'
        params['campaign_end'] = '2014-04-01'

        url = base_url + '?' + urllib.urlencode(params)
        response = self.api_client.get(url,follow=True)

        data = json.loads(response.content)

        pp.pprint(data['objects'])

        self.assertEqual(3,len(data['objects']))
