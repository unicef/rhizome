import json

from tastypie.test import ResourceTestCase
from django.contrib.auth.models import User
from setup_helpers import TestSetupHelpers

from rhizome.models import Indicator, IndicatorTag, \
    CalculatedIndicatorComponent,IndicatorToTag, IndicatorBound, \
    LocationPermission, Location, LocationType, Office

from rhizome.cache_meta import IndicatorCache


class IndicatorCalculationResourceTest(ResourceTestCase):
    def setUp(self):
        super(IndicatorCalculationResourceTest, self).setUp()

        self.ts = TestSetupHelpers()

        self.lt = self.ts.create_arbitrary_location_type()
        self.o = self.ts.create_arbitrary_office()

        self.top_lvl_location = self.ts.create_arbitrary_location(self.lt.id, self.o.id)

        LocationPermission.objects.create(user_id = self.ts.user.id,\
            top_lvl_location_id = self.top_lvl_location.id)

        self.ind = self.ts.create_arbitrary_indicator()

    def test_create_calculation(self):
        Indicator.objects.create(short_name='Test Indicator 1', \
                                 name='Test Indicator for the Tag 1', \
                                 data_format='int', \
                                 description='Test Indicator for the Tag 1 Description', )

        Indicator.objects.create(short_name='Test Indicator 2', \
                                 name='Test Indicator for the Tag 2', \
                                 data_format='int', \
                                 description='Test Indicator for the Tag 2 Description', )

        list = Indicator.objects.all().order_by('-id')

        indicator_1 = list[0]
        indicator_2 = list[1]

        CalculatedIndicatorComponent.objects.filter(indicator_id=indicator_1.id,
                                                    indicator_component_id=indicator_2.id).delete()

        post_data = {'indicator_id': indicator_1.id, 'component_id': indicator_2.id, 'typeInfo': 'DENOMINATOR'}

        resp = self.ts.post(self, '/api/v1/indicator_calculation/', data=post_data)

        response_data = self.deserialize(resp)
        indicator_calculation = CalculatedIndicatorComponent.objects.all().order_by('-id')[0]

        self.assertHttpCreated(resp)
        self.assertEqual(indicator_calculation.id, response_data['id'])
        self.assertEqual(indicator_1.id, response_data['indicator_id'])
        self.assertEqual(indicator_2.id, response_data['component_id'])
        self.assertEqual(indicator_calculation.calculation, response_data['typeInfo'])

    def test_remove_calculation(self):
        Indicator.objects.create(short_name='Test Indicator 1', \
                                 name='Test Indicator for the Tag 1', \
                                 description='Test Indicator for the Tag 1 Description', )
        Indicator.objects.create(short_name='Test Indicator 2', \
                                 name='Test Indicator for the Tag 2', \
                                 description='Test Indicator for the Tag 2 Description', )

        list = Indicator.objects.all().order_by('-id')

        indicator_1 = list[0]
        indicator_2 = list[1]

        CalculatedIndicatorComponent.objects.all().delete()

        component = CalculatedIndicatorComponent.objects.create(indicator_id=indicator_1.id,
                                                    indicator_component_id=indicator_2.id,
                                                    calculation = 'test calculation')

        self.assertEqual(CalculatedIndicatorComponent.objects.count(), 1)

        delete_url = '/api/v1/indicator_calculation/?id=' + str(component.id)

        self.api_client.delete(delete_url, format='json', data={}, authentication=self.ts.get_credentials(self))

        self.assertEqual(CalculatedIndicatorComponent.objects.count(), 0)

    #GET function-- pass parameter indicator_id. If indicator ID is incorrect 
    # or not included, will return 200 with an empty list.
    def test_get_calculation(self):
        ind = Indicator.objects.create(short_name='Test Indicator 1', \
                         name='Test Indicator for the Tag 1', \
                         description='Test Indicator for the Tag 1 Description', )
        
        ind2 = Indicator.objects.create(short_name='Test Indicator 2', \
                                 name='Test Indicator for the Tag 2', \
                                 data_format='int', \
                                 description='Test Indicator for the Tag 2 Description', )

        it = CalculatedIndicatorComponent.objects.create(
            indicator_id=ind.id,
            indicator_component_id=ind2.id,
            calculation='DENOMINATOR',
        )

        get_data = {'indicator_id': ind.id}
        resp = self.ts.get(self, '/api/v1/indicator_calculation/', get_data)
        self.assertHttpOK(resp)
        resp_data = self.deserialize(resp)
        self.assertEqual(len(resp_data['objects']), 1)

    def test_get_calculation_invalid_id(self):
    	get_data = {'indicator_id': 1234}
        resp = self.ts.get(self, '/api/v1/indicator_calculation/', get_data)
        self.assertHttpOK(resp)
        resp_data = self.deserialize(resp)
        self.assertEqual(len(resp_data['objects']), 0)
