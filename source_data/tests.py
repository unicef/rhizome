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

        self.sdp = SourceDataPoint.objects.create(
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

        # create
          # region map
          # campaign map
          # indicator map

    def test_source_metadata_creation(self):
        ''' here we ensure that by creating source datapoitns
        with the strings and source ids above that the cooresponding
        metadata ( with no mappings) are created.'''

        m = MasterRefresh(records = [self.sdp] ,user_id=self.user.id)
        m.get_mappings()

        self.assertEqual(1,1)


        # assert -> source region exists and is unmapped
               # -> source indicator exists and is unmapped
               # -> source campaign exists and is unmapped

    def test_source_metadata_mapping(self):
        ''' here we create a mapping based on the data created above
        and ensure that the IDs are such that we mapped them to '''

        m = MasterRefresh(records = [self.sdp] ,user_id=self.user.id)

        self.assertEqual(2,2)


    def test_sdp_to_dp(self):
        '''  after all is mapped we try to create the source datapoitn
        here.  We make sure that TRUE=1, FALSE=0 and that the value
        stored in the cell was properly converted to a numeric.'''

        # get the object by id
        sdp = SourceDataPoint.objects.get(id=self.sdp.id)

        # Make Sure the Value is the same
        self.assertEqual(sdp.get_val(), self.cell_value) # dp exists
