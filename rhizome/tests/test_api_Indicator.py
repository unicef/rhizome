
from base_test_case import RhizomeAPITestCase
from setup_helpers import TestSetupHelpers

from rhizome.models import Indicator, IndicatorTag, \
    CalculatedIndicatorComponent, IndicatorToTag, IndicatorBound, \
    LocationPermission, Location, LocationType, Office

from rhizome.cache_meta import IndicatorCache


class IndicatorResourceTest(RhizomeAPITestCase):

    def setUp(self):
        super(IndicatorResourceTest, self).setUp()

        self.ts = TestSetupHelpers()

        self.lt = self.ts.create_arbitrary_location_type()
        self.o = self.ts.create_arbitrary_office()

        self.top_lvl_location = self.ts.create_arbitrary_location(
            self.lt.id, self.o.id)

        LocationPermission.objects.create(user_id=self.ts.user.id,
                                          top_lvl_location_id=self.top_lvl_location.id)

        self.ind = self.ts.create_arbitrary_indicator()

    def test_auth_valid(self):
        resp = self.api_client.get('/api/v1/', format='json')
        self.assertValidJSONResponse(resp)

    def test_get_indicator_id(self):
        get_data = {'id': self.ind.id}
        resp = self.ts.get(self, '/api/v1/indicator/', data=get_data)
        resp_data = self.deserialize(resp)
        self.assertEqual(len(resp_data['objects']), 1)

    def test_get_invalid_indicator_id(self):
        get_data = {'id': 123456}
        resp = self.ts.get(self, '/api/v1/indicator/', data=get_data)
        self.assertHttpOK(resp)
        resp_data = self.deserialize(resp)
        self.assertEqual(len(resp_data['objects']), 0)

    def test_create_indicator(self):
        Indicator.objects.all().delete()

        self.assertEqual(Indicator.objects.count(), 0)

        post_data = {'name': 'New test indicator name',
                     'short_name': 'New test short name',
                     'description': 'test',
                     'bad_bound': 1,
                     'good_bound': 10,
                     'source_name': 'RHIZOME'
                     }

        resp = self.ts.post(self, '/api/v1/indicator/', data=post_data)
        resp_data = self.deserialize(resp)
        self.assertEqual(Indicator.objects.count(), 1)
        self.assertEqual(resp_data['name'], 'New test indicator name')

    def test_create_indicator_with_id(self):
        Indicator.objects.all().delete()

        self.assertEqual(Indicator.objects.count(), 0)

        post_data = {'name': 'New test indicator name',
                     'short_name': 'New test short name',
                     'description': 'test',
                     'id': 123,
                     'bad_bound': 1,
                     'good_bound': 10,
                     'source_name': 'RHIZOME'
                     }

        resp = self.ts.post(self, '/api/v1/indicator/', data=post_data)

        resp_data = self.deserialize(resp)
        self.assertEqual(resp_data['id'], 123)

    def test_create_indicator_missing_fields(self):
        Indicator.objects.all().delete()

        self.assertEqual(Indicator.objects.count(), 0)

        post_data = {'name': 'New test indicator name',
                     'short_name': 'New test short name',
                     'data_format': 'int',
                     'id': -1,
                     'description': 'test',
                     'source_name': 'RHIZOME'
                     }

        resp = self.ts.post(self, '/api/v1/indicator/', data=post_data)

        self.assertHttpApplicationError(resp)

    # the indicator is invalid because bad_bound and good_bound are passed as
    # strings
    def test_create_indicator_invalid(self):
        Indicator.objects.all().delete()

        self.assertEqual(Indicator.objects.count(), 0)

        post_data = {'name': 'New test indicator name',
                     'short_name': 'New test short name',
                     'description': 'test',
                     'bad_bound': "hello",
                     'good_bound': 'dsds',
                     'source_name': '???'
                     }

        resp = self.ts.post(self, '/api/v1/indicator/', data=post_data)

        self.assertHttpApplicationError(resp)

    def test_bound_and_tag_json(self):
        Indicator.objects.all().delete()

        ind = Indicator.objects.create(**{
            'name': 'test name',
            'short_name': 'test short name',
            'data_format': 'int',
            'description': 'test description',
        })

        ## tags ##
        ind_tag_0 = IndicatorTag.objects.create(tag_name='tag1')
        ind_tag_1 = IndicatorTag.objects.create(tag_name='tag2')

        indicator_to_tag_0 = IndicatorToTag.objects.create(
            indicator=ind, indicator_tag=ind_tag_0
        )
        indicator_to_tag_1 = IndicatorToTag.objects.create(
            indicator=ind, indicator_tag=ind_tag_1
        )

        ## bounds ##
        bound_dict_0 = {u'indicator_id': ind.id, u'mn_val': 10,
                        u'mx_val': 20, u'bound_name': u'Good'}
        bound_dict_1 = {'indicator_id': ind.id, u'mn_val': 20,
                        u'mx_val': 30, u'bound_name': u'Bad'}

        IndicatorBound.objects.create(**bound_dict_0)
        IndicatorBound.objects.create(**bound_dict_1)

        ## cache the indicator id ##
        ic = IndicatorCache([ind.id])
        ic.main()

        target_tag_json = [ind_tag_0.id, ind_tag_1.id]
        target_bound_json = [bound_dict_0, bound_dict_1]

        resp = self.ts.get(self, '/api/v1/indicator/', data={})

        data = self.deserialize(resp)
        objects = data['objects']

        ## basic attributes ##

        self.assertEqual(ind.short_name, objects[0]['short_name'])
        self.assertEqual(ind.name, objects[0]['name'])
        self.assertEqual(ind.description, objects[0]['description'])

        ## pivoted attributes ##
        self.assertEqual(sorted(target_tag_json),
                         sorted(objects[0]['tag_json']))
        self.assertEqual(sorted(target_bound_json),
                         sorted(objects[0]['bound_json']))
