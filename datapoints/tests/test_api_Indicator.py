from tastypie.test import ResourceTestCase
from django.contrib.auth.models import User

from datapoints.models import Indicator, IndicatorTag, \
    CalculatedIndicatorComponent,IndicatorToTag


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

    def test_create_calculation(self):
        Indicator.objects.create(short_name='Test Indicator 1', \
                                 name='Test Indicator for the Tag 1', \
                                 description='Test Indicator for the Tag 1 Description', )

        Indicator.objects.create(short_name='Test Indicator 2', \
                                 name='Test Indicator for the Tag 2', \
                                 description='Test Indicator for the Tag 2 Description', )

        list = Indicator.objects.all().order_by('-id')

        indicator_1 = list[0]
        indicator_2 = list[1]

        CalculatedIndicatorComponent.objects.filter(indicator_id=indicator_1.id,
                                                    indicator_component_id=indicator_2.id).delete()

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

    def test_remove_calculation(self):
        Indicator.objects.create(short_name='Test Indicator 1', \
                                 name='Test Indicator for the Tag 1', \
                                 description='Test Indicator for the Tag 1 Description', )
        Indicator.objects.create(short_name='Test Indicator 2', \
                                 name='Test Indicator for the Tag 2', \
                                 description='Test Indicator for the Tag 2 Description', )

        list = Indicator.objects.all().order_by('-id')

        indicator_1 = list[0]
        indicator_2 = list[1]

        CalculatedIndicatorComponent.objects.all().delete()

        component = CalculatedIndicatorComponent.objects.create(indicator_id=indicator_1.id,
                                                    indicator_component_id=indicator_2.id,
                                                    calculation = 'test calculation')

        self.assertEqual(CalculatedIndicatorComponent.objects.count(), 1)

        delete_url = '/api/v1/indicator_calculation/?id=' + str(component.id)

        self.api_client.delete(delete_url, format='json', data={}, authentication=self.get_credentials())

        self.assertEqual(CalculatedIndicatorComponent.objects.count(), 0)


    def test_create_tag(self):
        Indicator.objects.create(short_name='Test Indicator', \
                                 name='Test Indicator for the Tag', \
                                 description='Test Indicator for the Tag Description', )
        indicatior = Indicator.objects.all().order_by('-id')[0]

        IndicatorTag.objects.create(tag_name='Test tag')
        tag = IndicatorTag.objects.all().order_by('-id')[0]

        IndicatorToTag.objects.filter(indicator_id=indicatior.id, indicator_tag_id=tag.id).delete()

        post_data = {'indicator_id': indicatior.id, 'indicator_tag_id': tag.id}

        resp = self.api_client.post('/api/v1/indicator_to_tag/', format='json', \
                                    data=post_data, authentication=self.get_credentials())

        response_data = self.deserialize(resp)
        indicator_tag = IndicatorToTag.objects.all().order_by('-id')[0]

        self.assertHttpCreated(resp)
        self.assertEqual(indicator_tag.id, response_data['id'])
        self.assertEqual(indicatior.id, response_data['indicator_id'])
        self.assertEqual(tag.id, response_data['indicator_tag_id'])

    def test_remove_tag(self):
        indicatior = Indicator.objects.create(short_name='Test Indicator', \
                                              name='Test Indicator for the Tag', \
                                              description='Test Indicator for the Tag Description', )

        tag = IndicatorTag.objects.create(tag_name='Test tag')

        IndicatorToTag.objects.all().delete()

        indicatior_tag = IndicatorToTag.objects.create(indicator_id=indicatior.id, indicator_tag_id=tag.id)

        self.assertEqual(IndicatorToTag.objects.count(), 1)

        delete_url = '/api/v1/indicator_to_tag/?id=' + str(indicatior_tag.id)

        self.api_client.delete(delete_url, format='json', data={}, authentication=self.get_credentials())

        self.assertEqual(IndicatorToTag.objects.count(), 0)


    def test_create_indicator(self):
        Indicator.objects.all().delete()

        self.assertEqual(Indicator.objects.count(), 0)

        post_data = {'name': 'New test indicator name', \
            'short_name': 'New test short name', \
            'id': -1,'description':'test'}

        resp = self.api_client.post('/api/v1/basic_indicator/', format='json', \
                                    data=post_data, authentication=self.get_credentials())

        self.assertEqual(Indicator.objects.count(), 1)
