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

    def get_object_list(self, request):
        '''
        In this resoruce we only override the get_object_list method so that
        we return only the top level location data that the user can see.
        '''
        return LocationPermission.objects\
            .filter(user_id=request.GET['user_id']).values()
