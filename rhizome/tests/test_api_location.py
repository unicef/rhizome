from tastypie.test import ResourceTestCase
from django.contrib.auth.models import User
from rhizome.models import Office, LocationType, Location, LocationPermission

from rhizome.cache_meta import LocationTreeCache


class LocationResourceTest(ResourceTestCase):
    def setUp(self):

        ## instantiate the test client and all other methods ##
        super(LocationResourceTest, self).setUp()

        # Create a user.
        self.username = 'test_user'
        self.password = 'test_password'
        self.user = User.objects\
            .create_user(self.username,'test@test.com', self.password)
        self.lt = LocationType.objects.create(name='test',admin_level = 0)
        self.o = Office.objects.create(name = 'Earth')
        self.not_allowed_to_see_location = Location.objects.create(
                name = 'Somalia',
                location_code = 'Somalia',
                location_type_id = self.lt.id,
                office_id = self.o.id,
            )
        self.top_lvl_location = Location.objects.create(
                name = 'Nigeria',
                location_code = 'Nigeria',
                location_type_id = self.lt.id,
                office_id = self.o.id,
            )

        self.sub_location = Location.objects.create(
                name = 'Kano',
                location_code = 'Kano',
                location_type_id = self.lt.id,
                office_id = self.o.id,
                parent_location_id = self.top_lvl_location.id
            )

        ### set the user permission ###
        LocationPermission.objects.create(user_id = self.user.id,\
            top_lvl_location_id = self.top_lvl_location.id)

        self.get_credentials()

        ltr = LocationTreeCache()
        ltr.main()

    def get_credentials(self):
        result = self.api_client.client.login(username=self.username,
                                              password=self.password)
        return result

    def test_get_location_no_param(self):

        resp = self.api_client.get('/api/v1/location/', format='json', \
                                    authentication=self.get_credentials())

        response_data = self.deserialize(resp)
        self.assertHttpOK(resp)

        self.assertEqual(self.top_lvl_location.id,\
            response_data['meta']['top_lvl_location_id'])

        # https://trello.com/c/3kxd6hCc/1134-bring-back-ability-to-filter-locations-based-on-user-peromissions
        # self.assertEqual(len(response_data['objects']), 2)
        self.assertEqual(len(response_data['objects']), len(Location.objects.all()))

        # self.assertNotEqual(IndicatorTag.objects.all()[0].id, -1)
