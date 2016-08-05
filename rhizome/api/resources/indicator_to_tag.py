from tastypie import fields
from tastypie.resources import ALL

from rhizome.api.resources.base_model import BaseModelResource
from rhizome.models.indicator_models import IndicatorToTag


class IndicatorToTagResource(BaseModelResource):
    '''
    **GET Request** returns all indicator_to_tag objects, unless one of the
    optional parameters below is set
        - *Optional Parameters:*
            'indicator_id' return indicator_to_tags with the given indicator_id
            'indicator_tag_id' return indicator_to_tags with the given
            indicator_tag_id
        - *Errors:*
            if an invalid id is passed, the API returns an empty list of
            objects
    **POST Request**
        - *Required Parameters:*
            'indicator_id'
            'indicator_tag_id'
        - *Errors:*
            returns a 500 error if a required parameter is not passed
    **DELETE Request**
        - *Required Parameters:*
            'id'
        - *Errors:*
            returns a 500 error if a required parameter is not passed
    '''

    indicator_id = fields.IntegerField(attribute='indicator_id')
    indicator_tag_id = fields.IntegerField(attribute='indicator_tag_id')

    class Meta(BaseModelResource.Meta):
        resource_name = 'indicator_to_tag'
        object_class = IndicatorToTag
        filtering = {
            'id': ALL,
            'indicator_id': ALL,
            'indicator_tag_id': ALL
        }
        required_fields_for_post = ['indicator_id', 'indicator_tag_id']
        GET_fields = ['id', 'indicator_id', 'indicator_tag_id',
                      'indicator__short_name', 'indicator_tag__tag_name']
