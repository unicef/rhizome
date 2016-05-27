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
        resource_name = 'location_responsibility'

    def get_object_list(self, request):

        return LocationPermission.objects\
            .filter(user_id=request.GET['user_id']).values()

    def obj_create(self, bundle, **kwargs):
        '''
        '''

        lp_obj, created = LocationPermission.objects.get_or_create(
            user_id=bundle.data['user_id'], defaults={
                'top_lvl_location_id': bundle.data['location_id']
            })

        if not created:
            lp_obj.top_lvl_location_id = bundle.data['location_id']
            lp_obj.save()

        bundle.obj = lp_obj
        bundle.data['id'] = lp_obj.id

        return bundle
