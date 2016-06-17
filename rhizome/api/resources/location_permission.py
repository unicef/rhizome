from rhizome.api.resources.base_model import BaseModelResource
from rhizome.models import LocationPermission


class LocationPermissionResource(BaseModelResource):
    '''
    **GET Request** This endpoint tells which locations a user is responsible for.
        - *Required Parameters:*
            'user_id'
        - *Errors*
            API returns a 500 error if a required parameter is not supplied

    **POST Request**
        - *Required Parameters:*
            'user_id'
            'location_id'
        - *Errors*
            API returns a 500 error if a required parameter is not supplied
    '''

    class Meta(BaseModelResource.Meta):
        object_class = LocationPermission
        resource_name = 'location_responsibility'
        required_fields_for_post = ['user_id', 'top_lvl_location_id']

    def apply_filters(self, request, applicable_filters):
        """
        This is not the locations that the logged in user can see,
        these are the locations that appear when you look at a particular
        users page... otherwise we would say u_id  = request.user.id
        """

        applicable_filters['user_id'] = request.GET['user_id']
        return self.get_object_list(request).filter(**applicable_filters)
