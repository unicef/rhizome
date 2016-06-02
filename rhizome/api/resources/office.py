from tastypie import fields
from rhizome.api.resources.base_non_model import BaseNonModelResource
from datapoints.models import Office

from pprint import pprint

class OfficeResult(object):

	id = int()
	latest_campaign_id = int()
	top_level_location_id = int()

class OfficeResource(BaseNonModelResource):

	id = fields.IntegerField(attribute='id')
	latest_campaign_id = fields.IntegerField(attribute='latest_campaign_id')
	top_level_location_id = fields.IntegerField(attribute='top_level_location_id')

	'''
	**GET Request** Returns all office objects
	    - *Required Parameters:*
			None
	'''
	class Meta(BaseNonModelResource.Meta):
	    # queryset = Office.objects.all().values()
	    resource_name = 'office'

	def obj_get_list(self, bundle, **kwargs):

		return self.get_object_list(bundle.request)

	def get_object_list(self, request):
		'''
		in this 'global' implementation, the top lvl location has the same
		ID as the office, but in an abstraction, you would have to join
		the below query with a query that shows top lvl location for an
		office i.e.:

			SELECT id as location_id, office_id
			FROM location
			WHERE parent_lvl_location_id is null;

		This is used by the homepage to try to determine for what campaigns
		we should show data.
		'''

		results = []
		qs = Office.objects.raw('''
			SELECT DISTINCT ON (office_id)
				office_id as id
				, office_id as top_level_location_id
				, id as latest_campaign_id
			FROM campaign
			ORDER BY office_id, start_date DESC;
		''')

		for o in qs:
			resultObj = OfficeResult()
			resultObj.id = o.id
			resultObj.latest_campaign_id = o.latest_campaign_id
			resultObj.top_level_location_id = o.top_level_location_id
			results.append(resultObj)


		return results
