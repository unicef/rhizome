
from rhizome.tests.base_test_case import RhizomeApiTestCase
from django.contrib.auth.models import User

from rhizome.models.office_models import Office
from rhizome.models.campaign_models import Campaign
from rhizome.models.location_models import Location, LocationType, \
    LocationPermission
from rhizome.models.indicator_models import Indicator, IndicatorTag
from rhizome.models.document_models import Document, SourceSubmission, DataPoint

from rhizome.cache_meta import LocationTreeCache
from rhizome.tests.setup_helpers import TestSetupHelpers

import pandas as pd
from datetime import datetime

class DateDataPointResourceTest(RhizomeApiTestCase):
    # python manage.py test rhizome.tests.test_api_datapoint_groupby_date --settings=rhizome.settings.test

    def setUp(self):
        super(DateDataPointResourceTest, self).setUp()

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

        self.ts = TestSetupHelpers()

        self.doc_id = Document.objects.create(doc_title='Data Entry').id

    def create_polio_cases(self):

        df = pd.read_csv('rhizome/tests/_data/AfgPolioCases.csv')

        for ix, row in df.iterrows():

            DataPoint.objects.create(
                location_id = self.some_district.id,
                indicator_id = self.ind.id,
                data_date = datetime.strptime(row.data_date, '%d-%m-%y'),
                value = 1,
                source_submission_id = 1,
                unique_index = str(self.some_district.id) + str(self.ind.id) +\
                    str(row.data_date)
            )

    def get_credentials(self):
        result = self.api_client.client.login(username=self.username,
                                              password=self.password)
        return result


    def test_get_list(self):
        # python manage.py test rhizome.tests.test_api_datapoint_groupby_date.DateDataPointResourceTest.test_get_list --settings=rhizome.settings.test

        get = {'group_by_time':'year',
            'indicator__in' : self.ind.id,
            'start_date' : '2013-01-01',
            'end_date' : '2016-12-01',
            'location_id' : self.top_lvl_location.id,
            'location_depth' : 1
        }
        resp = self.api_client.get('/api/v1/date_datapoint/', \
            format='json', data=get, authentication=self.get_credentials())

        response_data = self.deserialize(resp)
        self.assertHttpOK(resp)

        objects = response_data['objects']
        meta = response_data['meta']

        ## does the 'meta' object have what the FE needs
        self.assertEqual(self.ind.id, int(meta['indicator_ids'][0]))
        # self.assertEqual(self.top_lvl_location.id, int(meta['location_ids'][0]))

        ## WE SHOULD REMOVE THIS LOGIC FROM FE -- DATES ARE SEPARATE FROM CAMPAIGNS
        self.assertEqual(set(meta['time_groupings']),set([2014,2015,2016]))

        self.assertEqual(3, len(objects)) # one for each year #

        case_dict = {}
        for obj in objects:
            case_dict[obj['time_grouping']] = float(obj['value'])

        self.assertEqual(28.00, case_dict[2014])
        self.assertEqual(20.00, case_dict[2015])
        self.assertEqual(3.0, case_dict[2016])

    # basic test to just get a datapoint at a location for which we have data
    def test_get_list_no_recursion(self):
    # python manage.py test rhizome.tests.test_api_datapoint_groupby_date.DateDataPointResourceTest.test_get_list_no_recursion --settings=rhizome.settings.test

        location_id = 4321
        get = {
            'group_by_time' :'all_time',
            'indicator__in': self.ind.id,
            'start_date': '2013-01-01',
            'end_date': '2016-01-01',
            'location_id': location_id,
            'location_depth' : 0
        }

        resp = self.api_client\
            .get('/api/v1/date_datapoint/',
                data = get,
                format = 'json',
                authentication = self.get_credentials())

        self.assertHttpOK(resp)
        response_data = self.deserialize(resp)

        dps_all_time = DataPoint.objects.filter(indicator_id=self.ind.id)

        total_all_time = 0
        for dp in dps_all_time:
            total_all_time += dp.value

        self.assertEqual(len(response_data['objects']), 1)
        self.assertEqual(int(response_data['objects'][0]['location_id']), location_id)

    # not sure if this is a bug or what, but start and end date seem to be irrelevant when using group_by_time
    def test_get_list_diff_start_end_dates(self):

        get = {
            'group_by_time' :'year',
            'indicator__in': self.ind.id,
            'start_date': '2013-01-01',
            'end_date': '2016-01-01',
            'location_id__in': self.top_lvl_location.id,
            'location_depth' : 1
        }

        resp = self.api_client.get('/api/v1/date_datapoint/',
            data = get, format='json', authentication=self.get_credentials())

        self.assertHttpOK(resp)
        response_data = self.deserialize(resp)
        objects_1 = response_data['objects']

        get_2 = {
            'group_by_time' :'year',
            'indicator__in': self.ind.id,
            'start_date': '2016-01-01',
            'end_date': '2016-01-01',
            'location_id__in': self.top_lvl_location.id,
            'location_depth' : 1
        }

        resp_2 = self.api_client.get('/api/v1/date_datapoint/',\
            data = get_2, format='json',\
            authentication=self.get_credentials())

        self.assertHttpOK(resp_2)
        response_data_2 = self.deserialize(resp_2)
        objects_2 = response_data_2['objects']

        self.assertEqual(len(objects_1), len(objects_2))

    def test_get_list_quarter_and_all_time(self):

        get = {
            'group_by_time' :'quarter',
            'indicator__in': self.ind.id,
            'start_date': '2013-01-01',
            'end_date': '2016-07-01',
            'location_id': self.top_lvl_location.id,
            'location_depth' : 1
        }

        resp = self.api_client.get('/api/v1/date_datapoint/', \
            data = get , format='json', authentication=self.get_credentials())
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
            campaign = indicator['time_grouping']
            if campaign == '20141':
                value = float(indicator['value'])
                self.assertEqual(value, total)
                q1_found = True

        self.assertTrue(q1_found)

        get_2 = {
                'group_by_time' :'all_time',
                'indicator__in': self.ind.id,
                'start_date': '2013-01-01',
                'end_date': '2016-07-01',
                'location_id': self.top_lvl_location.id,
                'location_depth' : 1
            }

        resp = self.api_client.get('/api/v1/date_datapoint/', \
            data = get_2, format='json',\
            authentication=self.get_credentials())

        response_data = self.deserialize(resp)
        dps_all_time = DataPoint.objects.filter(indicator_id=self.ind.id)

        total_all_time = 0
        for dp in dps_all_time:
            total_all_time += dp.value

        self.assertEqual(len(response_data['objects']), 1)
        self.assertEqual(float(response_data['objects'][0]['value']), total_all_time)

    # provide a non-existent id
    def test_get_list_bogus_id(self):

        get = {
                'group_by_time' :'quarter',
                'indicator__in': 3223,
                'start_date': '2013-01-01',
                'end_date': '2016-01-01',
                'location_id__in': self.top_lvl_location.id,
                'location_depth' : 1
            }

        resp = self.api_client.get('/api/v1/date_datapoint/', \
            data = get, format='json',  authentication=self.get_credentials())

        self.assertHttpOK(resp)
        response_data = self.deserialize(resp)
        self.assertEqual(len(response_data['objects']), 0)

    def test_get_list_wrong_grouping(self):
        '''
        What happens when we request an unsupported time grouping
        '''
        # python manage.py test rhizome.tests.test_api_datapoint_groupby_date.DateDataPointResourceTest.test_get_list_wrong_grouping --settings=rhizome.settings.test

        get = {
                'group_by_time' :'xxx',
                'indicator__in': self.ind.id,
                'start_date': '2013-01-01',
                'end_date': '2016-01-01',
                'location_id': self.top_lvl_location.id,
                'location_depth' : 1
            }

        resp = self.api_client.get('/api/v1/date_datapoint/',data = get,\
            format='json', authentication=self.get_credentials())

        self.deserialize(resp)
        self.assertHttpApplicationError(resp)

    def _show_missing_data(self):
        '''
        This test is not in the suite because for date_datapoint results, the back end should not
        be in charge of creating every possible datapoint
        wiht a null value in order to handle discontinuity.

        show_all_data should not be a parameter and we should remove this and handle the fallout in the front end charting library.
        '''
        #  python manage.py test rhizome.tests.test_api_datapoint_groupby_date.DateDataPointResourceTest.test_show_missing_data --settings=rhizome.settings.test


        rando_ind = Indicator.objects.create(
            name = 'some other damn indicator',
            short_name = 'we don\'t care!',
            data_format = 'int'
        )
        rando_ind_2 = Indicator.objects.create(
            name = 'some other indicator',
            short_name = 'we don care!',
            data_format = 'int'
        )
        # ind_list = [rando_ind.id, rando_ind_2.id]
        ind_list = '{0},{1}'.format(rando_ind.id, rando_ind_2.id)

        get = {
                'group_by_time' :'year',
                'indicator__in': ind_list,
                'start_date': '2013-01-01',
                'end_date': '2016-01-01',
                'location_id__in': self.top_lvl_location.id,
                'location_depth' : 0,
                'show_missing_data': 1
            }

        resp = self.api_client.get('/api/v1/date_datapoint/', \
            data = get , format='json',\
            authentication=self.get_credentials())

        response_data = self.deserialize(resp)

        self.assertHttpOK(resp)
        self.assertEqual(len(response_data['objects']), 6)
        ## should be one object for the location, for each Indicator
        ## for each location and each time grouping.
        ## 3 yrs * 2 indicators * one location = 6

        ## if location_depth = 1, the number would have to take into
        ## account the number of sub locations one step under the parent

    def test_patch_date_datapoint(self):
        '''
        create a datapoint with the ORM, submit a PATCH request and see
        if the value changed.

        If the user tries to change anything exept the value, there should be
        an error.
        '''

        dp_to_patch = DataPoint.objects.all()[0]
        patch_data = {'value': 101.01}
        dp_url = '/api/v1/date_datapoint/%s/' % dp_to_patch.id

        ## submit the patch and make sure it has the proper response code
        resp = self.ts.patch(self, dp_url, data=patch_data)
        self.assertHttpAccepted(resp)

        ## now get the dp and see if the value has been is updated ##
        dp_to_patch = DataPoint.objects.get(id=dp_to_patch.id)
        self.assertEqual(dp_to_patch.value, patch_data['value'])

    def test_post_date_datapoint(self):
        '''
        post a record to the datapoint table
        '''

        indicator_id = Indicator.objects.all()[0].id
        location_id = Location.objects.all()[0].id
        val = 10.0

        data = {
                'indicator_id': indicator_id,
                'data_date': '2016-01-01',
                'location_id': location_id,
                'value': val
                }

        resp = self.ts.post(self, '/api/v1/date_datapoint/', data)

        self.assertHttpCreated(resp)
        response_data = self.deserialize(resp)
        self.assertEqual(response_data['value'], val)

        another_date = '2016-02-02'
        data['data_date'] = another_date

        resp = self.ts.post(self, '/api/v1/date_datapoint/', data)

        self.assertHttpCreated(resp)
        response_data = self.deserialize(resp)
        self.assertEqual(response_data['data_date'], another_date)

    def test_post_date_datapoint_missing_data(self):
        '''
        if we do not have all hte keys we need, throw an error
        '''
        data = {'value': 10}
        resp = self.ts.post(self, '/api/v1/date_datapoint/', data)
        self.assertHttpApplicationError(resp)

    def test_post_date_datapoint_invalid_data(self):
        '''
        The indicator, and campaign dont exists, the api should tell us
        '''

        data = {
                # 'document_id': doc_id,
                'indicator_id': 4324,
                'time_grouping': 32132123,
                'location_id': 4321,
                'value': 10
                }
        resp = self.ts.post(self, '/api/v1/date_datapoint/', data)
        self.assertHttpApplicationError(resp)
        response_data = self.deserialize(resp)

    def test_delete_date_datapoint(self):
        '''
        create a datapoint, then delete it, make sure that it is no longer
        there.
        '''

        dp = DataPoint.objects.all()[0]
        delete_url = '/api/v1/date_datapoint/%d/' % dp.id
        resp = self.ts.delete(self, delete_url)

        ## now make sure that it is not there #
        dpc_query = DataPoint.objects.filter(id=dp.id)
        self.assertEqual(len(dpc_query), 0)

    def test_get_date_datapoint_by_id(self):
        '''
        Here we get one object from the API and ensure it has the proper
        data from when we inserted it.
        '''


        dp_obj = DataPoint.objects.all()[0]
        resp = self.ts.get(self, '/api/v1/date_datapoint/%s/' % dp_obj.id)

        self.assertHttpOK(resp)
        response_data = self.deserialize(resp)
        self.assertEqual(response_data['value'], dp_obj.value)
