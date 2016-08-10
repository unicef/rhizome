from rhizome.api.resources.base_non_model import BaseNonModelResource
from rhizome.cache_meta import cache_all_meta


class CacheMetaResource(BaseNonModelResource):

    class Meta(BaseNonModelResource.Meta):
        resource_name = 'cache_meta'
        queryset = Campaign.objects.all().values()

    def pre_process_data(self, request):
        cache_all_meta()
