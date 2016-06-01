from rhizome.api.resources.base_model import BaseModelResource
from datapoints.models import Office

class OfficeResource(BaseModelResource):
	'''
	**GET Request** Returns all office objects
	    - *Required Parameters:* 
			None	
	'''
	class Meta(BaseModelResource.Meta):
	    queryset = Office.objects.all().values()
	    resource_name = 'office'

