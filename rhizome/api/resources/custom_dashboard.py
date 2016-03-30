from tastypie.resources import ALL

from rhizome.api.resources.base_model import BaseModelResource
from rhizome.api.exceptions import DatapointsException
from rhizome.models import CustomDashboard, CustomChart, ChartToDashboard

import json

class CustomDashboardResource(BaseModelResource):
    class Meta(BaseModelResource.Meta):
        resource_name = 'custom_dashboard'
        filtering = {
            "id": ALL,
        }
        always_return_data = True

    def get_detail(self, request, **kwargs):

        requested_id = kwargs['pk']

        bundle = self.build_bundle(request=request)

        response_data = CustomDashboard.objects.get(id=requested_id).__dict__
        response_data.pop('_state')

        chart_data = []
        for c in CustomChart.objects\
            .filter(charttodashboard__dashboard_id = requested_id)\
            .values():
                c['chart_json'] = json.loads(c['chart_json'])
                chart_data.append(c)

        response_data['charts'] = chart_data
        bundle.data = response_data

        return self.create_response(request, bundle)

    def obj_create(self, bundle, **kwargs):

        post_data = bundle.data
        user_id = bundle.request.user.id

        try:
            dash_id = int(post_data['id'])
        except KeyError:
            dash_id = None

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
            'layout': layout
        }

        if(CustomDashboard.objects.filter(title=title).count() > 0 and (dash_id is None)):
            raise DatapointsException('the custom dashboard "{0}" already exists'.format(title))

        dashboard, created = CustomDashboard.objects.update_or_create(id=dash_id, defaults=defaults)

        bundle.obj = dashboard
        bundle.data['id'] = dashboard.id

        ## optionally add charts to the dashboard ##
        try:
            chart_uuids = post_data['chart_uuids']
            self.upsert_chart_uuids(dashboard.id, chart_uuids)
        except KeyError:
            pass

        return bundle

    def upsert_chart_uuids(self, dashboard_id, chart_uuids):

        chart_ids = CustomChart.objects.filter(uuid__in = [chart_uuids])\
            .values_list('id',flat=True)

        batch = [ChartToDashboard(**{
            'chart_id': c_id,
            'dashboard_id': dashboard_id
        }) for c_id in chart_ids]

        ChartToDashboard.objects.filter(dashboard_id = dashboard_id).delete()
        ChartToDashboard.objects.bulk_create(batch)

    def obj_delete_list(self, bundle, **kwargs):
        """
        """

        obj_id = int(bundle.request.GET[u'id'])
        CustomDashboard.objects.filter(id=obj_id).delete()

    def get_object_list(self, request):
        '''
        '''

        try:
            dash_id = request.GET['id']
            return CustomDashboard.objects.filter(id=dash_id).values()
        except KeyError:
            return CustomDashboard.objects.all().values()
