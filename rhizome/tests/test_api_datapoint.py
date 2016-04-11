
from django.test import TestCase
from tastypie.test import ResourceTestCase
from tastypie.models import ApiKey
from django.contrib.auth.models import User
from rhizome.models import CacheJob, Office, Indicator, Location,\
    LocationType, DataPointComputed, CampaignType, Campaign, IndicatorTag,\
    LocationPermission, Document, IndicatorClassMap

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
        get_parameter = 'indicator__in={0}&campaign_start={1}&campaign_end={2}&location_id__in={3}'\
            .format(indicator.id, start_date,end_date, location.id)

        resp = self.api_client.get('/api/v1/datapoint/?' + get_parameter, \
            format='json', authentication=self.get_credentials())

        self.assertHttpOK(resp)
        response_data = self.deserialize(resp)
        self.assertEqual(response_data['error'], None)
        self.assertEqual(response_data['meta']["total_count"], 1)

        self.assertEqual(len(response_data['objects']), 1)

        self.assertEqual(response_data['objects'][0]['campaign'], campaign.id)
        self.assertEqual(response_data['objects'][0]['location'], location.id)
        self.assertEqual(len(response_data['objects'][0]['indicators']), 1)
        self.assertEqual(int(response_data['objects'][0]['indicators'][0]['indicator']), indicator.id)
        self.assertEqual(response_data['objects'][0]['indicators'][0]['value'], value)


    def test_get_class_datapoint(self):
        cache_job = CacheJob.objects.create(
            is_error=False,
            response_msg='SUCCESS'
        )

        ind_tag = IndicatorTag.objects.create(tag_name='Polio')

        # 2. Create The Indicator value
        indicator = Indicator.objects.create(short_name='LQAS', \
                                             name='LQAS', \
                                              data_format='class',\
                                             description='LQAS', )

        # 3. Create The Location
        office = Office.objects.create(name='Nigeria')
        location = self.top_lvl_location

        # 4. Create The Campaign
        start_date = '2016-02-01'
        end_date = '2016-02-01'
        campaign_type = CampaignType.objects\
            .create(name='National Immunization Days (NID)')
        campaign = Campaign.objects.create(office=office,\
            campaign_type=campaign_type,start_date=start_date,end_date=end_date,\
            top_lvl_indicator_tag_id = ind_tag.id,\
            top_lvl_location_id = location.id)

        # 5. Create Test DataPointComputed
        value = 1
        document = Document.objects.create(doc_title='uploadddd')
        datapoint = DataPointComputed.objects.create(value=value,\
            cache_job=cache_job,indicator=indicator, location=location,\
            campaign=campaign, document=document)

        # 6 create the class indicator mapping

        mapping_1 = IndicatorClassMap.objects.create(
        indicator = indicator,
        string_value = "Fail",
        enum_value = 1,
        is_display =True)

        # 7 Request To The API
        get_parameter = 'indicator__in={0}&campaign_start={1}&campaign_end={2}&location_id__in={3}'\
            .format(indicator.id, start_date,end_date, location.id)

        resp = self.api_client.get('/api/v1/datapoint/?' + get_parameter, \
            format='json', authentication=self.get_credentials())

        self.assertHttpOK(resp)
        response_data = self.deserialize(resp)
        self.assertEqual(response_data['objects'][0]['indicators'][0]['value'], "Fail")

    def test_map_transform(self):

        indicator_id = 1
        campaign_id = 2
        parent_location_id =3
        document = Document.objects.create(doc_title='some doc')

        loc_and_value ={'Zamfara':0.054, 'Yobe':0.118, 'Taraba':0.221, 'Sokoto':0.032}
        data =[]
        for location, value in loc_and_value.iteritems():
            loc = Location.objects.create(
                name = location,
                location_code = location,
                location_type_id = self.lt.id,
                office_id = self.o.id,
                parent_location_id = parent_location_id
            )
            loc_dict = {'location_id': loc.id, 'value':value}
            data.append(loc_dict)

        for row in data:
            DataPointComputed.objects.create(
                location_id = row['location_id'],
                value = row['value'],
                campaign_id = campaign_id,
                indicator_id = indicator_id,
                document_id = document.id
            )

    # add another location and datapoint that shouldn't be retrieved
        nyc = Location.objects.create(
            name = 'New York',
            location_code = 'New York',
            location_type_id = self.lt.id,
            office_id = self.o.id,
            parent_location_id = 2345
        )

        DataPointComputed.objects.create(
            location_id = nyc.id,
            value = 0.0432,
            campaign_id = campaign_id,
            indicator_id = indicator_id,
            document_id = document.id
        )
        get_parameter = 'indicator__in={0}&campaign__in={1}&parent_location_id__in={2}&chart_type=MapChart'\
            .format(indicator_id, campaign_id, parent_location_id)

        resp = self.api_client.get('/api/v1/datapoint/?' + get_parameter, \
            format='json', authentication=self.get_credentials())

        response_data = self.deserialize(resp)
        chart_data = response_data['meta']['chart_data']

        self.assertEqual(len(chart_data), len(data))
        #since ordering can vary, check that each of the items is in the list
        all_values_in_list = True
        for datapoint in chart_data:
            if datapoint not in data:
                all_values_in_list = False

        self.assertEqual(True, all_values_in_list)

    # make sure that the api returns an empty list if the parent location has no children
    def test_map_transform_no_children(self):
        indicator_id = 1
        campaign_id = 2
        parent_location_id = 3

        document = Document.objects.create(doc_title='some doc')


        # add a bunch of children for parent_location_id
        loc_and_value ={'Zamfara':0.054, 'Yobe':0.118, 'Taraba':0.221, 'Sokoto':0.032}
        data =[]
        for location, value in loc_and_value.iteritems():
            loc = Location.objects.create(
                name = location,
                location_code = location,
                location_type_id = self.lt.id,
                office_id = self.o.id,
                parent_location_id = self.top_lvl_location.id
            )
            loc_dict = {'location_id': loc.id, 'value':value}
            data.append(loc_dict)

        for row in data:
            DataPointComputed.objects.create(
                location_id = row['location_id'],
                value = row['value'],
                campaign_id = campaign_id,
                indicator_id = indicator_id,
                document_id = document.id
            )

        child_id = Location.objects.filter(name='Zamfara')[0].id

        get_parameter = 'indicator__in={0}&campaign__in={1}&parent_location_id__in={2}&chart_type=MapChart'\
            .format(indicator_id, campaign_id, child_id)

        resp = self.api_client.get('/api/v1/datapoint/?' + get_parameter, \
            format='json', authentication=self.get_credentials())

        response_data = self.deserialize(resp)
        self.assertEqual(len(response_data['objects']), 0)

        self.assertEqual(len(response_data['meta']['chart_data']), 0)


