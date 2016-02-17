from datapoints.api.resources.base_model import BaseModelResource
from datapoints.models import Office

class OfficeResource(BaseModelResource):
    class Meta(BaseModelResource.Meta):
        queryset = Office.objects.all().values()
        resource_name = 'office'

