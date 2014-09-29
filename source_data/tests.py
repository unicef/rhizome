from django.test import TestCase
from django.contrib.auth.models import User

from source_data.etl_tasks.refresh_master import MasterRefresh
from source_data.models import SourceDataPoint, Document, ProcessStatus
from datapoints.models import Source

class NewDPTestCase(TestCase):

    def setUp(self):

        self.user = User.objects.create(username='test_user')
        self.source = Source.objects.create(source_name='test_source')
        self.document = Document.objects.create(docfile='asfasfasf',created_by=self.user)
        self.to_process_status = ProcessStatus.objects.create(status_text='TO_PROCESS')
        self.success_insert_status = ProcessStatus.objects.create(status_text='SUCESS_INSERT')

        self.cell_value = '8.8'

        sdp = SourceDataPoint.objects.create(
              region_string = 'test region',
              campaign_string = 'test campaign',
              indicator_string = 'test indicator',
              cell_value = self.cell_value,
              row_number= 1,
              source_id = self.source.id,
              document_id = self.document.id,
              source_guid = 'thisisafakeguid',
              status = self.to_process_status,
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

        # get the object by id
        sdp = SourceDataPoint.objects.get(id=self.sdp_id)

        # Make Sure the Value is
        self.assertEqual(sdp.get_val(), self.cell_value) # dp exists

        # refresh master
        m = MasterRefresh(records = [sdp],user_id = self.user.id)
        m.get_mappings()
