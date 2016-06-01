from rhizome.api.resources.base_model import BaseModelResource
from datapoints.models import IndicatorToTag

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

    class Meta(BaseModelResource.Meta):
        # queryset = IndicatorToTag.objects.all().values()
        resource_name = 'indicator_to_tag'

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

    def get_object_list(self, request):

        response_columns = ['id', 'indicator_id', 'indicator_tag_id', \
            'indicator__short_name', 'indicator_tag__tag_name']

        try:
            indicator_id = request.GET['indicator_id']
        except KeyError:
            indicator_id = None

        try:
            indicator_tag_id = request.GET['indicator_tag_id']
        except KeyError:
            indicator_tag_id = None

        if indicator_id:
            qs = IndicatorToTag.objects \
                .filter(indicator_id=indicator_id) \
                .values(*response_columns)
        elif indicator_tag_id:
            qs = IndicatorToTag.objects \
                .filter(indicator_tag_id=indicator_tag_id) \
                .values(*response_columns)
        else:
            qs = IndicatorToTag.objects.all().values(*response_columns)

        return qs

    def obj_delete_list(self, bundle, **kwargs):
        """
        """

        obj_id = int(bundle.request.GET[u'id'])
        IndicatorToTag.objects.filter(id=obj_id).delete()
