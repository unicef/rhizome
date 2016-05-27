from base_test_case import RhizomeAPITestCase
from django.contrib.auth.models import User
from rhizome.models import CacheJob, Office, Indicator, Location,\
    LocationType, DataPoint, CampaignType, Campaign, IndicatorTag,\
    LocationPermission, Document, IndicatorClassMap, DataPointComputed

from rhizome.cache_meta import LocationTreeCache

import pandas as pd
from datetime import datetime

class DataPointResourceTest(RhizomeAPITestCase):

    def setUp(self):
        super(DataPointResourceTest, self).setUp()

        # Create a user.
        self.username = 'john'
        self.password = 'pass'
        self.user = User.objects.create_user(self.username,\
                                        'eradicate@polio.com', self.password)

        self.lt = LocationType.objects.create(name='Country',admin_level = 0)
        self.province_lt = LocationType.objects.create(name='Province'\
            ,admin_level = 1)
        self.district_lt = LocationType.objects.create(name='District'\
            ,admin_level = 2)


        self.o = Office.objects.create(name = 'Earth')
        self.ind = Indicator.objects.create(
            name = 'Polio Cases',
            short_name = 'Polio Cases',
            data_format = 'date_int'
        )

        self.top_lvl_location = Location.objects.create(
                name = 'Afghanistan',
                location_code = 'Afghanistan',
                id=1234,
                location_type_id = self.lt.id,
                office_id = self.o.id,
            )
        self.some_province = Location.objects.create(
                name = 'Province',
                location_code = 'Province',
                id=432,
                parent_location_id = self.top_lvl_location.id,
                location_type_id = self.province_lt.id,
                office_id = self.o.id,
            )
        self.some_district = Location.objects.create(
                name = 'Achin',
                location_code = 'Achin',
                id=4321,
                parent_location_id = self.some_province.id,
                location_type_id = self.district_lt.id,
                office_id = self.o.id,
            )

        ltc = LocationTreeCache()
        ltc.main()

        LocationPermission.objects.create(user_id = self.user.id,\
            top_lvl_location_id = self.top_lvl_location.id)

        self.get_credentials()
        self.create_polio_cases()

    def create_polio_cases(self):

        df = pd.read_csv('rhizome/tests/_data/AfgPolioCases.csv')

        for ix, row in df.iterrows():

            DataPoint.objects.create(
                location_id = self.some_district.id,
                indicator_id = self.ind.id,
                data_date = datetime.strptime(row.data_date, '%d-%m-%y'),
                value = 1,
                source_submission_id = 1,
                unique_index = str(self.some_district.id) + str(self.ind.id) + str(row.data_date)
            )


    def get_credentials(self):
        result = self.api_client.client.login(username=self.username,
                                              password=self.password)
        return result


    def test_get_list(self):
        # python manage.py test rhizome.tests.test_api_datapoint_groupby_date --settings=rhizome.settings.test

        get_parameter = 'group_by_time=year&indicator__in={0}&start_date={1}&end_date={2}&location_id__in={3}'\
            .format(self.ind.id, '2013-01-01' ,'2016-01-01', self.top_lvl_location.id)
        get = {'group_by_time':'year',
            'indicator__in' : self.ind.id,
            'start_date' : '2013-01-01',
            'end_date' : '2016-01-01',
            'location_id__in' : self.top_lvl_location.id
        }
        resp = self.api_client.get('/api/v1/date_datapoint/', \
            format='json', data=get, authentication=self.get_credentials())
        response_data = self.deserialize(resp)
        self.assertHttpOK(resp)
        objects = response_data['objects']

        self.assertEqual(3, len(objects)) # one for each year #

        case_dict = {}
        for obj in objects:
            case_dict[obj['campaign_id']] = float(obj['value'])

        self.assertEqual(28.00, case_dict[2014])
        self.assertEqual(20.00, case_dict[2015])
        self.assertEqual(3.0, case_dict[2016])

    # basic test to just get a datapoint at a location for which we have data
    def test_get_list_no_recursion(self):

        location_id = 4321
        get_parameter = 'group_by_time=all_time&indicator__in={0}&start_date={1}&end_date={2}&location_id__in={3}'\
            .format(self.ind.id, '2013-01-01' ,'2016-01-01', location_id)
        resp = self.api_client.get('/api/v1/date_datapoint/?' + get_parameter, \
            format='json', authentication=self.get_credentials())
        response_data = self.deserialize(resp)
        dps_all_time = DataPoint.objects.filter(indicator_id=self.ind.id)

        total_all_time = 0
        for dp in dps_all_time:
            total_all_time += dp.value

        self.assertEqual(len(response_data['objects']), 1)
        self.assertEqual(int(response_data['objects'][0]['location_id']), location_id)

    # not sure if this is a bug or what, but start and end date seem to be irrelevant when using group_by_time
    def test_get_list_diff_start_end_dates(self):
        get_parameter = 'group_by_time=year&indicator__in={0}&start_date={1}&end_date={2}&location_id__in={3}'\
            .format(self.ind.id, '2013-01-01' ,'2016-01-01', self.top_lvl_location.id)

        resp = self.api_client.get('/api/v1/date_datapoint/?' + get_parameter, \
            format='json', authentication=self.get_credentials())

        self.assertHttpOK(resp)
        response_data = self.deserialize(resp)
        objects_1 = response_data['objects']

        get_parameter_2 = 'group_by_time=year&indicator__in={0}&start_date={1}&end_date={2}&location_id__in={3}'\
            .format(self.ind.id, '2016-01-01' ,'2016-01-01', self.top_lvl_location.id)

        resp_2 = self.api_client.get('/api/v1/date_datapoint/?' + get_parameter_2, \
            format='json', authentication=self.get_credentials())

        self.assertHttpOK(resp_2)
        response_data_2 = self.deserialize(resp_2)
        objects_2 = response_data_2['objects']

        self.assertEqual(len(objects_1), len(objects_2))

    def test_get_list_quarter_and_all_time(self):
        get_parameter = 'group_by_time=quarter&indicator__in={0}&start_date={1}&end_date={2}&location_id__in={3}'\
            .format(self.ind.id, '2013-01-01' ,'2016-01-01', self.top_lvl_location.id)

        resp = self.api_client.get('/api/v1/date_datapoint/?' + get_parameter, \
            format='json', authentication=self.get_credentials())
        response_data = self.deserialize(resp)
        self.assertHttpOK(resp)
        dps_q1_2014 = DataPoint.objects.filter(
            data_date__range=('2014-01-01', '2014-03-31'),\
            indicator = self.ind.id
            )
        total = 0
        for dp in dps_q1_2014:
            total += dp.value

        # find the total for q1 2014
        q1_found = False

        for indicator in response_data['objects']:
            campaign = indicator['campaign_id']
            if campaign == '20141':
                value = float(indicator['value'])
                self.assertEqual(value, total)
                q1_found = True

        self.assertTrue(q1_found)

        get_parameter = 'group_by_time=all_time&indicator__in={0}&start_date={1}&end_date={2}&location_id__in={3}'\
            .format(self.ind.id, '2013-01-01' ,'2016-01-01', self.top_lvl_location.id)
        resp = self.api_client.get('/api/v1/date_datapoint/?' + get_parameter, \
            format='json', authentication=self.get_credentials())
        response_data = self.deserialize(resp)
        dps_all_time = DataPoint.objects.filter(indicator_id=self.ind.id)

        total_all_time = 0
        for dp in dps_all_time:
            total_all_time += dp.value

        self.assertEqual(len(response_data['objects']), 1)
        self.assertEqual(float(response_data['objects'][0]['value']), total_all_time)

    # provide a non-existent id
    def test_get_list_bogus_id(self):
        get_parameter = 'group_by_time=quarter&indicator__in={0}&start_date={1}&end_date={2}&location_id__in={3}'\
            .format(3223, '2013-01-01' ,'2016-01-01', self.top_lvl_location.id)

        resp = self.api_client.get('/api/v1/date_datapoint/?' + get_parameter, \
            format='json', authentication=self.get_credentials())

        self.assertHttpOK(resp)
        response_data = self.deserialize(resp)
        self.assertEqual(len(response_data['objects']), 0)

        # what happens when we throw an unsupported grouping up in here?
    def test_get_list_wrong_grouping(self):
        get_parameter = 'group_by_time=week&indicator__in={0}&start_date={1}&end_date={2}&location_id__in={3}'\
            .format(self.ind.id, '2013-01-01' ,'2016-01-01', self.top_lvl_location.id)

        resp = self.api_client.get('/api/v1/date_datapoint/?' + get_parameter, \
            format='json', authentication=self.get_credentials())
        self.deserialize(resp)
        self.assertHttpApplicationError(resp)


    def test_show_missing_data(self):
        rando_ind = Indicator.objects.create(
            name = 'some other damn indicator',
            short_name = 'we don\'t care!',
            data_format = 'int'
        )

        get_parameter = 'group_by_time=year&indicator__in={0}&start_date={1}&end_date={2}&location_id__in={3}&show_missing_data=1'\
            .format(str(self.ind.id)+','+str(rando_ind.id), '2013-01-01' ,'2016-01-01', self.top_lvl_location.id)

        resp = self.api_client.get('/api/v1/date_datapoint/?' + get_parameter, \
            format='json', authentication=self.get_credentials())
        response_data = self.deserialize(resp)
        self.assertEqual(len(response_data['objects']), 6)
