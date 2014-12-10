
from tastypie.resources import ALL
from tastypie.bundle import Bundle
from tastypie import fields

from datapoints.models import *
from datapoints.api.meta_data import *
from tastypie.resources import Resource


class ResultObject(object):

    pk = None
    # campaign = None
    # region = None
    # changed_by_id = None
    # indicators = []


class IndicatorObject(object):
    '''
    This object represents the indicators and values for the region/campaign
    combinations.  Within each Result Object, there are N Inidcator objects
    with the attributes listed below.
    '''
    indicator = None
    value = None
    is_agg = None


class DataPointResource(Resource):
    '''
    This Resource is custom and builds upon the tastypie Model Resource by
    overriding the methods coorsponding to GET requests.  For more information
    on creating custom api functionality see :
      https://gist.github.com/nomadjourney/794424
      http://django-tastypie.readthedocs.org/en/latest/non_orm_data_sources.html
    '''

    pk = fields.IntegerField(attribute = 'id')

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
        # https://gist.github.com/nomadjourney/794424
        # return self._build_reverse_url('api_dispatch_detail', kwargs = {})


    def detail_uri_kwargs(self, bundle_or_obj):
            kwargs = {}

            if isinstance(bundle_or_obj, Bundle):
                kwargs['pk'] = bundle_or_obj.obj.pk
            else:
                kwargs['pk'] = bundle_or_obj.pk

            return kwargs

    def get_object_list(self,request):

        results = []


        for result in range(0,5):
            print result

            new_obj = ResultObject()

            new_obj.id = result
            results.append(new_obj)

        return results


    def obj_get_list(self,bundle,**kwargs):
        '''
        Outer method for get_object_list... this calls get_object_list and
        could be a point at which additional filtering may be applied
        '''

        return self.get_object_list(bundle.request)

    def obj_get():
        # get one object from data source
        pk = int(kwargs['pk'])
        try:
            return data[pk]
        except KeyError:
            raise NotFound("Object not found")
