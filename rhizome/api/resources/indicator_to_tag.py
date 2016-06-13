from tastypie import fields
from tastypie.resources import ALL, ALL_WITH_RELATIONS

from rhizome.api.resources.base_model import BaseModelResource
from rhizome.models import IndicatorToTag


class IndicatorToTagResource(BaseModelResource):
    '''
    **GET Request** returns all indicator_to_tag objects, unless one of the optional parameters below is set
        - *Optional Parameters:*
            'indicator_id' return indicator_to_tags with the given indicator_id
            'indicator_tag_id' return indicator_to_tags with the given indicator_tag_id
        - *Errors:*
            if an invalid id is passed, the API returns an empty list of objects
    **POST Request**
        - *Required Parameters:*
            'indicator_id'
            'indicator_tag_id'
        - *Errors:*
            returns a 500 error if a required parameter is not passed
    **DELETE Request**
        - *Required Parameters:*
            'indicator_id'
            'indicator_tag_id'
        - *Errors:*
            returns a 500 error if a required parameter is not passed
    '''

    indicator_id = fields.IntegerField(attribute='indicator_id')
    indicator_tag_id = fields.IntegerField(attribute='indicator_tag_id')

    class Meta(BaseModelResource.Meta):
        # queryset = IndicatorToTag.objects.all().values()
        resource_name = 'indicator_to_tag'
        object_class = IndicatorToTag
        filtering = {
            'id': ALL,
            'indicator_id': ALL_WITH_RELATIONS,
            'indicator_tag_id': ALL_WITH_RELATIONS
        }

    def obj_create(self, bundle, **kwargs):

        indicator_id = bundle.data['indicator_id']
        indicator_tag_id = bundle.data['indicator_tag_id']

        it = IndicatorToTag.objects.create(
            indicator_id=indicator_id,
            indicator_tag_id=indicator_tag_id,
        )

        bundle.obj = it
        bundle.data['id'] = it.id

        return bundle

    def obj_delete_list(self, bundle, **kwargs):
        """
        """

        obj_id = int(bundle.request.GET[u'id'])
        IndicatorToTag.objects.filter(id=obj_id).delete()
