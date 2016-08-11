
from rhizome.tests.base_test_case import RhizomeApiTestCase
from rhizome.tests.setup_helpers import TestSetupHelpers

from rhizome.models.indicator_models import Indicator, IndicatorTag, \
     IndicatorToTag

class IndicatorTagResourceTest(RhizomeApiTestCase):

    def setUp(self):
        super(IndicatorTagResourceTest, self).setUp()

        self.ts = TestSetupHelpers()

        self.lt = self.ts.create_arbitrary_location_type()

        self.top_lvl_location = self.ts.create_arbitrary_location(
            self.lt.id)

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

    def test_update_tag(self):

        IndicatorTag.objects.all().delete()

        tag = IndicatorTag.objects.create(id=None,
                                          tag_name='Test Tag Name', )

        self.assertEqual(IndicatorTag.objects.count(), 1)
        new_tag_name = "New Tag Name"
        patch_data = {"tag_name": new_tag_name}
        resp = self.api_client.patch('/api/v1/indicator_tag/%s/' % tag.id\
            , format='json', data=patch_data\
            , authentication=self.ts.get_credentials(self))

        response_data = self.deserialize(resp)

        self.assertHttpAccepted(resp)
        self.assertEqual(tag.id, response_data['id'])
        self.assertEqual(IndicatorTag.objects.count(), 1)
        self.assertEqual(new_tag_name, response_data['tag_name'])

    def test_remove_tag(self):
        indicatior = Indicator.objects.create(\
            short_name='Test Indicator',
            name='Test Indicator for the Tag',
            data_format='int',
            description='Test Indicator for the Tag Description')

        tag = IndicatorTag.objects.create(tag_name='Test tag')

        IndicatorToTag.objects.all().delete()

        indicatior_tag = IndicatorToTag.objects.create(
            indicator_id=indicatior.id, indicator_tag_id=tag.id)

        self.assertEqual(IndicatorToTag.objects.count(), 1)

        delete_url = '/api/v1/indicator_to_tag/%s/' % str(indicatior_tag.id)

        self.api_client.delete(delete_url, format='json',
            data={}, authentication=self.ts.get_credentials(self))

        self.assertEqual(IndicatorToTag.objects.count(), 0)
