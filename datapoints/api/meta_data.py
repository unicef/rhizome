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


    class Meta():
        queryset = SimpleRegion.objects.all()
        resource_name = 'region'
        max_limit = None # return all rows by default ( limit defaults to 20 )

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


    def parse_url_strings(self,query_dict):

        self.region__in, self.region_type_id, self.parent_region__in = \
            None, None, None

        ## REGION_ID
        try:
            self.region__in = [int(r) for r in query_dict['region__in']\
                .split(',')]
        except KeyError:
            pass

        ## REGION TYPE ##
        try:

            self.region_type_id = RegionType.objects.get(name = query_dict\
                ['region_type']).id

        except KeyError:
            pass

        except ObjectDoesNotExist:

            all_r_types = RegionType.objects.all().values_list('name',flat=True)

            err = 'region type doesnt exist. options are' + str(all_r_types)

            return err, []


        try:
            self.parent_region__in = [int(r) for r in query_dict['parent_region__in']\
                .split(',')]
        except KeyError:
            pass

        return None

    def get_regions_to_return_from_url(self,request):
        '''
        1  region__in returns geo data for the regions requested
        2. parent_region__in + level should return the shapes for all the child
           regions at the specified level that are within the region specified
        3. passing only parent_region__in  should return the shapes for all the
           immediate children in that region if no level parameter is supplied
        3. any request for which there is no geo data, return an empty feature
           collection
        4. no params - return top 10 regions
        '''

        ## attach these to self and return only error #
        err = self.parse_url_strings(request.GET)

        if err:
            self.err = err
            return err, []

        ## CASE 1 ##
        if self.region__in is not None:

            region_ids = Region.objects.filter(id__in = self.region__in)\
                .values_list('id',flat=True)


        ## CASE 2 ##
        elif self.parent_region__in is not None and self.region_type_id is not None:

            region_ids = RegionHeirarchy.objects.filter(
                contained_by_region_id__in = self.parent_region__in, \
                region_type_id = self.region_type_id)\
                .values_list('region_id',flat=True)

        ## CASE 3 #
        elif self.parent_region__in is not None and self.region_type_id is None:

            region_ids = Region.objects.filter(parent_region__in = \
                self.parent_region__in)

        else:
            region_ids = Region.objects.all().values_list('id',flat=True)[:5]


        return None, region_ids


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
