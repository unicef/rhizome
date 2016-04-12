import json

from tastypie.resources import ALL

from rhizome.api.resources.base_model import BaseModelResource
from rhizome.models import CustomChart,ChartToDashboard

class CustomChartResource(BaseModelResource):
    '''
    Create, retrieve, or delete a chart resource object
    **GET Requests:**
        - *Required Parameters:* 
            'id'
        - *Errors:*
            If an invalid id is passed, the API returns an empty list of objects and a status code of 200
    **DELETE Requests:**
        - *Required Parameters:* 
            'id'
    **POST Requests:**
        - *Required Parameters:* 
            'uuid', 'title', 'chart_json'
        -*Errors:*
            If any of the required parameters are missing, the API returns a 500 error

    '''
    class Meta(BaseModelResource.Meta):
        resource_name = 'custom_chart'
        queryset =  CustomChart.objects.all()
        filtering = {
            "id": ALL,
        }

    def get_detail(self, request, **kwargs):
        bundle = self.build_bundle(request=request)
        bundle.data = CustomChart.objects.get(id=kwargs['pk']).__dict__

        return self.create_response(request, bundle)

    def obj_create(self, bundle, **kwargs):

        post_data = bundle.data
        chart_json = json.loads(post_data['chart_json'])
        title = post_data['title']
        uuid = post_data['uuid']
        # chart_id = None

        # try:
        #     chart_id = int(post_data['id'])
        # except KeyError:
        #     pass

        defaults = {
            'chart_json': chart_json,
            'title': title
        }

        chart, created = CustomChart.objects.update_or_create(
            uuid=uuid,
            defaults=defaults
        )

        bundle.obj = chart
        bundle.data['id'] = chart.id

        return bundle

    def obj_delete(self, bundle, **kwargs):
        CustomChart.objects.get(id=kwargs['pk']).delete()


    def obj_delete_list(self, bundle, **kwargs):
        """
        """

        obj_id = int(bundle.request.GET[u'id'])
        CustomChart.objects.filter(id=obj_id).delete()

    def get_object_list(self, request):

        chart_id_list = []
        if 'dashboard_id' in request.GET:
            try:
                dashboard_id = request.GET['dashboard_id']
                chart_id_list = ChartToDashboard.objects\
                    .filter(dashboard_id=dashboard_id).values_list('chart_id', flat=True)
            except KeyError:
                pass
        elif 'id' in request.GET['id']:
            try:
                chart_id_list = [request.GET['id']]
            except KeyError:
                pass
        else:
            return CustomChart.objects.all().values()
        return CustomChart.objects.filter(id__in=chart_id_list) \
            .values()
