
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
                location_id = self.top_lvl_location.id,
                indicator_id = self.ind.id,
                data_date = self.clean_date(row.data_date),
                value = 1,
                source_submission_id = 1
            )


    def clean_date(self, date_string):

        try:
            date = datetime.strptime(date_string, '%d-%m-%y')
        except ValueError:
            pass

        try:
            date = datetime.strptime(date_string, '%m/%d/%y')
        except ValueError:
            date = None

        return date


    def get_credentials(self):
        result = self.api_client.client.login(username=self.username,
                                              password=self.password)
        return result


    def test_get_list(self):
        # python manage.py test rhizome.tests.test_api_datapoint_groupby_date --settings=rhizome.settings.test

        get_parameter = 'group_by_time=year&indicator__in={0}&start_date={1}&end_date={2}&location_id={3}'\
            .format(self.ind.id, '2013-01-01' ,'2016-01-01', self.top_lvl_location.id)

        resp = self.api_client.get('/api/v1/datapoint/?' + get_parameter, \
            format='json', authentication=self.get_credentials())

        print 'response\n' * 5
        print resp
        print '===\n' * 5

        self.assertHttpOK(resp)
        response_data = self.deserialize(resp)
        objects = response_data['objects']

        print '=='
        pprint(objects)
        print '=='
        self.assertEqual(3, objects) # one for each year #
