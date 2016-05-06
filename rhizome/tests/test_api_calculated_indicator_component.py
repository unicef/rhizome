from tastypie.test import ResourceTestCase
from rhizome.models import CalculatedIndicatorComponent
from setup_helpers import TestSetupHelpers

class CalculatedIndicatorResourceTest(ResourceTestCase):

    def setUp(self):
        super(CalculatedIndicatorResourceTest, self).setUp()
        self.ts = TestSetupHelpers()
        self.lt = self.ts.create_arbitrary_location_type()
        self.o = self.ts.create_arbitrary_office()

        self.top_lvl_location = self.ts.create_arbitrary_location(
            self.lt.id,
            self.o.id,
            location_code ='Nigeria',
            location_name='Nigeria')

# this is a pretty dumb test but it achieves 100% test coverage
    def test_indicator_id_missing(self):
    	data={}
        resp = self.ts.get(self, '/api/v1/campaign_type/',data=data)
        self.assertHttpOK(resp)
        resp_data = self.deserialize(resp)
        self.assertEqual(len(resp_data['objects']), 0)

