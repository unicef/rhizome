from tastypie.resources import ALL

from rhizome.api.resources.base_model import BaseModelResource
from rhizome.simple_models import DocumentDetail


class DocumentDetailResource(BaseModelResource):
    '''
    **POST Request**
        - *Required Parameters:*
            'document_id'
            'doc_detail_type_id'
            'doc_detail_value'
        - *Errors:*
            returns 500 error if a required parameter is not supplied
    **GET Request** returns all doc details unless one of the optional parameters is supplied
        - *Optional Parameters:*
            'doc_detail_type' returns all doc details with the given doc detail type supplied
            'document_id' returns all doc details for the given document id
    '''

    class Meta(BaseModelResource.Meta):
        resource_name = 'doc_detail'
        GET_fields = ['id', 'doc_detail_type_id', 'doc_detail_type__name',
            'document_id', 'doc_detail_value']
        required_fields_for_post = ['doc_detail_type_id', 'document_id',\
            'doc_detail_value']
        object_class = DocumentDetail
        filtering = {
            "id": ALL,
            "document": ALL,
        }
