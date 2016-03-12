from django.test import TestCase
from tastypie.test import ResourceTestCase
from tastypie.models import ApiKey
from django.contrib.auth.models import User
from rhizome.models import CacheJob, Office, Indicator, Location,\
    LocationType, DataPointComputed, CampaignType, Campaign, IndicatorTag,\
    LocationPermission, Document

from rhizome.cache_meta import LocationTreeCache

class DataPointResourceTest(ResourceTestCase):
    def setUp(self):
        super(DataPointResourceTest, self).setUp()

        # Create a user.
        self.username = 'john'
        self.password = 'pass'
        self.user = User.objects.create_user(self.username,\
                                        'eradicate@polio.com', self.password)

        self.lt = LocationType.objects.create(name='Country',admin_level = 0)
        self.o = Office.objects.create(name = 'Earth')

        self.top_lvl_location = Location.objects.create(
                name = 'Nigeria',
                location_code = 'Nigeria',
                location_type_id = self.lt.id,
                office_id = self.o.id,
            )

        ltc = LocationTreeCache()
        ltc.main()

        LocationPermission.objects.create(user_id = self.user.id,\
            top_lvl_location_id = self.top_lvl_location.id)

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

        ind_tag = IndicatorTag.objects.create(tag_name='Polio')

        # 2. Create The Indicator value
        indicator = Indicator.objects.create(short_name='Number of vaccine doses used in HRD', \
                                             name='Number of vaccine doses used in HRD', \
                                             is_reported=0, \
                                             description='Number of vaccine doses used in HRD', )

        # 3. Create The Location
        office = Office.objects.create(name='Nigeria')
        location = self.top_lvl_location

        # 4. Create The Campaign
        start_date = '2016-01-01'
        end_date = '2016-01-01'
        campaign_type = CampaignType.objects\
            .create(name='National Immunization Days (NID)')
        campaign = Campaign.objects.create(office=office,\
            campaign_type=campaign_type,start_date=start_date,end_date=end_date,\
            top_lvl_indicator_tag_id = ind_tag.id,\
            top_lvl_location_id = location.id)

        # 5. Create Test DataPointComputed
        value = 1.57
        document = Document.objects.create(doc_title='I am Every Woman -- Whitney Houston')
        datapoint = DataPointComputed.objects.create(value=value,\
            cache_job=cache_job,indicator=indicator, location=location,\
            campaign=campaign, document=document)

        # 6 Request To The API
        get_parameter = 'indicator__in={0}&campaign_start={1}&campaign_end={2}&parent_location_id__in={3}'\
            .format(indicator.id, start_date,end_date, location.id)

        resp = self.api_client.get('/api/v1/datapoint/?' + get_parameter, \
            format='json', authentication=self.get_credentials())

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
