from base_test_case import RhizomeAPITestCase
from rhizome.models import CustomDashboard, CustomChart, LocationPermission,\
    Location, LocationType, Office
from setup_helpers import TestSetupHelpers
import json
from django.test import TestCase


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

    def test_all_meta_json(self):
        resp = self.ts.get(self, '/api/v1/all_meta/')
        self.assertHttpOK(resp)
        response_data = self.deserialize(resp)
        for obj_key, obj_list in response_data['objects'][0].iteritems():
            if obj_key != 'is_superuser':
                try:
                    json_obj = json.loads(obj_list)
                except:
                    print "expected json object, got a %s for obj:" %str(type(obj_list))
                    print obj_list
                    self.assertTrue(False)
        self.assertTrue(True)
