from rhizome.api.resources.base_model import BaseModelResource
from rhizome.models import Indicator, Location, Campaign
from rhizome.models import SourceObjectMap, DocumentSourceObjectMap

class SourceObjectMapResource(BaseModelResource):
    class Meta(BaseModelResource.Meta):
        resource_name = 'source_object_map'

    def obj_create(self, bundle, **kwargs):

        post_data = bundle.data
        som_id = int(post_data['id'])

        som_obj = SourceObjectMap.objects.get(id=som_id)

        master_object_id = post_data['master_object_id']
        som_obj.master_object_id = master_object_id
        som_obj.master_object_name = self.get_master_object_name(som_obj)
        som_obj.mapped_by_id = post_data['mapped_by_id']
        som_obj.save()

        bundle.obj = som_obj
        bundle.data['id'] = som_obj.id
        bundle.data['master_object_name'] = som_obj.master_object_name

        return bundle

    def get_master_object_name(self, som_obj):

        qs_map = {
            'indicator': ['short_name',Indicator.objects.get],
            'location': ['name',Location.objects.get],
            'campaign': ['name',Campaign.objects.get],
        }

        obj_display_field = qs_map[som_obj.content_type][0]
        qs = qs_map[som_obj.content_type][1]
        master_obj = qs(id=som_obj.master_object_id).__dict__
        master_object_name = master_obj[obj_display_field]

        return master_object_name


    def get_object_list(self, request):
        qs =''
        if 'document_id' in request.GET:
            som_ids = DocumentSourceObjectMap.objects \
            .filter(document_id=request.GET['document_id']). \
            values_list('source_object_map_id', flat=True)
            qs = SourceObjectMap.objects.filter(id__in=som_ids,\
            master_object_id=-1).values()
        elif 'id' in request.GET:
            qs = SourceObjectMap.objects.filter(id=request.GET['id']).values()
        else:
            qs = SourceObjectMap.objects.all().values()
        return qs
