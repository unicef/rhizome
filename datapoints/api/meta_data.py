from tastypie.resources import ALL
from tastypie import fields
from tastypie.bundle import Bundle

from django.contrib.auth.models import User

from datapoints.api.base import BaseModelResource, BaseNonModelResource
from datapoints.models import *

class GeoJsonResult(object):
    region_id = int()
    type = unicode()
    properties = dict()
    geometry = dict()


class RegionPolygonResource(BaseNonModelResource):

    region_id = fields.IntegerField(attribute = 'region_id')
    type = fields.CharField(attribute = 'type')
    properties = fields.DictField(attribute = 'properties')
    geometry = fields.DictField(attribute = 'geometry')

    class Meta(BaseNonModelResource.Meta):
        object_class = GeoJsonResult
        resource_name = 'geo'
        filtering = {
            "region_id": ALL,
        }



    def get_object_list(self,request):
        '''
        parse the url, query the polygons table and do some
        ugly data munging to convert the results from the DB into geojson
        '''

        self.err = None
        err, regions_to_return = self.get_regions_to_return_from_url(request)
        ## since this is not a model resource i will filter explicitly

        if err:
            self.err = err
            return []

        polygon_values_list = RegionPolygon.objects.filter(region_id__in=\
            regions_to_return).values()

        features = []

        for p in polygon_values_list:

            ## this should be cleaned up in the ingestion ##
            ## so i don't need to process data on request ##
            cleaned_shape_list = []
            shape = p["polygon"].replace('\"[[','').replace(']]\"','')
            shape_list = [pt for pt in shape.split('], [')]

            for i,(pt) in enumerate(shape_list):
                lon_lat_list = [float(x.replace('[','').replace(']','')) for x in pt.split(', ')]
                cleaned_shape_list.append(lon_lat_list)

            geo_obj = GeoJsonResult()
            geo_obj.type = "Feature"
            geo_obj.properties = { "region_id": p['region_id'] }
            geo_obj.geometry = { "type": "Polygon", "coordinates": [cleaned_shape_list] }
            features.append(geo_obj)

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
        data['error'] = self.err

        data.pop("objects",None)
        data.pop("meta",None)

        return data


class IndicatorResource(BaseModelResource):
    '''Indicator Resource'''

    class Meta(BaseModelResource.Meta):
        queryset = Indicator.objects.all()
        resource_name = 'indicator'
        filtering = {
            "slug": ('exact'),
            "id": ALL,
        }


class UserResource(BaseModelResource):
    '''User Resource'''

    class Meta(BaseModelResource.Meta):
        queryset = User.objects.all()
        resource_name = 'user'
        excludes = ['password', 'username']
        allowed_methods = ['get']
