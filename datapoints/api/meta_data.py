import json
import base64
import time
import traceback

from tastypie.resources import ALL
from tastypie import fields
from tastypie.bundle import Bundle
from tastypie.resources import Resource
from django.contrib.auth.models import User, Group
from django.core.files.base import ContentFile
from django.core import serializers

from datapoints.api.base import BaseModelResource, BaseNonModelResource
from datapoints.models import *
from source_data.models import *
from source_data.etl_tasks.refresh_master import MasterRefresh
from source_data.etl_tasks.transform_upload import DocTransform
from datapoints.cache_tasks import CacheRefresh


class CampaignResource(BaseModelResource):

    class Meta(BaseModelResource.Meta):
        queryset = CampaignAbstracted.objects.all().values()
        resource_name = 'campaign'
        filtering = {
            "id": ALL,
        }


class RegionResource(BaseModelResource):

    def get_object_list(self,request):

        try:
            pr_id = request.GET['parent_region_id']
            qs = Region.objects.filter(parent_region_id=pr_id).values()
        except KeyError:
            qs =  Region.objects.all().values()

        return qs

    class Meta(BaseModelResource.Meta):
        queryset = Region.objects.all().values()
        resource_name = 'region'

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
    docfile = fields.FileField(attribute="csv", null=True, blank=True)

    class Meta:
        queryset = Document.objects.all().values()
        resource_name = 'source_doc'
        filtering = {
            "id": ALL,
        }

    def get_object_list(self,request):
        '''
        If post, create file and return the JSON of that object.
        If get, just query the source_doc table with request parameters
        '''
        try:
            doc_data = request.POST['docfile']
        except KeyError:
            return super(DocumentResource, self).get_object_list(request)

        try:
            doc_title = request.POST['doc_title'] + '-' + str(int(time.time()))
        except KeyError:
            doc_title = doc_data[:10]

        print doc_title

        new_doc = self.post_doc_data(doc_data, request.user.id, doc_title)

        return Document.objects.filter(id=new_doc.id).values()

    def post_doc_data(self, post_data, user_id, doc_title):

        file_meta, base64data = post_data.split(',')
        file_content = ContentFile(base64.b64decode(base64data))

        sd = Document.objects.create(
                doc_title = doc_title,
                created_by_id = user_id)

        sd.docfile.save(sd.guid, file_content)

        return sd


class Meta(BaseModelResource.Meta):
        queryset = Document.objects.all().values()
        list_allowed_methods = ['get', 'post']
        detail_allowed_methods = ['get', 'post']
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

class DocumentDetailResource(BaseModelResource):

    def get_object_list(self,request):

        try:
            document_id = request.POST['document_id']
        except KeyError:
            return super(DocumentDetailResource, self).get_object_list(request)

        post_data = request.POST

        doc_detail_dict = {
            'document_id': int(post_data['document_id']),
            'doc_detail_type_id': int(post_data['doc_detail_type_id']),
            'doc_detail_value': post_data['doc_detail_value'],
        }
        dd = DocumentDetail.objects.create(**doc_detail_dict)

        return DocumentDetail.objects.filter(id=dd.id).values()

    class Meta(BaseModelResource.Meta):
        queryset = DocumentDetail.objects.all().values()
        resource_name = 'doc_detail'
        filtering = {
            "id": ALL,
        }

class DocDataPointResource(BaseModelResource):

    def get_object_list(self,request):

        try:
            document_id = request.GET['document_id']
        except KeyError:
            document_id = None

        try:
            campaign_id = request.GET['campaign_id']
        except KeyError:
            campaign_id = None

        try:
            region_id = request.GET['region_id']
            all_region_ids = RegionTree.objects\
                .filter(parent_region_id = region_id).values_list('region_id',flat=True)
        except KeyError:
            all_region_ids = []

        return DocDataPoint.objects.filter(
            document_id = document_id,
            campaign_id = campaign_id,
            region_id__in=all_region_ids,
            ).values()

    class Meta(BaseModelResource.Meta):
        resource_name = 'doc_datapoint'

class ComputedDataPointResource(BaseModelResource):

    class Meta(BaseModelResource.Meta):
        queryset = DataPointComputed.objects.all().values()
        resource_name = 'computed_datapoint'

class SourceObjectMapResource(BaseModelResource):

    def get_object_list(self,request):

        som_ids = DocumentSourceObjectMap.objects\
            .filter(document_id=request.GET['document_id']).\
            values_list('source_object_map_id',flat=True)

        return SourceObjectMap.objects.filter(id__in=som_ids).values()

    class Meta(BaseModelResource.Meta):

        resource_name = 'source_object_map'

class SourceSubmissionResource(BaseModelResource):

    def get_object_list(self,request):

        try:
            qs = SourceSubmissionDetail.objects.filter(document_id=request\
                .GET['document_id']).values()
        except KeyError:
            qs = SourceSubmission.objects.filter(id=SourceSubmissionDetail\
                .objects.get(id=request\
                .GET['id']).source_submission_id)\
                .values_list('submission_json')

        return qs

    class Meta(BaseModelResource.Meta):
        resource_name = 'source_submission'


class DocTransFormResource(BaseModelResource):

    def get_object_list(self,request):

        doc_id = request.GET['document_id']
        dt = DocTransform(1,doc_id)
        dt.main()

        return Document.objects.filter(id = doc_id).values()

    class Meta(BaseModelResource.Meta):
        resource_name = 'transform_upload'

class RefreshMasterResource(BaseModelResource):

    def get_object_list(self,request):

        document_id = request.GET['document_id']

        mr = MasterRefresh(request.user.id, document_id)
        mr.submissions_to_doc_datapoints()
        mr.sync_datapoint()

        cr = CacheRefresh()
        cr.main()

        ## upsert document meta from the last run ##

        ## fixme -> abstract this <- ##

        doc_detail, created = DocumentDetail.objects.update_or_create(
            document_id = document_id,
            doc_detail_type_id = DocDetailType.objects.get(name = 'submission_processed_count').id,
            defaults= {'doc_detail_value': SourceSubmission.objects\
                .filter(process_status = 'PROCEESED').count()\
            },
        )

        doc_detail, created = DocumentDetail.objects.update_or_create(
            document_id = document_id,
            doc_detail_type_id = DocDetailType.objects.get(name = 'doc_datapoint_count').id,
            defaults= {'doc_detail_value': DocDataPoint.objects\
                .filter(document_id = document_id).count()\
            },
        )

        doc_detail, created = DocumentDetail.objects.update_or_create(
            document_id = document_id,
            doc_detail_type_id = DocDetailType.objects.get(name = 'datapoint_count').id,
            defaults= {'doc_detail_value': DataPoint.objects\
                .filter(source_submission_id__in=SourceSubmission.objects\
                .filter(document_id = document_id).values_list('id',flat=True)).count()\
            },
        )

        queryset = DocumentDetail.objects\
            .filter(document_id=document_id).values()

        return queryset

    class Meta(BaseModelResource.Meta):
        resource_name = 'refresh_master'

class DocDetailTypeResource(BaseModelResource):

    class Meta(BaseModelResource.Meta):
        queryset = DocDetailType.objects.all().values()
        resource_name = 'doc_detail_type'


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
