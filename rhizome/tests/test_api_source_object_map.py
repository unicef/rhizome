from base_test_case import RhizomeApiTestCase
from rhizome.models import Office, LocationType, Location, \
    LocationPermission, Campaign, CampaignType, IndicatorTag, SourceObjectMap,\
    DocumentSourceObjectMap
from pandas import read_csv
from rhizome.models import Indicator
from rhizome.tests.setup_helpers import TestSetupHelpers


class SourceObjectMapResourceTest(RhizomeApiTestCase):

    def setUp(self):

        ## instantiate the test client and all other methods ##
        super(SourceObjectMapResourceTest, self).setUp()

        self.test_setup = TestSetupHelpers()
        self.user = self.test_setup.user
        self.lt = self.test_setup.create_arbitrary_location_type()
        self.o = self.test_setup.create_arbitrary_office()
        self.location = \
            self.test_setup.create_arbitrary_location(self.lt.id, self.o.id)

        self.document = self.test_setup.create_arbitrary_document(id=22)
        som_0 = SourceObjectMap.objects.create(
            source_object_code='This is not mapped',
            master_object_id = -1,
            content_type = 'location'
        )
        DocumentSourceObjectMap.objects.create(
            document_id = self.document.id,
            source_object_map_id = som_0.id
        )


        som_1 = SourceObjectMap.objects.create(
            source_object_code='This is mapped',
            master_object_id = self.location.id,
            content_type = 'location'
        )
        DocumentSourceObjectMap.objects.create(
            document_id = self.document.id,
            source_object_map_id = som_1.id
        )

        indicator_df = read_csv('rhizome/tests/_data/indicators.csv')
        self.indicators = self.test_setup.model_df_to_data(
            indicator_df, Indicator)





    def test_som_post(self):
        # this is really a PUT that is i am updating values here in place

        post_data = {
            'source_object_code': 'Percent missed children_PCA',
            'master_object_id': self.indicators[0].id,
            'id': self.indicator_map.id,
            'content_type': 'indicator',
            'mapped_by_id': self.user.id
        }

        post_resp = self.test_setup.post(
            self, '/api/v1/source_object_map/', post_data)

        self.assertHttpCreated(post_resp)
        response_data = self.deserialize(post_resp)

        self.assertEqual(
            response_data['master_object_id'], self.indicators[0].id)

    def test_som_post_invalid_id(self):
        # this is really a PUT that is i am updating values here in place

        post_data = {
            'master_object_id': self.indicators[0].id,
            'id': 9090909090,
            'content_type': 'indicator',
            'mapped_by_id': self.user.id
        }

        post_resp = self.test_setup.post(
            self, '/api/v1/source_object_map/', post_data)

        self.assertHttpApplicationError(post_resp)

    def test_som_get_id(self):
        get_resp = self.test_setup.get(
            self, '/api/v1/source_object_map/%s/' % self.indicator_map.id)
        self.assertHttpOK(get_resp)
        response_data = self.deserialize(get_resp)
        self.assertEqual(response_data['id'], self.indicator_map.id)

    def test_som_get_doc_id(self):
        get_data = {'document_id': self.document.id}
        resp = self.test_setup.get(
            self, '/api/v1/source_object_map/', get_data)
        self.assertHttpOK(resp)
        data = self.deserialize(resp)
        self.assertEqual(get_data['objects'][0]['id'], self.indicator_map.id)

    def test_som_get(self):
        get_resp = self.test_setup.get(self, '/api/v1/source_object_map/')
        get_data = self.deserialize(get_resp)
        self.assertHttpOK(get_resp)
        self.assertEqual(len(get_data['objects']), 2)

    def test_som_get_unmapped(self):
        filter_params = {'document_id': self.document.id}
        resp = self.test_setup.get(self, '/api/v1/source_object_to_map/',\
            data = filter_params)
        self.assertHttpOK(resp)

        data = self.deserialize(resp)
        data_objects = data['objects']

        self.assertEqual(len(data_objects), 1) # since we created one unmapped
        self.assertEqual(data_objects[0]['master_object_id'], -1)
        self.assertEqual(str(data_objects[0]['source_object_code']),\
            'This is not mapped')

    def test_som_get_doc_id_invalid(self):
        get_data = {'document_id': 123456}
        get_resp = self.test_setup.get(
            self, '/api/v1/source_object_map/', get_data)

        self.assertHttpOK(get_resp)
        get_data = self.deserialize(get_resp)

    def test_som_get_id_invalid(self):
        get_data_id = 123456
        get_resp = self.test_setup.get(
            self, '/api/v1/source_object_map/%s/' % get_data_id)

        self.assertHttpApplicationError(get_resp)
        get_data = self.deserialize(get_resp)
