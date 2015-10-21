from django.test import TestCase
from tastypie.test import ResourceTestCase
from tastypie.models import ApiKey
from django.contrib.auth.models import User

from datapoints.models import Indicator, IndicatorTag, CustomDashboard, CustomChart, CalculatedIndicatorComponent, \
    IndicatorToTag
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
        post_data = {'title': 'this is the title'}

        resp = self.api_client.post('/api/v1/custom_dashboard/', format='json', \
                                    data=post_data, authentication=self.get_credentials())

        response_data = self.deserialize(resp)

        self.assertHttpCreated(resp)
        self.assertEqual(post_data['title'], response_data['title'])

    def test_chart_create(self):
        dash = CustomDashboard.objects.create(title='test', owner_id=self.user.id)

        post_data = {'dashboard_id': dash.id, 'chart_json': json.dumps({'foo': 'bar'})}

        resp = self.api_client.post('/api/v1/custom_chart/', format='json', \
                                    data=post_data, authentication=self.get_credentials())

        response_data = self.deserialize(resp)

        self.assertHttpCreated(resp)
        self.assertEqual(post_data['dashboard_id'], response_data['dashboard_id'])
        self.assertEqual(post_data['chart_json'], response_data['chart_json'])

    # def test_chart_delete(self):
    #     d = CustomDashboard.objects.create(owner_id = self.user.id,title='test')
    #     c1 = CustomChart.objects.create(dashboard_id = d.id,chart_json={'hello':'world'})
    #     c2 = CustomChart.objects.create(dashboard_id = d.id,chart_json={'goodnight':'moon'})
    #
    #     delete_url = '/api/v1/custom_chart/'
    #     params = {'id':c1.id}
    #
    #
    #     self.api_client.delete(delete_url,format='json',data=params,
    #         authentication=self.get_credentials())
    #
    #     self.assertEqual(CustomChart.objects.count(), 1)

    def test_create_calculation(self):

        Indicator.objects.create(short_name='Test Indicator 1',\
                                 name= 'Test Indicator for the Tag 1',\
                                 description = 'Test Indicator for the Tag 1 Description',)

        Indicator.objects.create(short_name='Test Indicator 2',\
                                 name= 'Test Indicator for the Tag 2',\
                                 description = 'Test Indicator for the Tag 2 Description',)

        list = Indicator.objects.all().order_by('-id')

        indicator_1 = list[0]
        indicator_2 = list[1]

        CalculatedIndicatorComponent.objects.filter(indicator_id=indicator_1.id, indicator_component_id=indicator_2.id).delete()

        post_data = {'indicator_id': indicator_1.id, 'component_id': indicator_2.id, 'typeInfo': 'WHOLE'}

        resp = self.api_client.post('/api/v1/indicator_calculation/', format='json', \
                                    data=post_data, authentication=self.get_credentials())

        response_data = self.deserialize(resp)
        indicator_calculation = CalculatedIndicatorComponent.objects.all().order_by('-id')[0]

        self.assertHttpCreated(resp)
        self.assertEqual(indicator_calculation.id, response_data['id'])
        self.assertEqual(indicator_1.id, response_data['indicator_id'])
        self.assertEqual(indicator_2.id, response_data['component_id'])
        self.assertEqual(indicator_calculation.calculation, response_data['typeInfo'])

    def test_create_tag(self):
        Indicator.objects.create(short_name='Test Indicator',\
                                 name= 'Test Indicator for the Tag',\
                                 description = 'Test Indicator for the Tag Description',)
        indicatior = Indicator.objects.all().order_by('-id')[0]

        IndicatorTag.objects.create(tag_name = 'Test tag')
        tag = IndicatorTag.objects.all().order_by('-id')[0]

        IndicatorToTag.objects.filter(indicator_id=indicatior.id, indicator_tag_id=tag.id).delete()

        post_data = {'indicator_id': indicatior.id, 'indicator_tag_id': tag.id}

        resp = self.api_client.post('/api/v1/indicator_to_tag/', format='json', \
                                    data=post_data, authentication=self.get_credentials())

        response_data = self.deserialize(resp)
        indicator_tag = IndicatorToTag.objects.all().order_by('-id')[0]

        self.assertHttpCreated(resp)
        self.assertEqual(indicator_tag.id, response_data['id'])
        self.assertEqual(post_data['indicator_id'], response_data['indicator_id'])
        self.assertEqual(post_data['indicator_tag_id'], response_data['indicator_tag_id'])

