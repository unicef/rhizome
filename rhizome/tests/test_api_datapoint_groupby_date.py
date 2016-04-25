
from django.test import TestCase
from tastypie.test import ResourceTestCase
from tastypie.models import ApiKey
from django.contrib.auth.models import User
from rhizome.models import CacheJob, Office, Indicator, Location,\
    LocationType, DataPoint, CampaignType, Campaign, IndicatorTag,\
    LocationPermission, Document, IndicatorClassMap

from rhizome.cache_meta import LocationTreeCache
from random import randint

import pandas as pd
from datetime import datetime
from pprint import pprint

class DataPointResourceTest(ResourceTestCase):

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

        df = pd.read_csv('AfgPolioCases.csv')

        for ix, row in df.iterrows():
            DataPoint.objects.create(
                location_id = self.some_district.id,
                indicator_id = self.ind.id,
                data_date = self.clean_date(row.data_date),
                value = 1,
                source_submission_id = 1
            )

    def clean_date(self, date_string):

        date = None

        try:
            date = datetime.strptime(date_string, '%d-%m-%y')
        except ValueError:
            pass

        try:
            date = datetime.strptime(date_string, '%m/%d/%y')
        except ValueError:
            pass

        return date


    def get_credentials(self):
        result = self.api_client.client.login(username=self.username,
                                              password=self.password)
        return result


    def test_get_list(self):
        # python manage.py test rhizome.tests.test_api_datapoint_groupby_date --settings=rhizome.settings.test

        get_parameter = 'group_by_time=year&indicator__in={0}&start_date={1}&end_date={2}&location_id__in={3}'\
            .format(self.ind.id, '2013-01-01' ,'2016-01-01', self.top_lvl_location.id)

        resp = self.api_client.get('/api/v1/datapoint/?' + get_parameter, \
            format='json', authentication=self.get_credentials())

        self.assertHttpOK(resp)
        response_data = self.deserialize(resp)
        objects = response_data['objects']

        self.assertEqual(3, len(objects)) # one for each year #

        case_dict = {}
        for obj in objects:
            case_dict[obj['campaign']] = obj['indicators'][0][unicode(self.ind.id)]

        pprint(case_dict)

        self.assertEqual(28.00, case_dict[-2014]) # one for each year #
        self.assertEqual(20.00, case_dict[-2015]) # one for each year #
        self.assertEqual(3.0, case_dict[-2016]) # one for each year #
