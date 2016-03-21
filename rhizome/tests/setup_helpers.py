import json

from tastypie.test import ResourceTestCase
from django.contrib.auth.models import User
from rhizome.models import Office, LocationType, Location, \
    LocationPermission, Campaign, CampaignType, IndicatorTag
from rhizome.cache_meta import LocationTreeCache
from rhizome.models import SourceObjectMap
from pandas import read_csv, notnull
from rhizome.models import *
from rhizome.etl_tasks.simple_upload_transform import SimpleDocTransform

class TestSetupHelpers(ResourceTestCase):

	def __init__(self):
		self.username = "test_user" 
		self.password = "test_password" 
		self.user = User.objects\
            .create_user(self.username,'test@test.com', self.password)  

	def get_credentials(self, test_class):
		result = test_class.api_client.client.login(username=self.username, password=self.password)
		return result

	def create_arbitrary_office(self, name='Earth'):
		return Office.objects.create(name = name)

   	def create_arbitrary_location_type(self):
   		return LocationType.objects.create(name='test',admin_level = 0)

   	def create_arbitrary_location(self, location_type_id, office_id, location_name='Somalia', location_code='Somalia', parent_location_id=None):
   		if parent_location_id:
	   		return Location.objects.create(
	                name = location_name,
	                location_code = location_code,
	                location_type_id = location_type_id,
	                office_id = office_id,
	                parent_location_id=parent_location_id
	            )
   		else:
   			return Location.objects.create(
	                name = location_name,
	                location_code = location_code,
	                location_type_id = location_type_id,
	                office_id = office_id
	            )

   	def create_arbitrary_som(self, source_object_code='Percent missed children_PCA', id=None):
   		if id:
   			return SourceObjectMap.objects.create(
	            source_object_code = source_object_code,
	            content_type = 'indicator',
	            mapped_by_id = self.user.id,
	            master_object_id = -1,
	            id=id
	        )
   		else:
   			return SourceObjectMap.objects.create(
	            source_object_code = source_object_code,
	            content_type = 'indicator',
	            mapped_by_id = self.user.id,
	            master_object_id = -1
	        )

	def create_arbitrary_document(self, document_docfile='eoc_post_campaign.csv', id=None):
		document =""
		if id:
			document = Document.objects.create(
	        doc_title = 'eoc_post_campaign.csv',
	        created_by_id = self.user.id,
	        guid = 'test',
	        id=id)
		else:
			document = Document.objects.create(
	        doc_title = 'eoc_post_campaign.csv',
	        created_by_id = self.user.id,
	        guid = 'test')
	 	document.docfile = document_docfile
	 	document.save()
	 	return document

	def create_arbitrary_dsom(self, document_id, som_id, id=None):
		if id:
			return DocumentSourceObjectMap.objects.create(
            document_id = document_id,
            source_object_map_id = som_id,
            id=23)
		else:
			return DocumentSourceObjectMap.objects.create(
            document_id = document_id,
            source_object_map_id = som_id)

	def post(self, test_class, uri, data=None):
		if data:
			return test_class.api_client.post(uri,\
    			format ='json', data=data, authentication= self.get_credentials(test_class))
		else:
			return test_class.api_client.post(uri,\
    			format ='json', authentication= self.get_credentials(test_class))

	def get(self, test_class, uri, data=None):
		if data:
			return test_class.api_client.get(uri,\
    			format ='json', data=data, authentication= self.get_credentials(test_class))
		else:
			return test_class.api_client.get(uri,\
    			format ='json', data=data, authentication= self.get_credentials(test_class))

	def model_df_to_data(self,model_df,model):
		meta_ids = []
		non_null_df = model_df.where((notnull(model_df)), None)
		list_of_dicts = non_null_df.transpose().to_dict()
		for row_ix, row_dict in list_of_dicts.iteritems():
			row_id = model.objects.create(**row_dict)
			meta_ids.append(row_id)
		return meta_ids

	def create_arbitrary_campaign(self, office_id, campaign_type_id, location_id, indicator_tag_id, name="test"):
		return Campaign.objects.create(
            start_date = '2016-01-01',
            end_date = '2016-01-01',
            office_id = office_id,
            campaign_type_id = campaign_type_id,
            top_lvl_location_id = location_id,
            top_lvl_indicator_tag_id = indicator_tag_id,
            name=name
        )

 	def create_arbitrary_indicator(self, name='test', short_name="test2"):
 		return Indicator.objects.create(short_name=short_name, \
            name=name, \
            description='Test Indicator for the Tag 2 Description')

	def ingest_file(self, file_name):
		document = Document.objects.create(
        	doc_title = file_name,
        	created_by_id = self.user.id,
        	guid = 'test')
		document.docfile = file_name
		document.save()
		sdt = SimpleDocTransform(self.user.id, document.id)
		sdt.main()
		return document.id




