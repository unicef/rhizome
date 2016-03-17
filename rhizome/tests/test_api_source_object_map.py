import json

from tastypie.test import ResourceTestCase
from django.contrib.auth.models import User
from rhizome.models import Office, LocationType, Location, \
    LocationPermission, Campaign, CampaignType, IndicatorTag
from rhizome.cache_meta import LocationTreeCache
from rhizome.models import SourceObjectMap
from pandas import read_csv, notnull
from rhizome.models import *

class SourceObjectMapResourceTest(ResourceTestCase):
    def setUp(self):

        ## instantiate the test client and all other methods ##
        super(SourceObjectMapResourceTest, self).setUp()

        # Create a user.
        self.username = 'test_user'
        self.password = 'test_password'
        self.user = User.objects\
            .create_user(self.username,'test@test.com', self.password)
        self.lt = LocationType.objects.create(name='test',admin_level = 0)
        self.o = Office.objects.create(name = 'Earth')
        self.not_allowed_to_see_location = Location.objects.create(
                name = 'Somalia',
                location_code = 'Somalia',
                location_type_id = self.lt.id,
                office_id = self.o.id,
            )

        self.indicator_map = SourceObjectMap.objects.create(
            source_object_code = 'Percent missed children_PCA',
            content_type = 'indicator',
            mapped_by_id = self.user.id,
            master_object_id = -1,
            id=21
        )
        indicator_df = read_csv('rhizome/tests/_data/indicators.csv')
        self.indicators = self.model_df_to_data(indicator_df,Indicator)
        
        self.document = Document.objects.create(
        doc_title = 'eoc_post_campaign.csv',
        created_by_id = self.user.id,
        guid = 'test',
        id=22)
        self.document.docfile = 'eoc_post_campaign.csv'
        self.document.save()

        self.dsom= DocumentSourceObjectMap.objects.create(
            document_id = self.document.id,
            source_object_map_id = self.indicator_map.id,
            id=23
        )

    def get_credentials(self):
        result = self.api_client.client.login(username=self.username,
                                              password=self.password)
        return result

    def model_df_to_data(self,model_df,model):
        meta_ids = []

        non_null_df = model_df.where((notnull(model_df)), None)
        list_of_dicts = non_null_df.transpose().to_dict()

        for row_ix, row_dict in list_of_dicts.iteritems():

            row_id = model.objects.create(**row_dict)
            meta_ids.append(row_id)

        return meta_ids


    def test_som_post(self):
        post_data = {
            'source_object_code': 'Percent missed children_PCA',
            'master_object_id': self.indicators[0].id,
            'id':self.indicator_map.id,
            'content_type': 'indicator',
            'mapped_by_id': self.user.id
        }
        post_resp = self.api_client.post('/api/v1/source_object_map/',\
            format='json', data=post_data, authentication=self.get_credentials())

        self.assertHttpCreated(post_resp)
        response_data = self.deserialize(post_resp)

        self.assertEqual(response_data['master_object_id'], self.indicators[0].id)


    def test_som_get_id(self):
        get_data ={'id':self.indicator_map.id}
        get_resp = self.api_client.get('/api/v1/source_object_map/',\
            format='json', data=get_data, authentication=self.get_credentials())

        self.assertHttpOK(get_resp)
        get_data = self.deserialize(get_resp)
        self.assertEqual(get_data['objects'][0]['id'], self.indicator_map.id)


    def test_som_get_doc_id(self):
        get_data ={'document_id':self.document.id}
        get_resp = self.api_client.get('/api/v1/source_object_map/',\
            format='json', data=get_data, authentication=self.get_credentials())

        self.assertHttpOK(get_resp)
        get_data = self.deserialize(get_resp)
        self.assertEqual(get_data['objects'][0]['id'], self.indicator_map.id)

    def test_get_object_list_fail(self):
        get_data={'document_id':123456}
        get_resp = self.api_client.get('/api/v1/source_object_map/',\
            format='json', data=get_data, authentication=self.get_credentials())

        self.assertHttpOK(get_resp)
        get_data = self.deserialize(get_resp)
        self.assertEqual(len(get_data['objects']),0)

