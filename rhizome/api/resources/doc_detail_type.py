from rhizome.api.resources.base_model import BaseModelResource
from source_data.models import DocDetailType

class DocDetailTypeResource(BaseModelResource):
    class Meta(BaseModelResource.Meta):
        queryset = DocDetailType.objects.all().values()
        resource_name = 'doc_detail_type'
