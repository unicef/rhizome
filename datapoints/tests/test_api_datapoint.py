from django.test import TestCase
from tastypie.test import ResourceTestCase
from tastypie.models import ApiKey
from django.contrib.auth.models import User
from datapoints.models import CacheJob, Office, Indicator, Location, LocationType, \
    DataPointComputed, CampaignType, Campaign

class DataPointResourceTest(ResourceTestCase):
    def setUp(self):
        super(DataPointResourceTest, self).setUp()

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

    def test_get_list(self):
        # Create the data, need input value to the DataPointComputed model.
        # 1. The CacheJob value
        cache_job = CacheJob.objects.create(
            is_error=False,
            response_msg='SUCCESS'
        )

        # 2. Create The Indicator value
        indicator = Indicator.objects.create(short_name='Number of vaccine doses used in HRD', \
                                             name='Number of vaccine doses used in HRD', \
                                             is_reported=0, \
                                             description='Number of vaccine doses used in HRD', )

        # 3. Create The Location
        office = Office.objects.create(name='Nigeria')
        location_type = LocationType.objects.create(name='Country', admin_level=0)
        location = Location.objects.create(name='Nigeria' \
                                           , office=office
                                           , location_type=location_type)

        # 4. Create The Campaign
        start_date = '2014-01-01'
        end_date = '2014-01-01'
        campaign_type = CampaignType.objects.create(name='National Immunization Days (NID)')
        campaign = Campaign.objects.create(office=office, campaign_type=campaign_type, \
                                           start_date=start_date, end_date=end_date)

        # 5. Create Test DataPointComputed
        value = 1.57
        datapoint = DataPointComputed.objects.create(value=value, cache_job=cache_job, indicator=indicator, \
                                                     location=location, campaign=campaign)

        # 6 Request To The API
        get_parameter = 'indicator__in={0}&campaign_start={1}&campaign_end={2}&parent_location__in={3}'.format( \
            indicator.id, start_date, end_date, location.id)

        resp = self.api_client.get('/api/v1/datapoint/?' + get_parameter, format='json', \
                                   authentication=self.get_credentials())

        # print resp
        # print '/api/v1/datapoint/?' + get_parameter

        self.assertHttpOK(resp)
        response_data = self.deserialize(resp)

        # print(response_data)
        self.assertEqual(response_data['error'], None)
        self.assertEqual(response_data['meta']["total_count"], 1)

        self.assertEqual(len(response_data['objects']), 1)

        self.assertEqual(response_data['objects'][0]['campaign'], campaign.id)
        self.assertEqual(response_data['objects'][0]['location'], location.id)
        self.assertEqual(len(response_data['objects'][0]['indicators']), 1)
        self.assertEqual(int(response_data['objects'][0]['indicators'][0]['indicator']), indicator.id)
        self.assertEqual(response_data['objects'][0]['indicators'][0]['value'], value)
