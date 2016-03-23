from tastypie import fields
from rhizome.api.resources.base_non_model import BaseNonModelResource
from rhizome.models import Indicator, Location, Campaign
import json
from rhizome.api.serialize import CustomSerializer

class AllMetaResult(object):
    indicators = list()
    campaigns = list()
    locations = list()


class AllMetaResource(BaseNonModelResource):
    indicators = fields.ListField(attribute='indicators')
    campaigns = fields.ListField(attribute='campaigns')
    locations = fields.ListField(attribute='locations')
    class Meta(BaseNonModelResource.Meta):
        object_class = AllMetaResult
        resource_name = 'all_meta'

    def obj_get_list(self, bundle, **kwargs):
        return self.get_object_list(bundle.request)


    def get_object_list(self, request):
        qs = []
        am_result = AllMetaResult()
        am_result.indicators = Indicator.objects.all().values()
        am_result.campaigns = Campaign.objects.all().values()
        am_result.locations = Location.objects.all().values()
        qs.append(am_result)
        return qs