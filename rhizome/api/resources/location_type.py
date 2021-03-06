from tastypie.resources import ALL

from rhizome.api.resources.base_model import BaseModelResource
from rhizome.models.location_models import LocationType

class LocationTypeResource(BaseModelResource):
    '''
    **GET Request** Returns all location type objects
        - *Required Parameters:*
                    None
    '''

    class Meta(BaseModelResource.Meta):
        queryset = LocationType.objects.all().values()
        resource_name = 'location_type'
        filtering = {
            "id": ALL,
            "admin_level": ALL,
            "name": ALL,
        }
