from rhizome.api.resources.base_model import BaseModelResource
from rhizome.models import Office

class OfficeResource(BaseModelResource):
    class Meta(BaseModelResource.Meta):
        queryset = Office.objects.all().values()
        resource_name = 'office'

