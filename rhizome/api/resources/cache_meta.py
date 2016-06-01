from rhizome.api.resources.base_model import BaseModelResource
from datapoints.models import Office
from rhizome.cache_meta import cache_all_meta

class CacheMetaResource(BaseModelResource):
    def get_object_list(self, request):
        cache_all_meta()

        return Office.objects.all().values()

    class Meta(BaseModelResource.Meta):
        resource_name = 'cache_meta'

