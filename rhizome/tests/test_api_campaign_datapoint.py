from random import randint
import json

from django.contrib.auth.models import User
from pandas import read_csv, to_datetime

from rhizome.models.campaign_models import Campaign, CampaignType, \
    DataPointComputed
from rhizome.models.location_models import Location, LocationType,\
    LocationPermission
from rhizome.models.document_models import SourceObjectMap, Document
from rhizome.models.indicator_models import IndicatorTag, Indicator

from rhizome.cache_meta import LocationTreeCache
from rhizome.tests.base_test_case import RhizomeApiTestCase
from rhizome.tests.setup_helpers import TestSetupHelpers



class CampaignDataPointResourceTest(RhizomeApiTestCase):

    def setUp(self):
        super(CampaignDataPointResourceTest, self).setUp()

        # Create a user.
        self.username = 'john'
        self.password = 'pass'
        self.user = User.objects.create_user(self.username,\
                                        'eradicate@polio.com', self.password)

        self.get_credentials()
        self.ts = TestSetupHelpers()

        ## create a metadata and data for us to use to test ##
        self.create_metadata()

        self.country_lt = LocationType.objects\
            .create(name='Country',admin_level = 0)
        self.region_lt = LocationType.objects\
            .create(name='Region',admin_level = 1)
        self.province_lt = LocationType.objects\
            .create(name='Province',admin_level = 2)

        self.top_lvl_location = Location.objects.get(name = 'Nigeria')

        ltc = LocationTreeCache()
        ltc.main()

        LocationPermission.objects.create(user_id = self.user.id,\
            top_lvl_location_id = self.top_lvl_location.id)

    def create_metadata(self):
        '''
        Creating the Indicator, location, Campaign, meta data needed for the
        system to aggregate / caclulate.
        '''

        self.top_lvl_tag = IndicatorTag.objects.create(id=1, tag_name='Polio')

        campaign_df = read_csv('rhizome/tests/_data/campaigns.csv')
        campaign_df['start_date'] = to_datetime(campaign_df['start_date'])
        campaign_df['end_date'] = to_datetime(campaign_df['end_date'])

        location_df = read_csv('rhizome/tests/_data/locations.csv')
        indicator_df = read_csv('rhizome/tests/_data/indicators.csv')

        self.campaign_type = CampaignType.objects.create(id=1, name="test")

        locations = self.ts.model_df_to_data(location_df, Location)
        campaigns = self.ts.model_df_to_data(campaign_df, Campaign)
        self.ts.model_df_to_data(indicator_df, Indicator)
        self.user_id = User.objects.create_user(
            'test', 'test@test.com', 'test').id
        self.mapped_location_id = locations[0].id
        loc_map = SourceObjectMap.objects.create(
            source_object_code='AF001039003000000000',
            content_type='location',
            mapped_by_id=self.user_id,
            master_object_id=self.mapped_location_id
        )

        source_campaign_string = '2016 March NID OPV'
        self.mapped_campaign_id = campaigns[0].id
        campaign_map = SourceObjectMap.objects.create(
            source_object_code=source_campaign_string,
            content_type='campaign',
            mapped_by_id=self.user_id,
            master_object_id=self.mapped_campaign_id
        )

        self.mapped_indicator_with_data = locations[2].id
        indicator_map = SourceObjectMap.objects.create(
            source_object_code='Percent missed due to other reasons',
            content_type='indicator',
            mapped_by_id=self.user_id,
            master_object_id=self.mapped_indicator_with_data
        )

    def create_a_single_dp(self):

        obj = DataPointComputed.objects.create(
            campaign_id = 1,
            location_id = 1,
            indicator_id = 1,
            value = 0
        )

        return obj

    def get_credentials(self):
        result = self.api_client.client.login(username=self.username,
                                              password=self.password)
        return result


    def test_get_list(self):
        # Create the data, need input value to the DataPointComputed model.

        campaign = Campaign.objects.all()[0]
        location = Location.objects.all()[0]
        indicator = Indicator.objects.all()[0]
        value = 1.57

        datapoint = DataPointComputed.objects.create(value=value,\
            indicator=indicator, location=location,\
            campaign=campaign)

        # 6 Request To The API
        chart_uuid = 'abc123'
        get_parameter = 'indicator__in={0}&campaign_start={1}&campaign_end={2}&location_id__in={3}&chart_uuid={4}'\
            .format(indicator.id, campaign.start_date, campaign.end_date, location.id, chart_uuid)

        resp = self.api_client.get('/api/v1/campaign_datapoint/?' + get_parameter, \
            format='json', authentication=self.get_credentials())

        response_data = self.deserialize(resp)
        self.assertHttpOK(resp)
        self.assertEqual(response_data['error'], None)

        self.assertEqual(response_data['meta']["total_count"], 1)

        self.assertEqual(len(response_data['objects']), 1)
        self.assertEqual(response_data['objects'][0]['campaign_id'], campaign.id)
        self.assertEqual(response_data['objects'][0]['location_id'], location.id)
        self.assertEqual(int(response_data['objects'][0]['indicator_id']), indicator.id)
        self.assertEqual(float(response_data['objects'][0]['value']), value)

        # check the meta data
        expected_indicator_list = [indicator.id]
        response_indicator_list = [int(x) for x in\
            response_data['meta']['indicator_ids']]
        self.assertEqual(response_indicator_list,expected_indicator_list)

        response_chart_uuid = response_data['meta']['chart_uuid']
        self.assertEqual(response_chart_uuid, chart_uuid)

        expected_campaign_list = [campaign.id]
        response_campaign_list = [int(x) for x in response_data['meta']['campaign_ids']]
        self.assertEqual(response_campaign_list, expected_campaign_list)

        expected_location_list = [location.id]
        response_location_list = [int(x) for x in \
            response_data['meta']['location_ids']]
        self.assertEqual(response_location_list, expected_location_list)



        # self.assertEqual(int(response_data['meta']['location_ids']), location.id)

    def _get_class_datapoint(self):
        # ./manage.py test rhizome.tests.test_api_datapoint.DataPointResourceTest.test_get_class_datapoint --settings=rhizome.settings.test

        # 2. Create The Indicator value
        indicator = Indicator.objects.create(short_name='LQAS', \
                                             name='LQAS', \
                                              data_format='class',\
                                             description='LQAS', )

        # 3. Create The Location
        location = self.top_lvl_location

        # 4. Create The Campaign
        start_date = '2016-02-01'
        end_date = '2016-02-01'
        campaign = Campaign.objects.create(\
            campaign_type=self.campaign_type,\
            start_date=start_date,\
            end_date=end_date)

        # 5. Create Test DataPointComputed
        value = 1

        datapoint = DataPointComputed.objects.create(value=value,\
            indicator=indicator, location=location,\
            campaign=campaign)

        # 6 create the class indicator mapping

        # mapping_1 = IndicatorClassMap.objects.create(
        # indicator = indicator,
        # string_value = "Fail",
        # is_display =True)

        # 7 Request To The API
        get_parameter = 'indicator__in={0}&campaign_start={1}&campaign_end={2}&location_id__in={3}'\
            .format(indicator.id, start_date,end_date, location.id)

        resp = self.api_client.get('/api/v1/campaign_datapoint/?' + get_parameter, \
            format='json', authentication=self.get_credentials())

        response_data = self.deserialize(resp)
        self.assertHttpOK(resp)
        self.assertEqual(response_data['objects'][0]['value'], "Fail")

    def _get_no_params(self):
        '''
        fixme..
        '''
        # ./manage.py test rhizome.tests.test_api_datapoint.DataPointResourceTest.test_get_no_params --settings=rhizome.settings.test

        resp = self.api_client.get('/api/v1/campaign_datapoint/',\
            format='json', authentication=self.get_credentials())

        response_data = self.deserialize(resp)
        expected_error_msg = 'Sorry, this request could not be processed.'

        self.assertEqual(response_data[u'error'],expected_error_msg)

    # what happens if we request a non-existent datapoint
    def test_empty_response(self):
        start_date = '2016-02-01'
        end_date = '2016-02-01'
        get_parameter = 'indicator__in={0}&campaign_start={1}&campaign_end={2}&location_id__in={3}'\
            .format(1, start_date, end_date, self.top_lvl_location.id)

        resp = self.api_client.get('/api/v1/campaign_datapoint/?' + get_parameter, \
            format='json', authentication=self.get_credentials())
        self.assertHttpOK(resp)
        response_data = self.deserialize(resp)
        self.assertEqual(len(response_data['objects']),0)


    def test_indicator_filter(self):
        #  ./manage.py test rhizome.tests.test_api_datapoint.DataPointResourceTest.test_indicator_filter --settings=rhizome.settings.test

        campaign_id = 2

        # make a couple different types of indicators, and indicators with
        # different values
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

        some_provinces = ['Kandahar', 'Kunar', 'Hilmand', 'Nimroz', \
            'Sari-Pul', 'Kabul', 'Paktika', 'Ghazni']

        ind_id_keys = indicator_ids_to_values.keys()
        indicator_to_query = ind_id_keys[1]

        # choose which indicator/value pair to filter by, and keep track of
        # dps that match this as they're created
        indicator_to_filter = ind_id_keys[0]
        indicator_val_to_filter = indicator_ids_to_values[indicator_to_filter][0]
        dps_to_track =[]

        for province in some_provinces:
            # create the province
            prov = Location.objects.create(
                name = province,
                location_code = province,
                location_type_id = self.province_lt.id,
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
                    indicator_id = indicator_id
                )
                if indicator_id == indicator_to_filter and value_to_use == indicator_val_to_filter:
                    dps_to_track.append(dp)

        ltc = LocationTreeCache()
        ltc.main()

        indicator_name_to_filter = Indicator.objects.get(id=indicator_to_filter);
        get_parameter = 'indicator__in={0}&campaign__in={1}&location_id={2}&location_depth=1&filter_indicator={3}&filter_value={4}'\
            .format(indicator_to_query, campaign_id, self.top_lvl_location.id, indicator_name_to_filter, indicator_val_to_filter)

        resp = self.api_client.get('/api/v1/campaign_datapoint/?' + get_parameter, \
            format='json', authentication=self.get_credentials())

        self.assertHttpOK(resp)

        response_data = self.deserialize(resp)
        self.assertEqual(len(response_data['objects']), len(dps_to_track))
        # oof, nested for loop is okay since it's a small dataset
        # makes sure that all the campaign and location ids match
        for dp in dps_to_track:
            found_dp = False
            for resp_dp in response_data['objects']:
                same_campaign = int(resp_dp['campaign_id']) == dp.campaign_id
                same_location = int(resp_dp['location_id']) == dp.location_id
                if same_location and same_campaign:
                    found_dp = True
            if not found_dp:
                fail("the datapoints from the respnse do not match the system")
                break
        #  make sure the chart data isn't empty


    def _get_cumulative(self): ## handling cumulative differntly
        # add a couple different campaigns with different time frames

        start_date_1 = '2016-01-01'
        end_date_1 = '2016-01-01'

        campaign_1 = Campaign.objects.create(\
            campaign_type=self.campaign_type,start_date=start_date_1,\
            end_date=end_date_1)

        start_date_2 = '2016-02-01'
        end_date_2 = '2016-02-01'

        campaign_2 = Campaign.objects.create(\
            campaign_type=campaign_type,start_date=start_date_2,\
            end_date=end_date_2)

        # create an indicator and location
        indicator = Indicator.objects.create(short_name='number missed children', \
                                     name='number missed children', \
                                     data_format='int', )
        province = Location.objects.create(
                name = 'Kandahar',
                location_code = 'Kandahar',
                location_type_id = self.province_lt,
                parent_location_id = self.top_lvl_location.id
            )
        # add datapoints for these different campaigns
        value_1 =12
        value_2 =322
        dp_1 = DataPointComputed.objects.create(
                    location_id = province.id,
                    value = value_1,
                    campaign_id = campaign_1.id,
                    indicator_id = indicator.id
                )

        dp_2 = DataPointComputed.objects.create(
                location_id = province.id,
                value = value_2,
                campaign_id = campaign_2.id,
                indicator_id = indicator.id            )

        # make sure that that api call returns cumulative values,
        get_parameter = 'indicator__in={0}&start_date=2016-01-01&end_date=2016-02-02&location_id__in={2}&location_depth=1&chart_type=MapChart&cumulative=1'\
            .format(indicator.id, campaign_1.id, self.top_lvl_location.id)

        resp = self.api_client.get('/api/v1/campaign_datapoint/?' + get_parameter, \
            format='json', authentication=self.get_credentials())

        response_data = self.deserialize(resp)
        returned_indicators = response_data['objects']
        self.assertEqual(len(returned_indicators), 1)
        self.assertEqual(returned_indicators[0]['indicators'][0]['value'], value_1 + value_2)

    def test_location_id_and_location_depth(self):
        '''
        When i pass location_id and depth_level, I should get data for
        datapoints underneath the location_id requested at the specified
        depth level
        '''

        # create Afghanistan, region, and provinces
        afghanistan = Location.objects.create(
            name='Afghanistan',
            location_code ='Afghanistan',
            location_type_id = self.country_lt.id
        )

        south = Location.objects.create(
            name='South',
            location_code = 'South',
            location_type_id=self.region_lt.id,
            parent_location_id = afghanistan.id
            )

        kandahar = Location.objects.create(
            name='Kandahar',
            location_code = 'Kandahar',
            location_type_id = self.province_lt.id,
            parent_location_id = south.id
            )

        hilmand = Location.objects.create(
            name='Hilmand',
            location_code = 'Hilmand',
            location_type_id = self.province_lt.id,
            parent_location_id = south.id
            )

        ltc = LocationTreeCache()
        ltc.main()

        indicator = Indicator.objects.create(short_name='stuff', \
            name='stuff', \
            data_format='int',\
            description='some stuff that we want to count', )

        start_date = '2014-01-01'
        end_date = '2014-01-01'

        campaign = Campaign.objects.get(start_date=start_date)

        kandahar_value =27
        hilmand_value =31
        # create some datapoints at province level
        dp_kandahar = DataPointComputed.objects.create(
            location_id = kandahar.id,
            value = kandahar_value,
            campaign_id = campaign.id,
            indicator_id = indicator.id
        )

        dp_hilmand = DataPointComputed.objects.create(
            location_id = hilmand.id,
            value = hilmand_value,
            campaign_id = campaign.id,
            indicator_id = indicator.id
        )

        get_parameter = 'indicator__in={0}&campaign__in={1}&location_id={2}&location_depth=2'\
            .format(indicator.id, campaign.id, afghanistan.id)

        resp = self.api_client.get('/api/v1/campaign_datapoint/?' + get_parameter, \
            format='json', authentication=self.get_credentials())

        response_data = self.deserialize(resp)
        self.assertHttpOK(resp)
        self.assertEqual(len(response_data['objects']), 2)

        # makes sure we're getting the right dp values, thus confirming that the provinces are returned
        sum_of_values = 0
        for indicator in response_data['objects']:
            sum_of_values += float(indicator['value'])

        self.assertEqual(sum_of_values, kandahar_value+hilmand_value)

    def _show_missing_data(self):
        # create some campaigns and indicators
        indicator_1 = Indicator.objects.create(short_name='stuff', \
            name='stuff', \
            data_format='int',\
            description='some stuff that we want to count', )

        indicator_2 = Indicator.objects.create(short_name='more_stuff',
            name="more stuff to track",
            data_format ='int'
            )

        start_date_1 = '2016-01-01'
        end_date_1 = '2016-01-01'

        ind_tag = IndicatorTag.objects.create(tag_name='Polio')

        campaign_type = CampaignType.objects\
            .create(name='National Immunization Days (NID)')

        campaign_1 = Campaign.objects.create(\
            start_date=start_date_1,end_date=end_date_1,\
            campaign_type_id = campaign_type.id)

        start_date_2 = '2016-03-01'
        end_date_2 = '2016-03-01'

        campaign_2 = Campaign.objects.create(\
            start_date=start_date_2,end_date=end_date_2,\
            campaign_type_id = campaign_type.id)

        dp= DataPointComputed.objects.create(
            location_id = self.top_lvl_location.id,
            value = 21,
            campaign_id = campaign_1.id,
            indicator_id = indicator_1.id
        )

        # create another location

        self.location_2 = Location.objects.create(
                name = 'Afghanistan',
                location_code = 'Afghanistan',
                location_type_id = 1,
            )

        get_parameter = 'indicator__in={0}&campaign__in={1}&location_id__in={2}&show_missing_data=1'\
            .format(indicator_1.id,\
            str(campaign_1.id)+','+str(campaign_2.id),\
            str(self.top_lvl_location.id) +',' + str(self.location_2.id))

        resp = self.api_client.get('/api/v1/campaign_datapoint/?' + get_parameter, \
            format='json', authentication=self.get_credentials())

        response_data = self.deserialize(resp)
        self.assertHttpOK(resp)
        # produce the cartesian product of location and campaign

        ## 2 campaigns, one loc, one indicator gives you four ##
        self.assertEqual(len(response_data['objects']), 4)

        ## even though there is only one datapoint with information ##
        self.assertEqual(DataPointComputed.objects.count(), 1)

    def test_patch_campaign_datapoint(self):
        '''
        create a datapoint with the ORM, submit a PATCH request and see
        if the value changed.

        If the user tries to change anything exept the value, there should be
        an error.

        '''

        dp_to_patch = self.create_a_single_dp()
        patch_data = {'value': 1071.012}
        dp_url = '/api/v1/campaign_datapoint/%s/' % dp_to_patch.id

        ## submit the patch and make sure it has the proper response code
        resp = self.ts.patch(self, dp_url, data=patch_data)
        self.assertHttpAccepted(resp)

        ## now get the dp and see if the value has been is updated ##
        dp_to_patch = DataPointComputed.objects.get(id=dp_to_patch.id)
        self.assertEqual(dp_to_patch.value, patch_data['value'])

    def test_post_campaign_datapoint(self):
        '''
        post a record to the campaign datapoint table
        '''

        data_entry_doc = Document.objects.create(doc_title = 'Data Entry')

        indicator_id = Indicator.objects.all()[0].id
        campaign_id = Campaign.objects.all()[0].id
        location_id = Location.objects.all()[0].id

        data = {
                'indicator_id': indicator_id,
                'campaign_id': campaign_id,
                'location_id': location_id,
                'value': 10
                }
        resp = self.ts.post(self, '/api/v1/campaign_datapoint/', data)

        self.assertHttpCreated(resp)
        response_data = self.deserialize(resp)
        self.assertEqual(response_data['value'], 10.0)

    def test_post_campaign_datapoint_missing_data(self):
        '''
        if we do not have all hte keys we need, throw an error
        '''
        data = {'value': 10}
        resp = self.ts.post(self, '/api/v1/campaign_datapoint/', data)
        self.assertHttpApplicationError(resp)

    def _post_campaign_datapoint_invalid_data(self):
        '''
        The indicator, and campaign dont exists, the api should tell us

        This won't fail in the test framework becausae we don't check foreign
        keys.

        Make this a "TransactionTestCase and it will work"
        '''

        data = {
                'indicator_id': 4324,
                'campaign_id': 32132123,
                'location_id': 4321,
                'value': 10
                }
        resp = self.ts.post(self, '/api/v1/campaign_datapoint/', data)
        self.assertHttpApplicationError(resp)
        response_data = self.deserialize(resp)

    def test_delete_campaign_datapoint(self):
        '''
        create a datapoint, then delete it, make sure that it is no longer
        there.
        '''

        dpc = self.create_a_single_dp()
        delete_url = '/api/v1/campaign_datapoint/%d/' % dpc.id
        resp = self.ts.delete(self, delete_url)

        ## now make sure that it is not there #
        dpc_query = DataPointComputed.objects.filter(id=dpc.id)
        self.assertEqual(len(dpc_query), 0)

    def test_get_campaign_datapoint_by_id(self):
        '''
        Here we get one object from the API and ensure it has the proper
        data from when we inserted it.
        '''

        dwc_obj = self.create_a_single_dp()

        resp = self.ts.get(self, '/api/v1/campaign_datapoint/%s/' % dwc_obj.id)
        self.assertHttpOK(resp)
        response_data = self.deserialize(resp)
        self.assertEqual(response_data['value'], dwc_obj.value)
