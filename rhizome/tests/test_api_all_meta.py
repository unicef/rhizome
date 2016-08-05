from rhizome.tests.base_test_case import RhizomeApiTestCase

from rhizome.models.office_models import Office
from rhizome.models.location_models import Location, LocationType, \
    LocationPermission
from rhizome.models.datapoint_models import CacheJob
from rhizome.models.dashboard_models import CustomDashboard, CustomChart



from rhizome.tests.setup_helpers import TestSetupHelpers
import json
from django.test import TestCase


class AllMetaResourceTest(RhizomeApiTestCase):
        # ./manage.py test rhizome.tests.test_api_all_meta.AllMetaResourceTest --settings=rhizome.settings.test

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

    def test_all_meta_location_json(self):

        resp = self.ts.get(self, '/api/v1/all_meta/')
        self.assertHttpOK(resp)
        response_data = self.deserialize(resp)
        location_data = response_data['objects'][0]['locations']
        self.assertEqual(type(location_data), list)
