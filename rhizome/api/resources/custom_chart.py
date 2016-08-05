import json

from tastypie.resources import ALL

from rhizome.api.resources.base_model import BaseModelResource
from rhizome.api.exceptions import RhizomeApiException
from rhizome.simple_models import CustomChart


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
