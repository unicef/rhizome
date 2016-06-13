from rhizome.api.resources.base_model import BaseModelResource
from rhizome.models import DocDetailType


class DocDetailTypeResource(BaseModelResource):
    '''
    **GET Request** Returns all doc_detail_type objects
        - *Required Parameters:*
                    None
    '''
    class Meta(BaseModelResource.Meta):
        object_class = DocDetailType
        resource_name = 'doc_detail_type'
