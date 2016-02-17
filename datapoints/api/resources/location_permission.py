from datapoints.api.resources.base_model import BaseModelResource
from datapoints.models import LocationPermission

class LocationPermissionResource(BaseModelResource):
    class Meta(BaseModelResource.Meta):
        resource_name = 'location_responsibility'

    def get_object_list(self, request):

        return LocationPermission.objects\
            .filter(user_id=request.GET['user_id']).values()

    def obj_create(self, bundle, **kwargs):
        '''
        '''

        lp_obj, created = LocationPermission.objects.get_or_create(
            user_id = bundle.data['user_id'], defaults = {
                'top_lvl_location_id' : bundle.data['location_id']
            })

        if not created:
            lp_obj.top_lvl_location_id = bundle.data['location_id']
            lp_obj.save()

        bundle.obj = lp_obj
        bundle.data['id'] = lp_obj.id

        return bundle
