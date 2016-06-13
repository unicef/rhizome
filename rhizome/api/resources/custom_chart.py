import json

from tastypie.resources import ALL

from rhizome.api.resources.base_model import BaseModelResource
from rhizome.api.exceptions import RhizomeApiException
from rhizome.models import CustomChart


class CustomChartResource(BaseModelResource):
    '''
    **GET Requests:** returns charts from the API. If no parameters are given, returns all the charts
        - *Optional Parameters:*
            'id' -- returns the chart with the given id
            'dashboard_id' -- returns a chart associated with the given dashboard id
        - *Errors:*
            If an invalid id is passed, the API returns an empty list of objects and a status code of 200
    **DELETE Requests:**
        - *Required Parameters:*
            'id'
    **POST Requests:**
        - *Required Parameters:*
            'uuid', 'title', 'chart_json'
        - *Errors:*
            If any of the required parameters are missing, the API returns a 500 error

    '''
    class Meta(BaseModelResource.Meta):
        resource_name = 'custom_chart'
        object_class = CustomChart
        required_fields_for_post = ['chart_json','title','uuid']
    
    # def obj_create(self, bundle, **kwargs):
    #
    #     post_data = bundle.data
    #     try:
    #         chart_json = json.loads(post_data['chart_json'])
    #         title = post_data['title']
    #         uuid = post_data['uuid']
    #     except KeyError as error:
    #         raise RhizomeApiException(
    #         message = 'missing required fields... chart_json, title\\\
    #             and uuid are required all required')
    #
    #     defaults = {
    #         'chart_json': chart_json,
    #         'title': title
    #     }
    #
    #     chart, created = CustomChart.objects.update_or_create(
    #         uuid=uuid,
    #         defaults=defaults
    #     )
    #
    #     bundle.obj = chart
    #     bundle.data['id'] = chart.id
    #
    #     return bundle
