import json

from django.contrib.auth.models import User, Group
from django.utils.datastructures import MultiValueDictKeyError

from tastypie.resources import ALL
from tastypie import fields
from tastypie.bundle import Bundle
from tastypie.resources import Resource
from tastypie.http import HttpBadRequest
from tastypie.exceptions import ImmediateHttpResponse

from datapoints.api.base import BaseModelResource, BaseNonModelResource
from datapoints.models import *
from source_data.models import *


class CampaignResource(BaseModelResource):

    class Meta(BaseModelResource.Meta):
        queryset = CampaignAbstracted.objects.all().values()
        resource_name = 'campaign'

class RegionResource(BaseModelResource):

    class Meta(BaseModelResource.Meta):
        resource_name = 'region'

    def get_list(self, request, **kwargs):
        """
        """

        region_tree = [rt for rt in RegionTree.objects\
            .filter(region_id=request.GET['parent_region_id'])\
            .values('parent_region_id','lvl','name')]

        base_bundle = self.build_bundle(request=request)
        objects = self.obj_get_list(bundle=base_bundle, **self.remove_api_resource_names(kwargs))
        bundles = [obj for obj in objects]#[self._meta.collection_name]]
        response_meta = {
            'limit':None, ## paginator.get_limit(),
            'offset': None, ## paginator.get_offset(),
            'total_count':len(objects),
            'region_tree': region_tree
        }

        response_data = {
            'objects': bundles,
            'meta': response_meta,
            'error': None
        }
        return self.create_response(request, response_data)

    def get_object_list(self,request):

        try:
            parent_region_id = request.GET['parent_region_id']
            region_id_list = list(Region.objects.filter(parent_region_id = \
                parent_region_id).values_list('id',flat=True))
            region_id_list.append(parent_region_id)
        except MultiValueDictKeyError:

            print '===='
            raise ImmediateHttpResponse(
                HttpBadRequest("v1 Region Resource requires a \
                    'parent_region_id'parameter"))

        return Region.objects.filter(id__in=region_id_list).values()

class IndicatorResource(BaseModelResource):

    class Meta(BaseModelResource.Meta):
        queryset = IndicatorAbstracted.objects.all().values()
        resource_name = 'indicator'

class OfficeResource(BaseModelResource):

    class Meta(BaseModelResource.Meta):
        queryset = Office.objects.all().values()
        resource_name = 'office'

class CampaignTypeResource(BaseModelResource):

    class Meta(BaseModelResource.Meta):
        queryset = CampaignType.objects.all().values()
        resource_name = 'campaign_type'

class RegionTypeResource(BaseModelResource):

    class Meta(BaseModelResource.Meta):
        queryset = CampaignType.objects.all().values()
        resource_name = 'region_type'

class IndicatorTagResource(BaseModelResource):

    class Meta(BaseModelResource.Meta):
        queryset = IndicatorTag.objects.all().values()
        resource_name = 'indicator_tag'

class IndicatorToTagResource(BaseModelResource):

    class Meta(BaseModelResource.Meta):
        queryset = IndicatorToTag.objects.all().values()
        resource_name = 'indicator_to_tag'

class DashboardResource(BaseModelResource):

    class Meta(BaseModelResource.Meta):
        queryset = CustomDashboard.objects.all().values()
        resource_name = 'custom_dashboard'

class DocumentResource(BaseModelResource):

    class Meta(BaseModelResource.Meta):
        queryset = Document.objects.all().values()
        resource_name = 'source_doc'

class UserResource(BaseModelResource):

    class Meta(BaseModelResource.Meta):
        queryset = User.objects.all().values()
        resource_name = 'user'

class GroupResource(BaseModelResource):

    class Meta(BaseModelResource.Meta):
        queryset = Group.objects.all().values()
        resource_name = 'group'

class UserGroupResource(BaseModelResource):

    class Meta(BaseModelResource.Meta):
        queryset = UserGroup.objects.all().values()
        resource_name = 'user_group'

class RegionPermissionResource(BaseModelResource):

    class Meta(BaseModelResource.Meta):
        queryset = RegionPermission.objects.all().values()
        resource_name = 'region_permission'

class GroupPermissionResource(BaseModelResource):

    class Meta(BaseModelResource.Meta):
        queryset = IndicatorPermission.objects.all().values()
        resource_name = 'group_permission'

class DocumentReviewResource(BaseModelResource):

    class Meta(BaseModelResource.Meta):
        queryset = IndicatorPermission.objects.all().values()
        resource_name = 'document_review'

class SourceSubmissionResource(BaseModelResource):

    class Meta(BaseModelResource.Meta):
        queryset = SourceSubmission.objects.all().values()
        resource_name = 'source_submission'

class DocumentDetailResource(BaseModelResource):

    class Meta(BaseModelResource.Meta):
        queryset = DocumentDetail.objects.all().values()
        resource_name = 'document_detail'

class DocDataPointResource(BaseModelResource):

    class Meta(BaseModelResource.Meta):
        queryset = DocDataPoint.objects.all().values()
        resource_name = 'doc_datapoint'

class ComputedDataPointResource(BaseModelResource):

    class Meta(BaseModelResource.Meta):
        queryset = DataPointComputed.objects.all().values()
        resource_name = 'computed_datapoint'

class SourceObjectMapResource(BaseModelResource):

    def get_object_list(self,request):

        som_ids = DocumentSourceObjectMap.objects.filter(document_id=request.GET['document_id'])
        queryset = SourceObjectMap.objects.filter(id__in=som_ids).values()

        return queryset

    class Meta(BaseModelResource.Meta):

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
