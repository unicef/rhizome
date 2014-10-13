from django.test import TestCase

from source_data.models import *
from source_data.etl_tasks.transform_odk import VcmSummaryTransform

# from datapoints.models import *


class OdkTestCase(TestCase):
    ''' this test takes a record from the VCM Summary table, and inserts ALL
    records into the source datapoints table '''

    def setUp(self):

        Source.objects.create(source_name='odk',source_description='thisisfake')

        self.cnt_tot_newborns = '345'
        self.cnt_census2_11mof = '34'
        self.sett_code = '12345'
        self.date_implement = '2014-02-01'

        self.to_process_status = ProcessStatus.objects.create(status_text='TO_PROCESS')
        self.success_insert_status = ProcessStatus.objects.create(status_text='SUCESS_INSERT')

        self.vcm_sum = VCMSummaryNew.objects.create(
          key = 'testkeyfromodk',
          process_status = self.to_process_status,
          request_guid = 'somethignfake',
          dateofreport = '2014-01-01',
          date_implement = self.date_implement,
          settlementcode = self.sett_code,
          tot_newborns = self.cnt_tot_newborns,
          census2_11mof = self.cnt_census2_11mof,
        )


    def test_source_datapoint_creation(self):

        v= VcmSummaryTransform('thisisafakerequestid')
        v.vcm_summary_to_source_datapoints()

        sdp_1 = SourceDataPoint.objects.get(indicator_string='tot_newborns')
        self.assertEqual(sdp_1.cell_value,self.cnt_tot_newborns)

        sdp_2 = SourceDataPoint.objects.get(indicator_string='census2_11mof')
        self.assertEqual(sdp_2.cell_value,self.cnt_census2_11mof)

        self.assertEqual(self.sett_code,sdp_1.region_string)
        self.assertEqual(self.date_implement,sdp_1.campaign_string)
