from rhizome.api.resources.base_non_model import BaseNonModelResource
from rhizome.models import Office
from rhizome.cache_meta import cache_all_meta

class CacheMetaResource(BaseNonModelResource):

    class Meta(BaseNonModelResource.Meta):
        resource_name = 'cache_meta'
        queryset = Office.objects.all().values()

    def pre_process_data(self, request):
        cache_all_meta()
