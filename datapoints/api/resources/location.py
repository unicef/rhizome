from datapoints.api.resources.base_model import BaseModelResource
from datapoints.api.functions import get_locations_to_return_from_url
from datapoints.models import Location

class LocationResource(BaseModelResource):
    class Meta(BaseModelResource.Meta):
        queryset = Location.objects.all().values()
        resource_name = 'location'

    def get_object_list(self, request):

        if self.top_lvl_location_id == 4721:
            return Location.objects.exclude(id = 4721).order_by('location_type_id').values()

        location_ids = list(get_locations_to_return_from_url(request))
        location_ids.append(self.top_lvl_location_id)
        # Add code to append afhganistan top the list of its own children
        qs = Location.objects.filter(id__in=location_ids).values()

        return qs

