from tastypie.resources import ALL

from rhizome.api.resources.base_model import BaseModelResource
from rhizome.models import IndicatorTag


class IndicatorTagResource(BaseModelResource):
    '''
    **GET Request** Returns all indicator tags
        - *Optional Parameters:*
            'show_leaf'only return leaf level nodes of the indicator_tag tree
            'id' return the indicator_tag associated with the given id
        - *Errors:*

    **POST Request** Creates an indicator tag
        - *Required Parameters:*
            'tag_name'
        - *Optional Parameters:*
            'parent_tag_id'
        - *Errors:*
            if a required parameter is not supplied, the API will return a 500 error
    '''

    class Meta(BaseModelResource.Meta):
        GET_fields = ['id', 'parent_tag_id', 'tag_name', 'parent_tag__tag_name']
        object_class = IndicatorTag
        resource_name = 'indicator_tag'
        filtering = {
            'id': ALL,
            'tag_name': ALL,
            'parent_tag_id':ALL
        }
        required_fields_for_post = ['tag_name']


    def apply_filters(self, request, applicable_filters):
        """
        """

        try:
            request.GET['show_leaf']
            applicable_filters['parent_tag_id__gt'] = 0
        except KeyError:
            pass

        return self.get_object_list(request).filter(**applicable_filters)
