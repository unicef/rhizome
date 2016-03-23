from tastypie import fields
from rhizome.api.resources.base_non_model import BaseNonModelResource
from rhizome.models import Indicator, Location, Campaign
import json
from rhizome.api.serialize import CustomSerializer

class AllMetaResult(object):
	content = list()
	name = unicode()
	id= int()

class AllMetaResource(BaseNonModelResource):
    id = fields.IntegerField(attribute='id')
    name = fields.CharField(attribute='name')
    content = fields.ListField(attribute='content')

    class Meta(BaseNonModelResource.Meta):
        object_class = AllMetaResult
        resource_name = 'all_meta'

    def obj_get_list(self, bundle, **kwargs):
        return self.get_object_list(bundle.request)


    def get_object_list(self, request):
        qs = []
    	all_meta_objs ={'indicators': Indicator, 'campaigns':Campaign, 'locations':Location}
    	for idx, (meta_name, meta_resource) in enumerate(all_meta_objs.iteritems()):
            am_result = AllMetaResult()
            am_result.name = meta_name
            am_result.content = meta_resource.objects.all().values()
            am_result.id = idx
            qs.append(am_result)
    	return qs