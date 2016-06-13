from base_test_case import RhizomeApiTestCase
from rhizome.models import LocationPermission
from setup_helpers import TestSetupHelpers


class LocationPermissionResourceTest(RhizomeApiTestCase):

    def setUp(self):
        super(LocationPermissionResourceTest, self).setUp()

        self.ts = TestSetupHelpers()
        self.lt = self.ts.create_arbitrary_location_type()
        self.o = self.ts.create_arbitrary_office()
        self.top_lvl_location = self.ts.create_arbitrary_location(
            self.lt.id,
            self.o.id,
            location_code='Nigeria',
            location_name='Nigeria')

    def test_get_location_permission(self):
        lp = LocationPermission.objects.create(user_id=self.ts.user.id,
                                               top_lvl_location_id=self.top_lvl_location.id)

        data = {
            'user_id': self.ts.user.id
        }

        resp = self.ts.get(self, '/api/v1/location_responsibility/', data=data)
        response_data = self.deserialize(resp)
        self.assertHttpOK(resp)
        self.assertEqual(response_data['objects'][0]['id'], lp.id)

    def test_get_location_permission_no_id(self):
        resp = self.ts.get(self, '/api/v1/location_responsibility/')
        self.assertHttpApplicationError(resp)

    def test_create_location_permission(self):
        data = {
            'location_id': self.top_lvl_location.id,
            'user_id': self.ts.user.id
        }

        resp = self.ts.post(
            self, '/api/v1/location_responsibility/', data=data)

        response_data = self.deserialize(resp)
        self.assertHttpCreated(resp)
        self.assertEqual(response_data['user_id'], self.ts.user.id)
        self.assertEqual(
            response_data['location_id'], self.top_lvl_location.id)

    def test_create_location_permission_missing_id(self):
        data = {
            'user_id': self.ts.user.id
        }

        resp = self.ts.post(
            self, '/api/v1/location_responsibility/', data=data)
        self.assertHttpApplicationError(resp)

    def test_update_location_permission(self):
        lp = LocationPermission.objects.create(user_id=self.ts.user.id,
                                               top_lvl_location_id=self.top_lvl_location.id)

        # update the location
        new_location = self.ts.create_arbitrary_location(
            self.lt.id,
            self.o.id,
            location_code='Kenya',
            location_name='Kenya'
        )
        data = {
            'location_id': new_location.id,
            'user_id': self.ts.user.id
        }
        resp = self.ts.post(
            self, '/api/v1/location_responsibility/', data=data)
        response_data = self.deserialize(resp)
        self.assertHttpCreated(resp)
        self.assertEqual(response_data['user_id'], self.ts.user.id)
        self.assertEqual(response_data['location_id'], new_location.id)
