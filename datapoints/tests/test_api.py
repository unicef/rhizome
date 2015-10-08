from django.test import TestCase
from tastypie.test import ResourceTestCase
from tastypie.models import ApiKey
from django.contrib.auth.models import User

from datapoints.models import Indicator,CustomDashboard,CustomChart
from source_data.models import Document

from tastypie.test import TestApiClient
import json

class IndicatorResourceTest(ResourceTestCase):

    def setUp(self):
        super(IndicatorResourceTest, self).setUp()

        # Create a user.
        self.username = 'john'
        self.password = 'pass'
        self.user = User.objects.create_user(self.username,
            'john@john.com', self.password)

        self.get_credentials()

        # create their api_key

    def get_credentials(self):

        result = self.api_client.client.login(username=self.username,
                                              password=self.password)
        return result

    def test_auth_valid(self):

        resp = self.api_client.get('/api/v1/', format='json')
        self.assertValidJSONResponse(resp)

    def test_dashboard_post(self):

        post_data = {'title':'this is the title'}

        resp = self.api_client.post('/api/v1/custom_dashboard/', format='json',\
            data=post_data,authentication=self.get_credentials())

        response_data = self.deserialize(resp)

        self.assertHttpCreated(resp)
        self.assertEqual(post_data['title'],response_data['title'])

    def test_chart_create(self):

        dash = CustomDashboard.objects.create(title='test',owner_id = self.user.id)

        post_data = {'dashboard_id':dash.id,'chart_json':{'foo':'bar'}}

        resp = self.api_client.post('/api/v1/custom_chart/', format='json',\
            data=post_data,authentication=self.get_credentials())

        response_data = self.deserialize(resp)

        self.assertHttpCreated(resp)
        self.assertEqual(post_data['dashboard_id'], response_data['dashboard_id'])
        self.assertEqual(post_data['chart_json'], response_data['chart_json'])
