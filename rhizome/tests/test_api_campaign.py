from tastypie.test import ResourceTestCase
from django.contrib.auth.models import User
from rhizome.models import Office, LocationType, Location, \
    LocationPermission, Campaign, CampaignType, IndicatorTag
from rhizome.cache_meta import LocationTreeCache


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
            top_lvl_indicator_tag_id = self.it.id,
            name="can_see"
        )

        self.can_see_campaign_2 = Campaign.objects.create(
            start_date = '2016-01-04',
            end_date = '2016-01-09',
            office_id = self.o.id,
            campaign_type_id = self.ct.id,
            top_lvl_location_id = self.top_lvl_location.id,
            top_lvl_indicator_tag_id = self.it.id,
            name="can_see_2"
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

    #GET request: if there are no parameters, return all campaigns.
    #if id__in is set, returns a list of campaigns. and 200 code
    def test_campaign_get(self):

        resp = self.api_client.get('/api/v1/campaign/', format='json', \
                                    authentication=self.get_credentials())
        self.assertHttpOK(resp)
        response_data = self.deserialize(resp)
        self.assertEqual(len(response_data['objects']), 2)

    def test_campaign_get_id_list(self):
        campaign_id_list = [self.can_see_campaign.id, self.can_see_campaign_2.id]
        data = {'id__in':str(campaign_id_list).strip('[]')}
        resp = self.api_client.get('/api/v1/campaign/', format='json', \
                                    data=data, authentication=self.get_credentials())
        response_data = self.deserialize(resp)
        self.assertHttpOK(resp)
        self.assertEqual(len(response_data['objects']), 2)

    #if id__in contains an invalid id, returns 200 with an empty list
    def test_campaign_get_id_list_invalid(self):
        data = {'id__in':12345}
        resp = self.api_client.get('/api/v1/campaign/', format='json', \
                                    data=data, authentication=self.get_credentials())
        response_data = self.deserialize(resp)
        self.assertHttpOK(resp)
        self.assertEqual(len(response_data['objects']), 0)

    def test_get_detail(self):
        detailURL = '/api/v1/campaign/{0}/'.format(self.can_see_campaign.id)
        resp=self.api_client.get(detailURL, format='json', \
                                    authentication=self.get_credentials())
        self.assertHttpOK(resp)
        response_data = self.deserialize(resp)
        self.assertEqual(self.can_see_campaign.name, response_data['name'])

    #if an id is invalid for get_detail, 500 response
    def test_get_detail_invalid_id(self):
        detailURL = '/api/v1/campaign/12345/'
        resp=self.api_client.get(detailURL, format='json', \
                                    authentication=self.get_credentials())
        self.assertHttpApplicationError(resp)

    #POST request requires fields: 'name','top_lvl_location_id',
    #'top_lvl_indicator_tag_id', 'office_id','campaign_type_id',
    #'start_date','end_date','pct_complete'
    #Returns 201 
    def test_post_campaign(self):
        data={
            'name': 'something',
            'top_lvl_location_id': self.top_lvl_location.id,
            'top_lvl_indicator_tag_id': self.it.id,
            'office_id': self.o.id,
            'campaign_type_id': self.ct.id,
            'start_date': '2016-05-01',
            'end_date': '2016-05-01',
            'pct_complete': 0.1
        }
        resp = self.api_client.post('/api/v1/campaign/', format='json', \
                                    data=data, authentication=self.get_credentials())
        response_data = self.deserialize(resp)
        self.assertHttpCreated(resp)
        self.assertEqual(response_data['name'], 'something')

    #if any of the fields are missing, returns a 500 error
    def test_post_campaign_invalid(self):
        data={
            'top_lvl_indicator_tag_id': self.it.id,
            'office_id': self.o.id,
            'campaign_type_id': self.ct.id,
            'start_date': '2016-05-01',
            'end_date': '2016-05-01',
            'pct_complete': 0.1
        }
        resp = self.api_client.post('/api/v1/campaign/', format='json', \
                                    data=data, authentication=self.get_credentials())
        self.assertHttpApplicationError(resp)


