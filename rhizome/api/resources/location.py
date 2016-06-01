from rhizome.api.resources.base_model import BaseModelResource
from datapoints.models import Location

class LocationResource(BaseModelResource):
    '''
    **GET Request** Returns locations objects. All location objects will be returned if an optional parameter is not set.
        - *Optional Parameters:*
            'location_depth' the recursive depth in relation to the location_id parameter. For instance, a depth of 1 would get all children of that location. 2 would return all "grandchildren"
            'location_type' return the descendants of the location_id param that have the given location_type id.
    '''
    class Meta(BaseModelResource.Meta):
        queryset = Location.objects.all().values()
        resource_name = 'location'

    def get_object_list(self, request):

        location_ids = list(self.get_locations_to_return_from_url(request))
        location_ids.append(self.top_lvl_location_id)
        # Add code to append afhganistan ( for example ) top the list of
        # its own children
        qs = Location.objects.filter(id__in=location_ids).values()

        return qs
