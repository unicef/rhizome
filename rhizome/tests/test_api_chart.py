from tastypie.test import ResourceTestCase
from django.contrib.auth.models import User
from rhizome.models import CustomDashboard, CustomChart, LocationPermission,\
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
        dash = CustomDashboard.objects.create(title='test')

        post_data = {
            'uuid': 'c8eef24a-f696-11e5-9ce9-5e5517507c66',
            'title': 'Afghanistan',\
            'chart_json': json.dumps({'foo': 'bar','title':'sometitle'}
            )}

        resp = self.api_client.post('/api/v1/custom_chart/', format='json', \
                                    data=post_data,
                                    authentication=self.get_credentials())

        response_data = self.deserialize(resp)

        self.assertHttpCreated(resp)
        # self.assertEqual(post_data['chart_json'], json.loads(response_data['chart_json']))

    def test_chart_delete(self):

        c1 = CustomChart.objects.create(title='L.O.X',\
            chart_json={'hello': 'world'},
            uuid='104fdca8-f697-11e5-9ce9-5e5517507c66')
        c2 = CustomChart.objects.create(title='J to the Muah',\
            chart_json={'goodnight': 'moon'},
            uuid='2049be4e-f697-11e5-9ce9-5e5517507c66')

        delete_url = '/api/v1/custom_chart/?id=' + str(c1.id)

        self.api_client.delete(delete_url, format='json', data={},
                               authentication=self.get_credentials())

        self.assertEqual(CustomChart.objects.count(), 1)
