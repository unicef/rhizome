
from django.test import TestCase
from tastypie.test import ResourceTestCase
from tastypie.models import ApiKey
from django.contrib.auth.models import User
from rhizome.models import CacheJob, Office, Indicator, Location,\
    LocationType, DataPointComputed, CampaignType, Campaign, IndicatorTag,\
    LocationPermission, Document, IndicatorClassMap

from rhizome.cache_meta import LocationTreeCache
from random import randint

class DataPointResourceTest(ResourceTestCase):

    def setUp(self):
        super(DataPointResourceTest, self).setUp()

        # Create a user.
        self.username = 'john'
        self.password = 'pass'
        self.user = User.objects.create_user(self.username,\
                                        'eradicate@polio.com', self.password)

        self.lt = LocationType.objects.create(name='Country',admin_level = 0)
        self.distr, created = \
            LocationType.objects.get_or_create(name='District',admin_level = 1)
        self.prov, created = \
            LocationType.objects.get_or_create(name='Province',admin_level = 2)

        self.o = Office.objects.create(name = 'Earth')

        self.top_lvl_location = Location.objects.create(
                name = 'Nigeria',
                location_code = 'Nigeria',
                id=1234,
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

    def test_get_no_params(self):
        resp = self.api_client.get('/api/v1/datapoint/',\
            format='json', authentication=self.get_credentials())
        self.assertHttpOK(resp)
        response_data = self.deserialize(resp)
        self.assertEqual(response_data['error'][0], "\"'indicator__in'\" is a required parameter!")

    # what happens if we request a non-existent datapoint
    def test_empty_response(self):
        start_date = '2016-02-01'
        end_date = '2016-02-01'
        get_parameter = 'indicator__in={0}&campaign_start={1}&campaign_end={2}&location_id__in={3}'\
            .format(1, start_date, end_date, self.top_lvl_location.id)

        resp = self.api_client.get('/api/v1/datapoint/?' + get_parameter, \
            format='json', authentication=self.get_credentials())
        self.assertHttpOK(resp)
        response_data = self.deserialize(resp)
        self.assertEqual(len(response_data['objects']),0)

    # this tests for both MapChart and BubbleMap
    def test_map_transform(self):

        indicator_id = 1
        indicator_object = Indicator.objects.create(
            id = indicator_id,name = 'name', short_name = 'short_name'
        )
        campaign_id = 2
        parent_location_id =3
        document = Document.objects.create(doc_title='some doc')

        loc_and_value ={'Zamfara':0.054, 'Yobe':0.118, 'Taraba':0.221, 'Sokoto':0.032}
        data =[]
        for location, value in loc_and_value.iteritems():
            loc = Location.objects.create(
                name = location,
                location_code = location,
                location_type_id = self.distr.id,
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

        ltr = LocationTreeCache()
        ltr.main()
        get_parameter = 'indicator__in={0}&campaign__in={1}&parent_location_id__in={2}&chart_type=MapChart'\
            .format(indicator_id, campaign_id, parent_location_id)

        resp = self.api_client.get('/api/v1/datapoint/?' + get_parameter, \
            format='json', authentication=self.get_credentials())

        response_data = self.deserialize(resp)
        self.assertHttpOK(resp)

        chart_data = response_data['meta']['chart_data']

        self.assertEqual(len(chart_data), len(data))
        #since ordering can vary, check that each of the items is in the list
        all_values_in_list = True
        for datapoint in chart_data:
            if datapoint not in data:
                all_values_in_list = False

        self.assertEqual(True, all_values_in_list)

        # test BubbleMap
        map_type ='BubbleMap'

        get_parameter = 'indicator__in={0}&campaign__in={1}&parent_location_id__in={2}&chart_type={3}'\
            .format(indicator_id, campaign_id, parent_location_id, map_type)

        resp = self.api_client.get('/api/v1/datapoint/?' + get_parameter, \
            format='json', authentication=self.get_credentials())

        response_data = self.deserialize(resp)
        self.assertHttpOK(resp)
        chart_data = response_data['meta']['chart_data']
        self.assertEqual(len(chart_data), len(data))
        if 'z' in chart_data[0].keys():
            pass
        else:
            fail('returned object didn\'t contain a \'z\' for value')

    # make sure that the api returns an empty list if the parent location has no children
    def test_map_transform_no_children(self):
        indicator_id = 1
        indicator_object = Indicator.objects.create(
            id = indicator_id,name = 'name', short_name = 'short_name'
        )
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

        # test MapChart
        map_type = 'MapChart'
        get_parameter = 'indicator__in={0}&campaign__in={1}&parent_location_id__in={2}&chart_type={3}'\
            .format(indicator_id, campaign_id, child_id, map_type)

        resp = self.api_client.get('/api/v1/datapoint/?' + get_parameter, \
            format='json', authentication=self.get_credentials())

        response_data = self.deserialize(resp)

        self.assertEqual(len(response_data['objects']), 0)
        self.assertEqual(len(response_data['meta']['chart_data']), 0)

    def test_indicator_filter(self):
        campaign_id = 2
        province_lt, created = LocationType.objects\
            .get_or_create(name='Province',defaults = {'admin_level': 1})

        document = Document.objects.create(doc_title='some doc')

        #make a couple different types of indicators, and indicators with different values
        indicator_names_to_values = {"LPD Status":[1,2],
            'LQAS':[0, 1, 2]
        }

        indicator_ids_to_values ={}

        for indicator_name, values in indicator_names_to_values.iteritems():
            indicator = Indicator.objects.create(short_name=indicator_name, \
                                     name=indicator_name, \
                                     description=indicator_name,
                                     data_format ='class' )
            indicator_ids_to_values[indicator.id] = values



        some_provinces = ['Kandahar', 'Kunar', 'Hilmand', 'Nimroz', 'Sari-Pul', 'Kabul', 'Paktika', 'Ghazni']

        ind_id_keys = indicator_ids_to_values.keys()
        indicator_to_query = ind_id_keys[1]

       # choose which indicator/value pair to filter by, and keep track of dps that match this as they're created
        indicator_to_filter = ind_id_keys[0]
        indicator_val_to_filter = indicator_ids_to_values[indicator_to_filter][0]
        dps_to_track =[]

        for province in some_provinces:
            # create the province
            prov = Location.objects.create(
                name = province,
                location_code = province,
                location_type_id = province_lt.id,
                office_id = self.o.id,
                parent_location_id = self.top_lvl_location.id
            )

            # create a random dp for each indicator
            for indicator_id, values in indicator_ids_to_values.iteritems():
                idx = randint(0, len(values)-1)
                value_to_use = values[idx]
                dp = DataPointComputed.objects.create(
                    location_id = prov.id,
                    value = value_to_use,
                    campaign_id = campaign_id,
                    indicator_id = indicator_id,
                    document_id = document.id
                )
                if indicator_id == indicator_to_filter and value_to_use == indicator_val_to_filter:
                    dps_to_track.append(dp)

        indicator_name_to_filter = Indicator.objects.get(id=indicator_to_filter);
        get_parameter = 'indicator__in={0}&campaign__in={1}&parent_location_id__in={2}&filter_indicator={3}&filter_value={4}&chart_type=TableChart'\
            .format(indicator_to_query, campaign_id, self.top_lvl_location.id, indicator_name_to_filter, indicator_val_to_filter)

        resp = self.api_client.get('/api/v1/datapoint/?' + get_parameter, \
            format='json', authentication=self.get_credentials())

        response_data = self.deserialize(resp)
        self.assertEqual(len(response_data['objects']), len(dps_to_track))

        # oof, nested for loop is okay since it's a small dataset
        # makes sure that all the campaign and location ids match
        for dp in dps_to_track:
            found_dp = False
            for resp_dp in response_data['objects']:
                same_campaign = int(resp_dp['campaign']) == dp.campaign_id
                same_location = int(resp_dp['location']) == dp.location_id
                if same_location and same_campaign:
                    found_dp = True
            if not found_dp:
                fail("the datapoints from the respnse do not match the system")
                break
        pass
        #  make sure the chart data isn't empty


    def _get_cumulative(self): ## handling cumulative differntly
        # add a couple different campaigns with different time frames
        campaign_type = CampaignType.objects\
            .create(name='National Immunization Days (NID)')

        ind_tag = IndicatorTag.objects.create(tag_name='Polio')
        document = Document.objects.create(doc_title='uploadddd')

        start_date_1 = '2016-01-01'
        end_date_1 = '2016-01-01'

        campaign_1 = Campaign.objects.create(office=self.o,\
            campaign_type=campaign_type,start_date=start_date_1,end_date=end_date_1,\
            top_lvl_indicator_tag_id = ind_tag.id,\
            top_lvl_location_id = self.top_lvl_location.id)

        start_date_2 = '2016-02-01'
        end_date_2 = '2016-02-01'

        campaign_2 = Campaign.objects.create(office=self.o,\
            campaign_type=campaign_type,start_date=start_date_2,end_date=end_date_2,\
            top_lvl_indicator_tag_id = ind_tag.id,\
            top_lvl_location_id = self.top_lvl_location.id)

        # create an indicator and location
        indicator = Indicator.objects.create(short_name='number missed children', \
                                     name='number missed children', \
                                     data_format='int', )
        province = Location.objects.create(
                name = 'Kandahar',
                location_code = 'Kandahar',
                location_type_id = self.lt.id,
                office_id = self.o.id,
                parent_location_id = self.top_lvl_location.id
            )
        # add datapoints for these different campaigns
        value_1 =12
        value_2 =322
        dp_1 = DataPointComputed.objects.create(
                    location_id = province.id,
                    value = value_1,
                    campaign_id = campaign_1.id,
                    indicator_id = indicator.id,
                    document_id = document.id,
                )

        dp_2 = DataPointComputed.objects.create(
                location_id = province.id,
                value = value_2,
                campaign_id = campaign_2.id,
                indicator_id = indicator.id,
                document_id = document.id,

            )

        # make sure that that api call returns cumulative values,
        get_parameter = 'indicator__in={0}&start_date=2016-01-01&end_date=2016-02-02&parent_location_id__in={2}&chart_type=MapChart&cumulative=1'\
            .format(indicator.id, campaign_1.id, self.top_lvl_location.id)

        resp = self.api_client.get('/api/v1/datapoint/?' + get_parameter, \
            format='json', authentication=self.get_credentials())

        response_data = self.deserialize(resp)
        returned_indicators = response_data['objects']
        self.assertEqual(len(returned_indicators), 1)
        self.assertEqual(returned_indicators[0]['indicators'][0]['value'], value_1 + value_2)

