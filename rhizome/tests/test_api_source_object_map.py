from rhizome.tests.base_test_case import RhizomeApiTestCase

from rhizome.models.office_models import Office
from rhizome.models.campaign_models import Campaign, CampaignType
from rhizome.models.location_models import Location, LocationType, LocationPermission
from rhizome.models.indicator_models import Indicator, IndicatorTag
from rhizome.models.datapoint_models import CacheJob
from rhizome.models.document_models import SourceObjectMap, \
    DocumentSourceObjectMap

from pandas import read_csv
from rhizome.models.indicator_models import Indicator
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

        self.document = self\
            .test_setup.create_arbitrary_document(id=22,file_type ='campaign')
        self.som_0 = SourceObjectMap.objects.create(
            source_object_code='This is not mapped',
            master_object_id = -1,
            content_type = 'location'
        )
        DocumentSourceObjectMap.objects.create(
            document_id = self.document.id,
            source_object_map_id = self.som_0.id
        )


        self.som_1 = SourceObjectMap.objects.create(
            source_object_code='This is mapped',
            master_object_id = self.location.id,
            content_type = 'location'
        )
        DocumentSourceObjectMap.objects.create(
            document_id = self.document.id,
            source_object_map_id = self.som_1.id
        )

        indicator_df = read_csv('rhizome/tests/_data/indicators.csv')
        self.indicators = self.test_setup.model_df_to_data(
            indicator_df, Indicator)

    def test_som_patch(self):
        # this is really a PUT that is i am updating values here in place

        post_data = {
            'source_object_code': 'Percent missed children_PCA',
            'master_object_id': self.indicators[0].id,
            'content_type': 'indicator',
            'mapped_by_id': self.user.id
        }

        patch_url = '/api/v1/source_object_map/%s/' % self.som_0.id
        patch_resp = self.test_setup.patch(self, patch_url, post_data)

        self.assertHttpAccepted(patch_resp)
        response_data = self.deserialize(patch_resp)

        self.assertEqual(
            response_data['master_object_id'], self.indicators[0].id)

    def test_som_post_invalid_id(self):
        '''
        try to PATCH with an invalid id.
        '''

        post_data = {
            'master_object_id': self.indicators[0].id,
            'content_type': 'indicator',
            'mapped_by_id': self.user.id
        }

        post_resp = self.test_setup.patch(
            self, '/api/v1/source_object_map/9090909090/' , post_data)

        self.assertHttpApplicationError(post_resp)

    def test_som_get_id(self):
        '''
        get the som_obj by id for both the mapped and un mapped.
        '''
        ## mapped ##
        get_resp = self.test_setup.get(
            self, '/api/v1/source_object_map/%s/' % self.som_1.id)
        self.assertHttpOK(get_resp)
        response_data = self.deserialize(get_resp)
        self.assertEqual(response_data['master_object_id'], self.location.id)

        ## un mapped ##
        get_resp_1 = self.test_setup.get(
            self, '/api/v1/source_object_map/%s/' % self.som_0.id)
        self.assertHttpOK(get_resp_1)
        response_data_1 = self.deserialize(get_resp_1)
        self.assertEqual(response_data_1['master_object_id'], -1)

    def test_som_get_doc_id(self):
        get_data = {'document_id': self.document.id, 'is_mapped': 1}
        resp = self.test_setup.get(
            self, '/api/v1/source_object_map/', get_data)

        self.assertHttpOK(resp)
        data = self.deserialize(resp)
        self.assertEqual(data['objects'][0]['master_object_id']\
            , self.location.id)

    def test_som_get_no_doc_param(self):
        '''
        the document_id is a required parameter so we need to make sure
        that when we pass a request without a document_id, that we get the
        expected error message.
        '''

        resp = self.test_setup.get(self, '/api/v1/source_object_map/')
        data = self.deserialize(resp)
        self.assertHttpApplicationError(resp)

        # expected_error_msg = 'Missing required parameter document_id'
        expected_error_msg = "'document_id'"
        self.assertEqual(data['error'], str(expected_error_msg))

    def test_som_get_unmapped(self):
        filter_params = {'document_id': self.document.id, 'is_mapped': 0}
        resp = self.test_setup.get(self, '/api/v1/source_object_map/',\
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
