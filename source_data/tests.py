from django.test import TestCase
from source_data.models import SourceDataPoint, Document, ProcessStatus
from datapoints.models import Source
from django.contrib.auth.models import User

class NewDPTestCase(TestCase):

    def setUp(self):

        user = User.objects.create(username='test_user')
        source = Source.objects.create(source_name='test_source')
        document = Document.objects.create(docfile='asfasfasf',created_by=user)
        to_process_status = ProcessStatus.objects.create(status_text='TO_PROCESS')
        success_insert_status = ProcessStatus.objects.create(status_text='SUCESS_INSERT')

        self.cell_value = '8.8'

        sdp = SourceDataPoint.objects.create(
              region_string = 'test region',
              campaign_string = 'test campaign',
              indicator_string = 'test indicator',
              cell_value = self.cell_value,
              row_number= 1,
              source_id = source.id,
              document_id = document.id,
              source_guid = 'thisisafakeguid',
              status = to_process_status,
        )

        self.sdp_id = sdp.id

        # create
          # source datapoint
          # source region
          # source campaign
          # source indicator

          # region map
          # campaign map
          # indicator map



    def test_sdp_to_dp(self):

        # self.assertEqual(1,1)

        sdp = SourceDataPoint.objects.get(id=self.sdp_id)
        self.assertEqual(sdp.get_val(), self.cell_value) # dp exists

        # run refresh master
