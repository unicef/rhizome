from tastypie.resources import ModelResource,Resource, ALL
from tastypie import fields

from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

from datapoints.api.base import BaseApiResource
from datapoints.models import *

class OfficeResource(BaseApiResource):
    '''Office Resource'''


    class Meta(BaseApiResource.Meta):
        queryset = Office.objects.all()
        resource_name = 'office'


class RegionResource(ModelResource):
    '''Region Resource'''

    # parent_region = fields.ForeignKey('datapoints.api.meta_data.RegionResource', 'parent_region', full=True, null=True)
    # name = fields.CharField('name')
    region_type_id = fields.IntegerField(attribute='region_type_id')



    class Meta():
        # queryset = Region.objects.raw("Select id, parent_region_id, name from region")
        queryset = SimpleRegionExtra.objects.all()
        resource_name = 'region'
        max_limit = None # return all rows by default ( limit defaults to 20 )
        # paginator_class = CustomPaginator

    def dehydrate(self, bundle):

        bundle.data.pop("resource_uri",None)# = bundle.obj.region.id
        return bundle

class GeoJsonResult(object):
    region_id = int()
    type = unicode()
    properties = dict()
    geometry = dict()


class RegionPolygonResource(Resource):

    region_id = fields.IntegerField(attribute = 'region_id')
    type = fields.CharField(attribute = 'type')
    properties = fields.DictField(attribute = 'properties')
    geometry = fields.DictField(attribute = 'geometry')

    class Meta(BaseApiResource.Meta):
        object_class = GeoJsonResult
        resource_name = 'geo'
        filtering = {
            "region_id": ALL,
        }

    def get_object_list(self,request):
        '''
        parse the region_id__in parameter, query the polygons table and do some
        ugly data munging to convert the results from the DB into geojson
        '''

        ## since this is not a model resource i will filter explicitly
        try:
            region_id__in = [int(r) for r in request.GET['region_id__in']\
                .split(',')]

            polygon_values_list = RegionPolygon.objects.filter(region_id__in=\
                region_id__in).values()

        except KeyError:
            polygon_values_list = RegionPolygon.objects.all().values()

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
