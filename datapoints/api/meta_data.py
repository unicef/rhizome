from tastypie.resources import ALL
from tastypie import fields
from tastypie.bundle import Bundle
from tastypie.resources import Resource
from django.contrib.auth.models import User, Group

from datapoints.api.base import BaseModelResource, BaseNonModelResource
from datapoints.models import *
from source_data.models import *

import json


class CampaignResource(BaseModelResource):

    class Meta:
        queryset = CampaignAbstracted.objects.all().values()
        resource_name = 'campaign'

class RegionResource(BaseModelResource):

    class Meta:
        queryset = Region.objects.all().values()
        resource_name = 'region'

class IndicatorResource(BaseModelResource):

    class Meta:
        queryset = IndicatorAbstracted.objects.all().values()
        resource_name = 'indicator'

class OfficeResource(BaseModelResource):

    class Meta:
        queryset = Office.objects.all().values()
        resource_name = 'office'

class CampaignTypeResource(BaseModelResource):

    class Meta:
        queryset = CampaignType.objects.all().values()
        resource_name = 'campaign_type'

class RegionTypeResource(BaseModelResource):

    class Meta:
        queryset = CampaignType.objects.all().values()
        resource_name = 'region_type'

class IndicatorTagResource(BaseModelResource):

    class Meta:
        queryset = IndicatorTag.objects.all().values()
        resource_name = 'indicator_tag'

class IndicatorToTagResource(BaseModelResource):

    class Meta:
        queryset = IndicatorToTag.objects.all().values()
        resource_name = 'indicator_to_tag'

class DashboardResource(BaseModelResource):

    class Meta:
        queryset = CustomDashboard.objects.all().values()
        resource_name = 'custom_dashboard'

class DocumentResource(BaseModelResource):

    class Meta:
        queryset = Document.objects.all().values()
        resource_name = 'source_doc'

class GroupResource(BaseModelResource):

    class Meta:
        queryset = Group.objects.all().values()
        resource_name = 'group'

class UserGroupResource(BaseModelResource):

    class Meta:
        queryset = UserGroup.objects.all().values()
        resource_name = 'user_group'

class RegionPermissionResource(BaseModelResource):

    class Meta:
        queryset = RegionPermission.objects.all().values()
        resource_name = 'region_permission'

class GroupPermissionResource(BaseModelResource):

    class Meta:
        queryset = IndicatorPermission.objects.all().values()
        resource_name = 'group_permission'

class DocumentReviewResource(BaseModelResource):

    class Meta:
        queryset = IndicatorPermission.objects.all().values()
        resource_name = 'document_review'

class SourceObjectMapResource(BaseModelResource):

    class Meta:
        queryset = SourceObjectMap.objects.all().values()
        resource_name = 'source_object_map'



## Result Objects for geo Resources ##

class GeoJsonResult(object):
    region_id = int()
    type = unicode()
    properties = dict()
    geometry = dict()


class RegionPolygonResource(BaseNonModelResource):
    '''
    A non model resource that allows us to query for shapefiles based on a
    colletion of parameters.
    '''

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
        ## since this is not a model resource i will filter explicitly #

        if err:
            self.err = err
            return []

        polygon_values_list = RegionPolygon.objects.filter(region_id__in=\
            regions_to_return).values()

        features = []

        for p in polygon_values_list:

            geo_dict = json.loads(p['geo_json'])

            geo_obj = GeoJsonResult()
            geo_obj.region_id = p['region_id']
            geo_obj.geometry = geo_dict['geometry']
            geo_obj.type = geo_dict['type']
            geo_obj.properties = {'region_id': p['region_id']}

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
