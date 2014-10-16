import time
import decimal
from datetime import timedelta

from django.test import TestCase
from django.contrib.auth.models import User

from source_data.etl_tasks.refresh_master import MasterRefresh
from source_data.etl_tasks.transform_odk import VcmSummaryTransform
from source_data.models import *
from datapoints.models import *


class NewDPTestCase(TestCase):
    ''' this test goes through creating all of the metadata and mapping needed
    to create a datapoint.  the datapoint is not inserted here directly but all
    of the requisite data is first, finally allowing the "refresh_master" method
    to sync the DB '''

    def setUp(self):

        self.user = User.objects.create(username='test_user')
        self.office = Office.objects.create(name='test_office')
        self.source = Source.objects.create(source_name='test_source')
        self.document = Document.objects.create(docfile='asfasfasf',created_by=self.user)
        self.to_process_status = ProcessStatus.objects.create(status_text='TO_PROCESS')
        self.success_insert_status = ProcessStatus.objects.create(status_text='SUCCESS_INSERT')
        self.success_update_status = ProcessStatus.objects.create(status_text='SUCCESS_UPDATE')
        self.overriden_status = ProcessStatus.objects.create(status_text='OVERRIDEN')



        self.region_string = 'test region'
        self.campaign_string = 'test campaign'
        self.indicator_string = 'test indicator'

        self.cell_value = '8.8'

        # create source datapoint
        self.sdp = SourceDataPoint.objects.create(
              region_string = self.region_string,
              campaign_string = self.campaign_string,
              indicator_string = self.indicator_string,
              cell_value = self.cell_value,
              row_number= 1,
              source_id = self.source.id,
              document_id = self.document.id,
              source_guid = 'thisisafakeguid',
              status = self.to_process_status,
        )

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

        # create campaign (master)
        self.campaign = Campaign.objects.create(
            name = 'fake campaign',
            office = self.office,
            start_date = time.strftime("%Y-%m-%d"),
            end_date = time.strftime("%Y-%m-%d"),
        )




    def test_source_metadata_creation(self):
        ''' here we ensure that by creating source datapoitns
        with the strings and source ids above that the cooresponding
        metadata'''

        m = MasterRefresh(records = [self.sdp] ,user_id=self.user.id)
        m.get_mappings()

        src_reg = SourceRegion.objects.get(region_string=self.region_string,source_id=self.source.id)
        src_camp = SourceCampaign.objects.get(campaign_string=self.campaign_string,source_id=self.source.id)
        src_ind = SourceIndicator.objects.get(indicator_string=self.indicator_string,source_id=self.source.id)



    def source_metadata_mapping(self):
        ''' here we create mappings based on the data created above
        and ensure that the IDs are such that we mapped them to '''

        m = MasterRefresh(records = [self.sdp] ,user_id=self.user.id)

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

        cmap = CampaignMap.objects.create(
            master_campaign = self.campaign,
            source_campaign = SourceCampaign.objects.get(campaign_string=\
                self.campaign_string,source=self.source),
            mapped_by = self.user
        )


        mappings_post = m.get_mappings()

        self.assertEqual(self.region.id,mappings_post['regions'][self.region_string])
        self.assertEqual(self.campaign.id,mappings_post['campaigns'][self.campaign_string])
        self.assertEqual(self.indicator.id,mappings_post['indicators'][self.indicator_string])


    def test_sdp_to_dp(self):
        '''This tests the behavior of the refresh_master method. Test that a
        new SDP gets inserted, an update gets update, and the existing value
        is overriden.'''

        self.source_metadata_mapping()
        m = MasterRefresh(records = [self.sdp] ,user_id=self.user.id)
        # this refreshes master, so that newly mapped data makes it in!
        m.main()

        dp = DataPoint.objects.get(source_datapoint_id = self.sdp.id)

        # Make Sure the Value is the same
        self.assertEqual(float(self.sdp.get_val()), float(dp.value))

        # make sure the process status is correct

        self.assertEqual(self.sdp.status_id,
          ProcessStatus.objects.get(status_text='SUCCESS_INSERT').id)

        ## now create another SDP, and update the original, checking the process status in both cases

        new_cell_val = 99


        sdp_new = SourceDataPoint.objects.create(
            indicator_string =  self.sdp.indicator_string,
            region_string = self.sdp.region_string,
            campaign_string = self.sdp.campaign_string,
            cell_value = new_cell_val,
            row_number = 0,
            source_id = self.source.id,
            document_id = self.document.id,
            status_id = self.to_process_status.id,
            created_at = self.sdp.created_at + timedelta(days=1)

        )

        m = MasterRefresh(records = [sdp_new], user_id = self.user.id)
        m.main()

        updated_dp = DataPoint.objects.get(source_datapoint_id = sdp_new.id)

        ## DID THE VALUE GET UPDATED
        self.assertEqual(updated_dp.value,new_cell_val)
