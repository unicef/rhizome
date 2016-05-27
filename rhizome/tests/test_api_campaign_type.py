from base_test_case import RhizomeAPITestCase
from rhizome.models import CampaignType
from setup_helpers import TestSetupHelpers

class CampaignTypeResourceTest(RhizomeAPITestCase):

    def setUp(self):
        super(CampaignTypeResourceTest, self).setUp()
        self.ts = TestSetupHelpers()
        self.lt = self.ts.create_arbitrary_location_type()
        self.o = self.ts.create_arbitrary_office()

        self.top_lvl_location = self.ts.create_arbitrary_location(
            self.lt.id,
            self.o.id,
            location_code ='Nigeria',
            location_name='Nigeria')


    def test_get_campaign_type(self):
    	CampaignType.objects.create(name="test")
        resp = self.ts.get(self, '/api/v1/campaign_type/')
        self.assertHttpOK(resp)
        resp_data = self.deserialize(resp)
        self.assertEqual(resp_data['objects'][0]['name'], 'test')
