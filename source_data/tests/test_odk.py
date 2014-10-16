import pprint as pp

from django.test import TestCase

from datapoints.models import *
from source_data.models import *
from source_data.etl_tasks.transform_odk import VcmSummaryTransform
from source_data.etl_tasks.refresh_master import MasterRefresh


# from datapoints.models import *


class OdkTestCase(TestCase):
    ''' this test takes a record from the VCM Summary table, and inserts ALL
    records into the source datapoints table '''

    def setUp(self):

        self.source = Source.objects.create(source_name='odk',source_description='thisisfake')
        self.user = User.objects.create(username='test_user')

        self.cnt_tot_newborns = '345'
        self.cnt_census2_11mof = '34'
        self.sett_code = '12345'
        self.date_implement = '2014-02-01'
        self.odk_key = 'testkeyfromodk'

        self.to_process_status = ProcessStatus.objects.create(status_text='TO_PROCESS')
        self.success_insert_status = ProcessStatus.objects.create(status_text='SUCCESS_INSERT')

        self.vcm_sum = VCMSummaryNew.objects.create(
          key = self.odk_key,
          process_status = self.to_process_status,
          request_guid = 'somethignfake',
          dateofreport = '2014-01-01',
          date_implement = self.date_implement,
          settlementcode = self.sett_code,
          tot_newborns = self.cnt_tot_newborns,
          census2_11mof = self.cnt_census2_11mof,
        )

        ## Master Meta Data ##
        self.office = Office.objects.create(name='FAKE')

        self.region = Region.objects.create(
            full_name = 'Da Bronx',
            region_code = 42424,
            region_type = 'LGA',
            office = self.office,
            source = self.source,
            source_guid = 'somethingtotallyfake'
        )

        self.campaign = Campaign.objects.create(
            name = 'test campaign',
            office = self.office,
            start_date = '2014-01-01',
            end_date = '2014-01-01',
        )

        self.indicator_01 = Indicator.objects.create(
            short_name = 'fake',
            name = 'faker',
            description = 'fakest'
        )

        self.indicator_02 = Indicator.objects.create(
            short_name = 'extra fake',
            name = 'super fake',
            description = 'super duper fake'
        )


    def create_source_dps(self):

        v= VcmSummaryTransform('thisisafakerequestid')
        v.vcm_summary_to_source_datapoints()

        sdp_1 = SourceDataPoint.objects.get(indicator_string='tot_newborns')
        self.assertEqual(sdp_1.cell_value,self.cnt_tot_newborns)

        sdp_2 = SourceDataPoint.objects.get(indicator_string='census2_11mof')
        self.assertEqual(sdp_2.cell_value,self.cnt_census2_11mof)

        self.assertEqual(self.sett_code,sdp_1.region_string)
        self.assertEqual(self.date_implement,sdp_1.campaign_string)

        return [sdp_1,sdp_2]

    def add_mappings(self,records):

        m = MasterRefresh(records,self.user.id)

        # CREATE THE SOURCE DATAPOINTS #
        mappings = m.get_mappings()

        RegionMap.objects.create(
          source_region= SourceRegion.objects.get(region_string=self.sett_code\
              ,source=self.source),
          master_region=self.region,
          mapped_by=self.user
        )

        IndicatorMap.objects.create(
          source_indicator= SourceIndicator.objects.get(indicator_string=\
              'tot_newborns',source=self.source),
          master_indicator=self.indicator_01,
          mapped_by=self.user
        )

        IndicatorMap.objects.create(
          source_indicator= SourceIndicator.objects.get(indicator_string=\
              'census2_11mof',source=self.source),
          master_indicator=self.indicator_02,
          mapped_by=self.user
        )

        CampaignMap.objects.create(
          source_campaign= SourceCampaign.objects.get(campaign_string=\
              self.date_implement,source=self.source),
          master_campaign=self.campaign,
          mapped_by=self.user
        )


        return mappings


    def test_(self):

        sdps = self.create_source_dps()

        ## Making Sure that the process status was set properly ##

        self.assertEqual(self.success_insert_status.id,
            VCMSummaryNew.objects.get(key=self.odk_key).process_status_id)

        mappings = self.add_mappings(sdps)

        # Adding the ODK data via the Refresh Master Method
        m = MasterRefresh(sdps,self.user.id)
        m.main()

        dp_1 = DataPoint.objects.get(
            region=self.region,
            campaign=self.campaign,
            indicator=self.indicator_01
        )

        dp_2 = DataPoint.objects.get(
            region=self.region,
            campaign=self.campaign,
            indicator=self.indicator_02
        )

        self.assertEqual(dp_1.value,int(self.cnt_tot_newborns))
        self.assertEqual(dp_2.value,int(self.cnt_census2_11mof))
