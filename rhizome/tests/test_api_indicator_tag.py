
from base_test_case import RhizomeAPITestCase
from setup_helpers import TestSetupHelpers

from rhizome.models import Indicator, IndicatorTag, \
    CalculatedIndicatorComponent, IndicatorToTag, IndicatorBound, \
    LocationPermission, Location, LocationType, Office


class IndicatorTagResourceTest(RhizomeAPITestCase):

    def setUp(self):
        super(IndicatorTagResourceTest, self).setUp()

        self.ts = TestSetupHelpers()

        self.lt = self.ts.create_arbitrary_location_type()
        self.o = self.ts.create_arbitrary_office()

        self.top_lvl_location = self.ts.create_arbitrary_location(
            self.lt.id, self.o.id)

    def test_get_indicator_tag_id(self):
        tag_name = 'tag1'
        ind_tag_0 = IndicatorTag.objects.create(tag_name=tag_name)
        data = {'id': ind_tag_0.id}
        resp = self.ts.get(self, '/api/v1/indicator_tag/', data=data)
        response_data = self.deserialize(resp)
        self.assertHttpOK(resp)
        self.assertEqual(response_data['objects'][0]['tag_name'], tag_name)

    def test_get_indicator_tag_show_leaf(self):
        tag_name_0 = 'tag1'
        ind_tag_0 = IndicatorTag.objects.create(tag_name=tag_name_0)
        tag_name_1 = 'tag2'
        ind_tag_1 = IndicatorTag.objects.create(
            tag_name=tag_name_1, parent_tag_id=ind_tag_0.id)
        data = {'show_leaf': 1}
        resp = self.ts.get(self, '/api/v1/indicator_tag/', data=data)
        response_data = self.deserialize(resp)
        self.assertHttpOK(resp)
        self.assertEqual(len(response_data['objects']), 1)
        self.assertEqual(response_data['objects'][0]['tag_name'], tag_name_1)

    def test_create_indicator_tag(self):
        tag_name_1 = 'test1'
        data_1 = {
            'tag_name': tag_name_1
        }
        resp = self.ts.post(self, '/api/v1/indicator_tag/', data=data_1)
        response_data = self.deserialize(resp)
        self.assertHttpCreated(resp)
        self.assertEqual(response_data['tag_name'], tag_name_1)
        tag_1_id = int(response_data['id'])
        # now test creating another tag, with tag_1 as its parent
        tag_name_2 = 'test2'
        data_2 = {
            'tag_name': tag_name_2,
            'parent_tag_id': tag_1_id
        }
        resp = self.ts.post(self, '/api/v1/indicator_tag/', data=data_2)
        response_data = self.deserialize(resp)
        self.assertHttpCreated(resp)
        self.assertEqual(response_data['tag_name'], tag_name_2)
        self.assertEqual(response_data['parent_tag_id'], tag_1_id)

    def test_create_indicator_tag_no_vals(self):
        resp = self.ts.post(self, '/api/v1/indicator_tag/')
        self.deserialize(resp)
        self.assertHttpApplicationError(resp)

    def test_get_indicator_tag_no_params(self):
        tag_name_0 = 'tag1'
        ind_tag_0 = IndicatorTag.objects.create(tag_name=tag_name_0)
        tag_name_1 = 'tag2'
        ind_tag_1 = IndicatorTag.objects.create(
            tag_name=tag_name_1, parent_tag_id=ind_tag_0.id)

        resp = self.ts.get(self, '/api/v1/indicator_tag/')
        response_data = self.deserialize(resp)
        self.assertHttpOK(resp)
        self.assertEqual(len(response_data['objects']), 2)
