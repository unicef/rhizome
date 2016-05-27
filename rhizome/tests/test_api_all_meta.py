from base_test_case import RhizomeAPITestCase
from rhizome.models import CustomDashboard, CustomChart, LocationPermission,\
    Location, LocationType, Office
from setup_helpers import TestSetupHelpers


class AllMetaResourceTest(RhizomeAPITestCase):

    def setUp(self):
        super(AllMetaResourceTest, self).setUp()

        self.ts = TestSetupHelpers()
        self.lt = self.ts.create_arbitrary_location_type()
        self.o = self.ts.create_arbitrary_office()
        self.not_allowed_to_see_location = self.ts.create_arbitrary_location(
            self.lt.id,
            self.o.id)

    def test_all_meta_get(self):
        resp = self.ts.get(self, '/api/v1/all_meta/')
        self.assertHttpOK(resp)
        response_data = self.deserialize(resp)
        self.assertEqual(len(response_data['objects']), 1)
