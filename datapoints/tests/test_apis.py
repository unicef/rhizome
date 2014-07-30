import datetime
from tastypie.test import ResourceTestCase
from datapoints.models import Indicator
from django.contrib.auth.models import User
from tastypie.models import ApiKey

import pprint as pp

# http://django-tastypie.readthedocs.org/en/latest/testing.html

class IndicatorResourceTest(ResourceTestCase):
    # Use ``fixtures`` & ``urls`` as normal. See Django's ``TestCase``
    # documentation for the gory details.
    # fixtures = ['test_indicators.json']

    ## ^ not sure what this means ^ ##

    def setUp(self):
        super(IndicatorResourceTest, self).setUp()

        # Create a user.
        self.username = 'john'
        self.password = 'pas'
        self.user = User.objects.create_user(self.username,
            'john@john.com', self.password)

        # create their api_key
        self.api_key = ApiKey.objects.create(user=self.user)


        # first create an indicator
        Indicator.objects.create(name='First Indicator',
            description='First Indicator Description')

        # Fetch the ``Datapoint`` object we'll use in testing.
        # Note that we aren't using PKs because they can change depending
        # on what other tests are running.
        self.indicator_1 = Indicator.objects.get(slug='first-indicator')

        # We also build a detail URI, since we will be using it all over.
        # DRY, baby. DRY.
        self.detail_url = '/api/v1/indicator/{0}/'.format(self.indicator_1.pk)

        # The data we'll send on POST requests. Again, because we'll use it
        # frequently (enough).
        self.post_data = {
            'description': 'Second Indicator Description',
            'name': 'Second Indicator',
            'slug': 'second-indicator',
            'created': '2012-05-01T22:05:12'
        }

    def get_credentials(self):
        return self.create_basic(username=self.username, password=self.password)

    def test_get_list_unauthorzied(self):
        self.assertHttpUnauthorized(self.api_client.get('/api/v1/indicator/',
            format='json'))

    def test_get_list_json(self):
        resp = self.api_client.get('/api/v1/indicator/', format='json',
            usernmae='john',api_key=self.api_key,
            authentication=self.get_credentials())

        # x = resp.__dict__
        # pp.pprint(x)

        self.assertValidJSONResponse(resp)

        # Scope out the data for correctness.
        ## IN THE DOCS THE ASSERTION HAD 12... dunno why that was but i expect 1
        self.assertEqual(len(self.deserialize(resp)['objects']), 1)

        # Here, we're checking an entire structure for the expected data.
        self.assertEqual(self.deserialize(resp)['objects'][0]['name'],
        'First Indicator')
        # {
        #     'pk': str(self.indicator_1.pk),
        #     'name': 'First Indicator',
        #     'slug': 'first-indicator',
        #     'created': '2012-05-01T19:13:42',
        #     'resource_uri': '/api/v1/indicator/{0}/'.format(self.indicator_1.pk)
        # })

### RUN THIS BY USING THE FOLLOWING COMMAND ###
# coverage run manage.py test datapoints.api  --settings=polio.settings_test
