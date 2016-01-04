from tastypie.test import ResourceTestCase
from django.contrib.auth.models import User
from datapoints.models import Office, LocationType, Location, \
    LocationPermission, Campaign, CampaignType, IndicatorTag
from datapoints.cache_meta import LocationTreeCache


class CampaignResourceTest(ResourceTestCase):
    def setUp(self):

        ## instantiate the test client and all other methods ##
        super(CampaignResourceTest, self).setUp()

        # Create a user.
        self.username = 'test_user'
        self.password = 'test_password'
        self.user = User.objects\
            .create_user(self.username,'test@test.com', self.password)
        self.lt = LocationType.objects.create(name='test',admin_level = 0)
        self.o = Office.objects.create(name = 'Earth')
        self.not_allowed_to_see_location = Location.objects.create(
                name = 'Somalia',
                location_code = 'Somalia',
                location_type_id = self.lt.id,
                office_id = self.o.id,
            )

        self.top_lvl_location = Location.objects.create(
                name = 'Nigeria',
                location_code = 'Nigeria',
                location_type_id = self.lt.id,
                office_id = self.o.id,
            )

        self.sub_location = Location.objects.create(
                name = 'Kano',
                location_code = 'Kano',
                location_type_id = self.lt.id,
                office_id = self.o.id,
                parent_location_id = self.top_lvl_location.id
            )
        self.it = IndicatorTag.objects.create(tag_name='Polio')

        self.ct = CampaignType.objects.create(name='NID')
        self.can_see_campaign = Campaign.objects.create(
            start_date = '2016-01-01',
            end_date = '2016-01-01',
            office_id = self.o.id,
            campaign_type_id = self.ct.id,
            top_lvl_location_id = self.top_lvl_location.id,
            top_lvl_indicator_tag_id = self.it.id
        )

        self.can_not_see_campaign = Campaign.objects.create(
            start_date = '2016-02-01',
            end_date = '2016-02-01',
            office_id = self.o.id,
            campaign_type_id = self.ct.id,
            top_lvl_location_id = self.not_allowed_to_see_location.id,
            top_lvl_indicator_tag_id = self.it.id
        )

        ### set the user permission ###
        LocationPermission.objects.create(user_id = self.user.id,\
            top_lvl_location_id = self.top_lvl_location.id)

        self.get_credentials()

        ltr = LocationTreeCache()
        ltr.main()

    def get_credentials(self):
        result = self.api_client.client.login(username=self.username,
                                              password=self.password)
        return result

    def test_get_campaign_no_param(self):

        resp = self.api_client.get('/api/v1/campaign/', format='json', \
                                    authentication=self.get_credentials())
        self.assertHttpOK(resp)

        response_data = self.deserialize(resp)

        self.assertEqual(len(response_data['objects']), 1)
