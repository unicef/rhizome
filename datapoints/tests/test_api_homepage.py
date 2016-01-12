import json

from tastypie.test import ResourceTestCase
from django.contrib.auth.models import User

from datapoints.models import Indicator, IndicatorTag, \
    CalculatedIndicatorComponent,IndicatorToTag, IndicatorBound, \
    LocationPermission, Location, LocationType, Office, Campaign

# python manage.py test datapoints.tests.test_api_homepage --settings=rhizome.settings.test
class IndicatorResourceTest(ResourceTestCase):
    def setUp(self):
        super(IndicatorResourceTest, self).setUp()


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

        self.it = IndicatorTag.objects.create(tag_name = 'Ebola')

        self.campaign = Campaign.objects.create(
            id = 299,
            start_date = '2016-01-01',
            end_date = '2016-01-01',
            office_id = self.o.id,
            top_lvl_location_id = self.top_lvl_location.id,
            top_lvl_indicator_tag_id = self.it.id,
            campaign_type_id = 1
        )

        LocationPermission.objects.create(user_id = self.user.id,\
            top_lvl_location_id = self.top_lvl_location.id)

        self.get_credentials()

    def get_credentials(self):
        result = self.api_client.client.login(username=self.username,
                                              password=self.password)
        return result

    # def test_get_homepage(self):
    #
    #     resp = self.api_client.get('/api/v1/homepage/', format='json'\
    #         , data={}, authentication=self.get_credentials())
    #
    #     response_data = self.deserialize(resp)
    #     chart_objects = response_data['objects']
    #
    #     # self.assertEqual(3,len(chart_objects))
    #     self.assertValidJSONResponse(resp)
