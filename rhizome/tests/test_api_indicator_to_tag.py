from base_test_case import RhizomeApiTestCase
from rhizome.tests.setup_helpers import TestSetupHelpers
from rhizome.models import IndicatorTag
from rhizome.models import IndicatorToTag


class IndicatorToTagResourceTest(RhizomeApiTestCase):

    def setUp(self):
        super(IndicatorToTagResourceTest, self).setUp()

        self.ts = TestSetupHelpers()

        self.lt = self.ts.create_arbitrary_location_type()
        self.o = self.ts.create_arbitrary_office()

        self.top_lvl_location = self.ts.create_arbitrary_location(
            self.lt.id, self.o.id)
        self.ind_tag = IndicatorTag.objects.create(tag_name='a tag')
        self.ind = self.ts.create_arbitrary_indicator()

    def test_obj_create(self):
        data = {
            'indicator_tag_id': self.ind_tag.id,
            'indicator_id': self.ind.id
        }
        resp = self.ts.post(self, '/api/v1/indicator_to_tag/', data=data)
        response_data = self.deserialize(resp)
        self.assertHttpCreated(resp)
        self.assertEqual(response_data['indicator_id'], self.ind.id)
        self.assertEqual(response_data['indicator_tag_id'], self.ind_tag.id)

    def test_obj_get_ind_id(self):
        ind_to_tag = IndicatorToTag.objects.create(indicator_id=self.ind.id,
                                                   indicator_tag_id=self.ind_tag.id)

        data = {
            'indicator_id': self.ind.id
        }
        resp = self.ts.get(self, '/api/v1/indicator_to_tag/', data=data)
        response_data = self.deserialize(resp)
        self.assertHttpOK(resp)
        self.assertEqual(len(response_data['objects']), 1)
        self.assertEqual(response_data['objects'][0][
                         'id'], IndicatorToTag.objects.all()[0].id)

    def test_obj_get_ind_id_invalid(self):
        data = {
            'indicator_id': 3232
        }
        resp = self.ts.get(self, '/api/v1/indicator_to_tag/', data=data)
        response_data = self.deserialize(resp)
        self.assertEqual(len(response_data['objects']), 0)

    def test_obj_get_ind_tag_id(self):
        ind_to_tag = IndicatorToTag.objects.create(indicator_id=self.ind.id,
                                                   indicator_tag_id=self.ind_tag.id)

        data = {
            'indicator_tag_id': self.ind_tag.id
        }
        resp = self.ts.get(self, '/api/v1/indicator_to_tag/', data=data)
        response_data = self.deserialize(resp)
        self.assertEqual(len(response_data['objects']), 1)
        self.assertEqual(response_data['objects'][0][
                         'id'], IndicatorToTag.objects.all()[0].id)

    def test_obj_get_all(self):
        self.ind_tag_2 = IndicatorTag.objects.create(tag_name='another tag')
        ind_to_tag = IndicatorToTag.objects.create(indicator_id=self.ind.id,
                                                   indicator_tag_id=self.ind_tag.id)

        ind_to_tag_2 = IndicatorToTag.objects.create(indicator_id=self.ind.id,
                                                     indicator_tag_id=self.ind_tag_2.id)
        resp = self.ts.get(self, '/api/v1/indicator_to_tag/')
        response_data = self.deserialize(resp)
        self.assertHttpOK(resp)
        self.assertEqual(len(response_data['objects']), 2)

    def test_obj_delete(self):
        ind_to_tag = IndicatorToTag.objects.create(indicator_id=self.ind.id,
                                                   indicator_tag_id=self.ind_tag.id)
        self.assertEqual(IndicatorToTag.objects.count(), 1)
        delete_url = '/api/v1/indicator_to_tag/%s/' % str(ind_to_tag.id)
        self.ts.delete(self, delete_url)
        self.assertEqual(IndicatorToTag.objects.count(), 0)
