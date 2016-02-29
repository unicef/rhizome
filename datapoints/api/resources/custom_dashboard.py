from tastypie.resources import ALL

from datapoints.api.resources.base_model import BaseModelResource
from datapoints.api.exceptions import DatapointsException
from datapoints.models import CustomDashboard, CustomChart

class CustomDashboardResource(BaseModelResource):
    class Meta(BaseModelResource.Meta):
        resource_name = 'custom_dashboard'
        filtering = {
            "id": ALL,
        }
        always_return_data = True

    def obj_create(self, bundle, **kwargs):

        post_data = bundle.data
        user_id = bundle.request.user.id

        try:
            dash_id = int(post_data['id'])
        except KeyError:
            dash_id = None

        default_office_id = 1  # FIXME int(post_data['default_office_id'][0])

        title = post_data['title']

        try:
            description = post_data['description']
        except KeyError:
            description = ''

        try:
            layout = int(post_data['layout'])
        except KeyError:
            layout = 0

        defaults = {
            'id': dash_id,
            'title': title,
            'description': description,
            'default_office_id': default_office_id,
            'layout': layout
        }

        if(CustomDashboard.objects.filter(title=title).count() > 0 and (dash_id is None)):
            raise DatapointsException('the custom dashboard "{0}" already exists'.format(title))

        dashboard, created = CustomDashboard.objects.update_or_create(id=dash_id, defaults=defaults)

        bundle.obj = dashboard
        bundle.data['id'] = dashboard.id
        return bundle

    def obj_delete_list(self, bundle, **kwargs):
        """
        """

        obj_id = int(bundle.request.GET[u'id'])
        CustomChart.objects.filter(dashboard_id=obj_id).delete()
        CustomDashboard.objects.filter(id=obj_id).delete()

    def get_object_list(self, request):
        '''
        '''

        try:
            dash_id = request.GET['id']
            return CustomDashboard.objects.filter(id=dash_id).values()
        except KeyError:
            return CustomDashboard.objects.all().values()
