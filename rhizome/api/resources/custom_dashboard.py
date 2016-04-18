from tastypie.resources import ALL

from rhizome.api.resources.base_model import BaseModelResource
from rhizome.api.exceptions import DatapointsException
from rhizome.models import CustomDashboard, CustomChart, ChartToDashboard

import json

class CustomDashboardResource(BaseModelResource):
    '''
    **GET Requests:** Get a dashboard. If no params are passed, returns all the dashboards
        - *Optional Parameters:*
            'id'
    **GET Request get detail:**
        - to access a specific chart, send a get request to /api/v1/custom_dashboard/<dashboard_id>/
    **POST Requests:** Create a dashboard
        - *Required Parameters:*
            'title'
        - *Optional Parameters:*
            'chart_uuids': this associates the given chart() with a dashboard
        - *Errors:*
            If a title is not supplied. The API will return a 500 error.
    **DELETE Requests:** There are two ways to submit a delete request to API
        - to delete a resource, HTTP delete request to /api/v1/custom_dashboard/<dashboard_id>/
        - or delete request to /api/v1/custom_dashboard/ with param 'id'
    '''
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

        if response_data['rows']:
            response_data_rows = response_data['rows']
            chart_uuids = response_data_rows[0]['charts']
            charts = list(CustomChart.objects.filter(uuid__in = chart_uuids))

            # create a dict to get random access
            charts_dict ={}
            for chart in charts:
                chart_dict = chart.__dict__
                chart_dict.pop('_state')
                charts_dict[chart.uuid] = chart_dict
            # add the charts to the row in the response
            for idx, row in enumerate(response_data_rows):
                charts_list = row['charts']
                for idx2, chart_uuid in enumerate(charts_list):
                    if chart_uuid in charts_dict.keys():
                        chart = charts_dict[chart_uuid]
                        response_data_rows[idx]['charts'][idx2] = chart
            response_data['rows'] = response_data_rows
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

        try:
            rows = json.loads(post_data['rows'])
        except KeyError:
            rows =None

        defaults = {
            'id': dash_id,
            'title': title,
            'description': description,
            'layout': layout,
            'rows': rows
        }

        if(CustomDashboard.objects.filter(title=title).count() > 0 and (dash_id is None)):
            raise DatapointsException('the custom dashboard "{0}" already exists'.format(title))

        dashboard, created = CustomDashboard.objects.update_or_create(id=dash_id, defaults=defaults)

        bundle.obj = dashboard
        bundle.data['id'] = dashboard.id

        ## optionally add charts to the dashboard ##
        try:
            chart_uuids = post_data['chart_uuids']
            self.upsert_chart_uuids(dashboard.id, chart_uuids.split(','))
        except KeyError:
            pass

        return bundle

    def upsert_chart_uuids(self, dashboard_id, chart_uuids):

        chart_ids = CustomChart.objects.filter(uuid__in = chart_uuids)\
            .values_list('id',flat=True)

        batch = [ChartToDashboard(**{
            'chart_id': c_id,
            'dashboard_id': dashboard_id
        }) for c_id in chart_ids]

        ChartToDashboard.objects.filter(dashboard_id = dashboard_id).delete()
        ChartToDashboard.objects.bulk_create(batch)

    def obj_delete_list(self, bundle, **kwargs):
        obj_id = int(bundle.request.GET[u'id'])
        CustomDashboard.objects.filter(id=obj_id).delete()

    def obj_delete(self, bundle, **kwargs):
        CustomDashboard.objects.get(id=kwargs['pk']).delete()

    def get_object_list(self, request):
        if 'id' in request.GET:
            dash_id = request.GET['id']
            return CustomDashboard.objects.filter(id=dash_id).values()
        else:
            return CustomDashboard.objects.all().values()
