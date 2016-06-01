from rhizome.api.resources.base_model import BaseModelResource
from rhizome.models import Indicator, Location, Campaign
from rhizome.models import SourceObjectMap, DocumentSourceObjectMap


class SourceObjectToMapResource(BaseModelResource):
    '''
    '''

    class Meta(BaseModelResource.Meta):
        resource_name = 'source_object_to_map'

    def get_object_list(self, request):

        print '=-obj-=\n' * 5
        qs =''
        if 'document_id' in request.GET:

            som_ids = DocumentSourceObjectMap.objects \
                .filter(document_id=request.GET['document_id']). \
                values_list('source_object_map_id', flat=True)

            qs = SourceObjectMap.objects.filter(id__in=som_ids,\
                master_object_id = -1).values()

        elif 'id' in request.GET:
            qs = SourceObjectMap.objects.filter(id=request.GET['id']).values()
        else:
            qs = SourceObjectMap.objects.all().values()
        return qs
