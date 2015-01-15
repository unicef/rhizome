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
    type = fields.CharField(attribute = 'type')
    properties = fields.DictField(attribute = 'properties')
    geometry = fields.DictField(attribute = 'geometry')

    class Meta(BaseApiResource.Meta):
        # queryset = RegionPolygon.objects.all()
        object_class = GeoJsonResult
        resource_name = 'polygon'
        filtering = {
            "region_id": ALL,
        }

    def get_object_list(self,request):

        # results = RegionPolygon.objects.all()
        # region_values_list = RegionPolygon.objects.all().values()
        # pp.pprint(region_values_list)

        # { "type": "FeatureCollection",
        # "features": [
        features = []

        f_1 = {"type": "Feature",
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
        f1_obj.type = f_1['type']
        f1_obj.properties = f_1['properties']
        f1_obj.geometry = f_1['geometry']

        f2_obj = GeoJsonResult()
        f2_obj.type = f_1['type']
        f2_obj.properties = f_1['properties']
        f2_obj.geometry = f_1['geometry']

        features.append(f1_obj)
        features.append(f2_obj)

        return features

    def obj_get_list(self,bundle,**kwargs):
        '''
        Outer method for get_object_list... this calls get_object_list and
        could be a point at which additional build_agg_rc_dfing may be applied
        '''

        return self.get_object_list(bundle.request)


    def dehydrate(self, bundle):

        bundle.data.pop("resource_uri",None)# = bundle.obj.region.id
        return bundle

    def alter_list_data_to_serialize(self, request, data):
        '''
        If there is an error for this resource, add that to the response.  If
        there is no error, than add this key, but set the value to null.  Also
        add the total_count to the meta object as well
        '''
        ## get rid of the meta_dict. i will add my own meta data.
        data['type'] = "FeatureCollection"
        data['features'] = data['objects']

        data.pop("objects",None)
        data.pop("meta",None)

        return data



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
