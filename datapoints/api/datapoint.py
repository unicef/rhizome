
from tastypie.resources import ALL
from tastypie.bundle import Bundle
from tastypie import fields

from datapoints.models import *
from datapoints.api.base import BaseApiResource
from datapoints.api.meta_data import *

class ResultObject(object):

    id = None
    # campaign = None
    # region = None
    # changed_by_id = None
    # indicators = []


class DataPointResource(BaseApiResource):
    '''Datapoint Resource'''

    id = fields.IntegerField(attribute = 'id')

    # region = fields.ToOneField(RegionResource, 'region')
    # indicator = fields.ToOneField(IndicatorResource, 'indicator')
    # campaign = fields.ToOneField(CampaignResource, 'campaign')
    # changed_by_id = fields.ToOneField(UserResource, 'changed_by')


    class Meta(BaseApiResource.Meta):
        # queryset = DataPoint.objects.all()
        # object_class = ResultObject
        resource_name = 'datapoint'
        excludes = ['note']
        filtering = {
            "value": ALL,
            "created_at":ALL,
            "indicator":ALL,
            "region": ALL ,
            "campaign": ALL,
        }
        # serializer = CustomSerializer()
        max_limit = None


    # def get_resource_uri(self, bundle_or_obj):
    #     kwargs = {
    #         'resource_name': self._meta.resource_name,
    #     }
    #
    #     if isinstance(bundle_or_obj, Bundle):
    #         kwargs['pk'] = bundle_or_obj.obj.id # pk is referenced in ModelResource
    #     else:
    #         kwargs['pk'] = bundle_or_obj.id
    #
    #     if self._meta.api_name is not None:
    #         kwargs['api_name'] = self._meta.api_name
    #
    #     return self._build_reverse_url('api_dispatch_detail', kwargs = kwargs)


    def detail_uri_kwargs(self, bundle_or_obj):
            kwargs = {}

            if isinstance(bundle_or_obj, Bundle):
                kwargs['pk'] = bundle_or_obj.obj.id
            else:
                kwargs['pk'] = bundle_or_obj.id

            return kwargs

    def get_object_list(self,request):

        results = []

        for result in range(0,10):
            print result

            new_obj = ResultObject()

            new_obj.id = result
            results.append(new_obj)

        return results


    def obj_get_list(self,bundle,**kwargs):

        return self.get_object_list(bundle.request)

    # def obj_get():
