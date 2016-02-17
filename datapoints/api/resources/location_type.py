from datapoints.api.resources.base_model import BaseModelResource
from datapoints.models import LocationType

class LocationTypeResource(BaseModelResource):
    class Meta(BaseModelResource.Meta):
        queryset = LocationType.objects.all().values()
        resource_name = 'location_type'

