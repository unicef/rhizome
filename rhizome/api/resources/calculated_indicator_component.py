from tastypie.resources import ALL

from rhizome.api.resources.base_model import BaseModelResource
from rhizome.models import CalculatedIndicatorComponent


class CalculatedIndicatorComponentResource(BaseModelResource):
    '''
    **GET Request:** Returns a calculated indicator component
        - *Required Parameters:*
            'indicator_id'
        - *Errors:*
            If 'indicator_id' is invalid or not set, the API returns 200 with an empty list
    **DELETE Request:** Delete a calculated indicator component
        - *Required Parameters:*
            'id'
        - *Errors:*
            If and invalid id is supplied, the request returns with 204. If no id parameter is supplied, the status code returned is 500.

    '''

    class Meta(BaseModelResource.Meta):
        object_class = CalculatedIndicatorComponent
        resource_name = 'indicator_calculation'
        required_fields_for_post = ['indicator_id', 'indicator_component_id']
        filtering = {
            "id": ALL,
            "indicator_id": ALL,
            "indicator_component_id": ALL,
        }
