from tastypie.resources import ModelResource,Resource, ALL
from tastypie import fields

from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

from datapoints.api.base import BaseApiResource
from datapoints.models import *

import pprint as pp


class OfficeResource(BaseApiResource):
    '''Office Resource'''


    class Meta(BaseApiResource.Meta):
        queryset = Office.objects.all()
        resource_name = 'office'


class RegionResource(ModelResource):
    '''Region Resource'''

    # parent_region = fields.ForeignKey('datapoints.api.meta_data.RegionResource', 'parent_region', full=True, null=True)
    # name = fields.CharField('name')


    class Meta():
        # queryset = Region.objects.raw("Select id, parent_region_id, name from region")
        queryset = SimpleRegion.objects.all()
        resource_name = 'region'
        max_limit = None # return all rows by default ( limit defaults to 20 )
        # paginator_class = CustomPaginator

    def dehydrate(self, bundle):

        bundle.data.pop("resource_uri",None)# = bundle.obj.region.id
        return bundle

class GeoJsonResult(object):
    '''
    This is the same as a row in the CSV export in which one row has a distinct
    region / campaign combination, and the remaing columns represent the
    indicators requested.  Indicators are a list of IndicatorObjects.
    '''
    geo_json = dict()

class RegionPolygonResource(Resource):

    # region_id = fields.ForeignKey(RegionResource,'region')
    geo_json = fields.DictField()

    class Meta(BaseApiResource.Meta):
        # queryset = RegionPolygon.objects.all()
        object_class = GeoJsonResult
        resource_name = 'polygon'
        filtering = {
            "region_id": ALL,
        }

    # def obj_get(self):
    #     # get one object from data source
    #     pk = int(kwargs['pk'])
    #     try:
    #         return data[pk]
    #     except KeyError:
    #         raise NotFound("Object not found")


    def obj_get_list(self,bundle,**kwargs):
        '''
        Outer method for get_object_list... this calls get_object_list and
        could be a point at which additional build_agg_rc_dfing may be applied
        '''

        return self.get_object_list(bundle.request)

    def get_object_list(self,request):

        print 'wuddup\n' * 10
        # results = RegionPolygon.objects.all()
        # region_values_list = RegionPolygon.objects.all().values()
        # pp.pprint(region_values_list)

        # { "type": "FeatureCollection",
        # "features": [
        features = []

        f_1 = { "type": "Feature",
             "geometry": {
               "type": "Polygon",
               "coordinates": [
                 [ [100.0, 0.0], [101.0, 0.0], [101.0, 1.0],
                   [100.0, 1.0], [100.0, 0.0] ]
                 ]
             },
             "properties": { "region_id": 211 }
        }
        f_2 = { "type": "Feature",
             "geometry": {
               "type": "Polygon",
               "coordinates": [
                 [ [100.0, 0.0], [101.0, 0.0], [101.0, 1.0],
                   [100.0, 1.0], [100.0, 0.0] ]
                 ]
             },
             "properties": { "region_id": 122 }
        }

        f1_obj = GeoJsonResult()
        f1_obj.geo_json = f_1

        f2_obj = GeoJsonResult()
        f2_obj.geo_json = f_2

        features.append(f1_obj)
        features.append(f2_obj)

        return features


class IndicatorResource(BaseApiResource):
    '''Indicator Resource'''

    class Meta(BaseApiResource.Meta):
        queryset = Indicator.objects.all()
        resource_name = 'indicator'
        filtering = {
            "slug": ('exact'),
            "id": ALL,
        }

class CampaignResource(BaseApiResource):
    '''Campaign Resource'''

    office = fields.ToOneField(OfficeResource, 'office')


    class Meta(BaseApiResource.Meta):
        queryset = Campaign.objects.all()
        resource_name = 'campaign'
        filtering = {
            "slug": ('exact'),
            "id": ALL,
            "office": ALL,
        }

    def dehydrate(self, bundle):

        bundle.data['office'] = bundle.obj.office.id

        return bundle

class UserResource(BaseApiResource):
    '''User Resource'''

    class Meta(BaseApiResource.Meta):
        queryset = User.objects.all()
        resource_name = 'user'
        excludes = ['password', 'username']
        allowed_methods = ['get']
