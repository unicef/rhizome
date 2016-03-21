from django.test import TestCase
from tastypie.test import ResourceTestCase
from tastypie.models import ApiKey
from django.contrib.auth.models import User
from rhizome.models import CacheJob, Office, Indicator, Location,\
    LocationType, DataPointComputed, CampaignType, Campaign, IndicatorTag,\
    LocationPermission, Document
from setup_helpers import TestSetupHelpers

from rhizome.cache_meta import LocationTreeCache

class DocumentResourceTest(ResourceTestCase):
    def setUp(self):
        super(DocumentResourceTest, self).setUp()
        self.ts = TestSetupHelpers();
        self.lt = self.ts.create_arbitrary_location_type()
        self.o = self.ts.create_arbitrary_office()
        self.top_lvl_location = self.ts.create_arbitrary_location(self.lt.id, self.o.id)
        LocationPermission.objects.create(user_id = self.ts.user.id,\
            top_lvl_location_id = self.top_lvl_location.id)
        # self.doc = self.ts.create_arbitrary_document();


  #TODO write a test to check file upload.. need to pass file as POST obj
  #   def test_obj_create(self):
		# post_data = {'docfile':'eoc_post_campaign.csv', 'doc_title': 'eoc_post_campaign.csv'}
		# resp = self.ts.post(self, '/api/v1/source_doc/', post_data)
		# resp_data = self.deserialize(resp)
		# print(resp_data)
		# self.assertHttpOK(resp)
