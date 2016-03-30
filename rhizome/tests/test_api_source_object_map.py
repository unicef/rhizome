import json

from tastypie.test import ResourceTestCase
from django.contrib.auth.models import User
from rhizome.models import Office, LocationType, Location, \
    LocationPermission, Campaign, CampaignType, IndicatorTag
from rhizome.cache_meta import LocationTreeCache
from rhizome.models import SourceObjectMap
from pandas import read_csv, notnull
from rhizome.models import *
from setup_helpers import TestSetupHelpers

class SourceObjectMapResourceTest(ResourceTestCase):
    def setUp(self):

        ## instantiate the test client and all other methods ##
        super(SourceObjectMapResourceTest, self).setUp()

        self.test_setup = TestSetupHelpers()
        self.user = self.test_setup.user
        self.lt = self.test_setup.create_arbitrary_location_type()
        self.o = self.test_setup.create_arbitrary_office()
        self.not_allowed_to_see_location = self.test_setup.create_arbitrary_location(self.lt.id, self.o.id)

        self.indicator_map = self.test_setup.create_arbitrary_som(
            source_object_code = 'Percent missed children_PCA', 
            id=21)

        self.test_setup.create_arbitrary_som(
            source_object_code = 'Percent missed due to other reasons', 
            id=24)

        indicator_df = read_csv('rhizome/tests/_data/indicators.csv')
        self.indicators = self.test_setup.model_df_to_data(indicator_df,Indicator)
        
        self.document = self.test_setup.create_arbitrary_document(id=22)

        self.dsom= self.test_setup.create_arbitrary_dsom(self.document.id, self.indicator_map.id, 23)

    #POST changes the master object for an existing source object map.
    #Required fields: 'master_object_id' 'mapped_by_id' 'id'
    def test_som_post(self):
        post_data = {
            'source_object_code': 'Percent missed children_PCA',
            'master_object_id': self.indicators[0].id,
            'id':self.indicator_map.id,
            'content_type': 'indicator',
            'mapped_by_id': self.user.id
        }
        post_resp = self.test_setup.post(self, '/api/v1/source_object_map/', post_data)

        self.assertHttpCreated(post_resp)
        response_data = self.deserialize(post_resp)

        self.assertEqual(response_data['master_object_id'], self.indicators[0].id)

    #POST returns 500 if required field is not included
    def test_som_post_invalid(self):
        post_data = {
            'source_object_code': 'Percent missed children_PCA',
            'id':self.indicator_map.id,
            'content_type': 'indicator',
            'mapped_by_id': self.user.id
        }
        post_resp = self.test_setup.post(self, '/api/v1/source_object_map/', post_data)

        self.assertHttpApplicationError(post_resp)

    #POST returns 500 if master_object_id is invalid
    def test_som_post_invalid_master_obj_id(self):
        post_data = {
            'source_object_code': 'Percent missed children_PCA',
            'master_object_id': 12345,
            'id':self.indicator_map.id,
            'content_type': 'indicator',
            'mapped_by_id': self.user.id
        }
        post_resp = self.test_setup.post(self, '/api/v1/source_object_map/', post_data)
    
        self.assertHttpApplicationError(post_resp)

    #GET requests: if "document_id" is specified, returns a list of Source Object Maps
    #if 'id' field is specified, returns the Source Object Map
    #if neither is specified, returns all of the source object maps

    def test_som_get_id(self):
        get_data ={'id':self.indicator_map.id}
        get_resp = self.test_setup.get(self, '/api/v1/source_object_map/', get_data)

        self.assertHttpOK(get_resp)
        get_data = self.deserialize(get_resp)
        self.assertEqual(get_data['objects'][0]['id'], self.indicator_map.id)
        self.assertEqual(len(get_data['objects']), 1)

    def test_som_get_doc_id(self):
        get_data ={'document_id':self.document.id}
        get_resp = self.test_setup.get(self, '/api/v1/source_object_map/', get_data)

        self.assertHttpOK(get_resp)
        get_data = self.deserialize(get_resp)
        self.assertEqual(get_data['objects'][0]['id'], self.indicator_map.id)

    def test_som_get(self):
        get_resp = self.test_setup.get(self, '/api/v1/source_object_map/')

        self.assertHttpOK(get_resp)
        get_data = self.deserialize(get_resp)
        self.assertEqual(len(get_data['objects']), 2)

    #if GET contains invalid document id or id, returns 200 but with empty object
    def test_som_get_doc_id_invalid(self):
        get_data={'document_id':123456}
        get_resp = self.test_setup.get(self, '/api/v1/source_object_map/', get_data)

        self.assertHttpOK(get_resp)
        get_data = self.deserialize(get_resp)
        self.assertEqual(len(get_data['objects']),0)

    def test_som_get_id_invalid(self):
        get_data={'id':123456}
        get_resp = self.test_setup.get(self, '/api/v1/source_object_map/', get_data)

        self.assertHttpOK(get_resp)
        get_data = self.deserialize(get_resp)
        self.assertEqual(len(get_data['objects']),0)


