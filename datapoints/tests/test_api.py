from django.test import TestCase
from tastypie.test import ResourceTestCase
from tastypie.models import ApiKey
from django.contrib.auth.models import User

from datapoints.models import Indicator
from source_data.models import Document


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

        # # create create an indicator
        self.indicator = Indicator.objects.create(name='First Indicator',
            description='First Indicator Description')

    def get_credentials(self):

        result = self.api_client.client.login(username=self.username,
                                              password=self.password)
        return result

    def test_indicator_get(self):

        resp = self.api_client.get('/api/v1/indicator/', format='json')
        self.assertValidJSONResponse(resp)
