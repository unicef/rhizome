from tastypie.test import ResourceTestCase
from django.contrib.auth.models import User
from datapoints.models import CustomDashboard, CustomChart, LocationPermission,\
 Location, LocationType, Office

import json

class ChartResourceTest(ResourceTestCase):
    def setUp(self):
        super(ChartResourceTest, self).setUp()

        # Create a user.
        self.username = 'john'
        self.password = 'pass'
        self.user = User.objects.create_user(self.username,
                                             'john@john.com', self.password)
        self.lt = LocationType.objects.create(name='test',admin_level = 0)
        self.o = Office.objects.create(name = 'Earth')

        self.top_lvl_location = Location.objects.create(
                name = 'Nigeria',
                location_code = 'Nigeria',
                location_type_id = self.lt.id,
                office_id = self.o.id,
            )

        LocationPermission.objects.create(user_id = self.user.id,\
            top_lvl_location_id = self.top_lvl_location.id)

        self.get_credentials()

        # create their api_key

    def get_credentials(self):
        result = self.api_client.client.login(username=self.username,
                                              password=self.password)
        return result

    def test_chart_create(self):
        dash = CustomDashboard.objects.create(title='test', owner_id=self.user.id)

        post_data = {'chart_json': json.dumps({'foo': 'bar'})}

        resp = self.api_client.post('/api/v1/custom_chart/', format='json', \
                                    data=post_data, authentication=self.get_credentials())

        response_data = self.deserialize(resp)

        self.assertHttpCreated(resp)
        # self.assertEqual(post_data['chart_json'], json.loads(response_data['chart_json']))

    def test_chart_delete(self):

        c1 = CustomChart.objects.create(chart_json={'hello': 'world'})
        c2 = CustomChart.objects.create(chart_json={'goodnight': 'moon'})

        delete_url = '/api/v1/custom_chart/?id=' + str(c1.id)

        self.api_client.delete(delete_url, format='json', data={},
                               authentication=self.get_credentials())

        self.assertEqual(CustomChart.objects.count(), 1)
