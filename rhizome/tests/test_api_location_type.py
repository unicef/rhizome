from rhizome.tests.base_test_case import RhizomeApiTestCase
from rhizome.tests.setup_helpers import TestSetupHelpers
from rhizome.models.location_models import LocationType


class LocationTypeResourceTest(RhizomeApiTestCase):

    def setUp(self):

        ## instantiate the test client and all other methods ##
        super(LocationTypeResourceTest, self).setUp()

        self.ts = TestSetupHelpers()
        self.lt = self.ts.create_arbitrary_location_type()
        self.o = self.ts.create_arbitrary_office()
        self.top_lvl_location = self.ts.create_arbitrary_location(
            self.lt.id,
            self.o.id,
            location_code='Nigeria',
            location_name='Nigeria')

    def test_location_type(self):
        lt = LocationType.objects.create(name="lt", admin_level=1)
        lt_2 = LocationType.objects.create(name="lt2", admin_level=2)
        url = '/api/v1/location_type/'
        resp = self.ts.get(self, url)
        response_data = self.deserialize(resp)
        self.assertHttpOK(resp)
        # the two we just created, plus one created in setup
        self.assertEqual(len(response_data['objects']), 3)
