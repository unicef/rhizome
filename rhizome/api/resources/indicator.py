import json

from django.http import HttpResponse

from tastypie.resources import ALL
from tastypie.bundle import Bundle
from tastypie.exceptions import ImmediateHttpResponse

from rhizome.api.resources.base_model import BaseModelResource
from rhizome.models.indicator_models import Indicator


class IndicatorResource(BaseModelResource):
    '''
    **GET Request** Returns all indicators
        - *Optional Parameters:*
            'id': return only the id(s) specified
        - *Errors:*
            If an error occurs, the API returns 200 code and an empty list of indicators

    **POST Request** Creates an indicator
        - *Required Parameters:*
            'name, 'short_name', 'description','good_bound', 'bad_bound', 'source_name'
        - *Optional Parameters:*
            'id', 'data_format' (defaults to int)
        - *Errors:*
            if any of the required fields are missing or incorrect, the API returns a 500 error code.
    '''

    class Meta(BaseModelResource.Meta):
        object_class = Indicator
        resource_name = 'indicator'
        filtering = {
            "id": ALL,
            'name': ALL,
            'short_name': ALL,
            'data_format': ALL,
            'source_name': ALL
        }
        required_fields_for_post = ['name', 'short_name', 'data_format']
