from rhizome.api.resources.base_model import BaseModelResource
from rhizome.models import Indicator, Location, Campaign
from rhizome.models import SourceObjectMap, DocumentSourceObjectMap


class SourceObjectMapResource(BaseModelResource):
    '''
    **GET Request** Returns all Source Object Maps
        - *Optional Parameters:*
            'id': return only the id(s) specified
            'document_id': returns only Source Object Maps associated with the given document id(s)
        - *Errors:*
            If an error occurs, the API returns 200 code and an empty list of Source Object Maps
    **POST Request** Changes the master object for an existing source object map
        - *Required Parameters:*
           'master_object_id' 'mapped_by_id' 'id'
        - *Errors:*
            if any of the required fields are missing or incorrect, the API returns a 500 error code.
    '''
    class Meta(BaseModelResource.Meta):
        object_class = SourceObjectMap
        resource_name = 'source_object_map'
        required_fields_for_post = ['content_type','source_object_code',\
            'mapped_by_id']

    def get_object_list(self, request):

        qs = ''
        if 'document_id' in request.GET:

            som_ids = DocumentSourceObjectMap.objects \
                .filter(document_id=request.GET['document_id']). \
                values_list('source_object_map_id', flat=True)

            qs = SourceObjectMap.objects.filter(id__in=som_ids,
                                                master_object_id__gt=0).values()

        elif 'id' in request.GET:
            qs = SourceObjectMap.objects.filter(id=request.GET['id']).values()

        else:
            qs = SourceObjectMap.objects.all().values()
        return qs
