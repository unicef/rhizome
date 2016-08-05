from rhizome.api.resources.base_model import BaseModelResource
from rhizome.models.office_models import Office


class OfficeResource(BaseModelResource):
    '''
    **GET Request** Returns all office objects
        - *Required Parameters:*
                    None
    '''
    class Meta(BaseModelResource.Meta):
        object_class = Office
        resource_name = 'office'
