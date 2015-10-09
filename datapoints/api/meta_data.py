import json
import base64
import time
import traceback

from tastypie.resources import ALL
from tastypie import fields
from tastypie.bundle import Bundle
from tastypie.resources import Resource

from tastypie.authentication import Authentication
from tastypie.authentication import SessionAuthentication, ApiKeyAuthentication,\
    MultiAuthentication

from django.contrib.auth.models import User, Group
from django.core.files.base import ContentFile
from django.core import serializers
from django.utils.html import escape
from django.http import QueryDict

from datapoints.api.base import BaseModelResource, BaseNonModelResource
from datapoints.models import *
from source_data.models import *
from source_data.etl_tasks.refresh_master import MasterRefresh
from source_data.etl_tasks.transform_upload import DocTransform
from datapoints.cache_tasks import CacheRefresh
from django.utils.html import escape
from django.utils.datastructures import MultiValueDictKeyError

class CampaignResource(BaseModelResource):

    class Meta(BaseModelResource.Meta):
        queryset = CampaignAbstracted.objects.all().values()
        resource_name = 'campaign'
        filtering = {
            "id": ALL,
        }

class LocationResource(BaseModelResource):

    def get_object_list(self,request):

        try:
            pr_id = request.GET['parent_location_id']
            if pr_id == '-1':
                pr_id = None

            qs = Location.objects.filter(parent_location_id=pr_id).values()

        except KeyError:
            qs =  Location.objects.all().values()

        return qs

    class Meta(BaseModelResource.Meta):
        queryset = Location.objects.all().values()
        resource_name = 'location'

class IndicatorResource(BaseModelResource):

    class Meta(BaseModelResource.Meta):
        queryset = IndicatorAbstracted.objects.all().values()
        resource_name = 'indicator'
        filtering = {
            "id": ALL,
            "name": ALL,
        }

class OfficeResource(BaseModelResource):

    class Meta(BaseModelResource.Meta):
        queryset = Office.objects.all().values()
        resource_name = 'office'

class CampaignTypeResource(BaseModelResource):

    class Meta(BaseModelResource.Meta):
        queryset = CampaignType.objects.all().values()
        resource_name = 'campaign_type'

class LocationTypeResource(BaseModelResource):

    class Meta(BaseModelResource.Meta):
        queryset = LocationType.objects.all().values()
        resource_name = 'location_type'


class IndicatorTagResource(BaseModelResource):

    def get_object_list(self,request):

        try:
            tag_id = request.POST['id']

            if tag_id == '-1':
                tag_id = None

            tag_post_data = clean_post_data(dict(request.POST))
            del tag_post_data['id']

            tag_obj, created = IndicatorTag.objects.update_or_create(id=tag_id,
                defaults = tag_post_data)

            qs = IndicatorTag.objects.filter(id=tag_obj.id).values()

        except KeyError:
            return super(IndicatorTagResource, self).get_object_list(request)

        return qs


    class Meta(BaseModelResource.Meta):
        queryset = IndicatorTag.objects.all().values('id','parent_tag_id','tag_name','parent_tag__tag_name')
        resource_name = 'indicator_tag'
        filtering = {
            "id": ALL,
        }

class BaseIndicatorResource(BaseModelResource):

    def get_object_list(self,request):

        try:
            ind_id = request.POST['id']
            if ind_id == '-1':
                ind_id = None

            ind_post_data = clean_post_data(dict(request.POST))
            del ind_post_data['id']

            ind_obj, created = Indicator.objects.update_or_create(id=ind_id,
                defaults = ind_post_data)

            qs = Indicator.objects.filter(id=ind_obj.id).values('id','name','short_name')

        except KeyError:
            return super(BaseIndicatorResource, self).get_object_list(request)

        return qs

    class Meta(BaseModelResource.Meta):
        queryset = Indicator.objects.all().values('id','name','short_name')
        resource_name = 'basic_indicator'
        filtering = {
            "id": ALL,
        }

class IndicatorToTagResource(BaseModelResource):

    def get_object_list(self,request):

        try:
            indicator_id = request.POST['indicator_id']
            indicator_tag_id = request.POST['indicator_tag_id']

            it = IndicatorToTag.objects.create(
                indicator_id = indicator_id,
                indicator_tag_id = indicator_tag_id,
            )

            return IndicatorToTag.objects.filter(id=it.id).values()

        except KeyError:
            pass


        try:
            indicator_id = request.GET['indicator_id']
        except KeyError:
            indicator_id = -1

        qs = IndicatorToTag.objects\
            .filter(indicator_id=indicator_id)\
            .values('id','indicator_id','indicator__short_name',\
                'indicator_tag__tag_name')

        return qs


    class Meta(BaseModelResource.Meta):
        # queryset = IndicatorToTag.objects.all().values()
        resource_name = 'indicator_to_tag'

class CalculatedIndicatorComponentResource(BaseModelResource):

    class Meta(BaseModelResource.Meta):
        # queryset = CalculatedIndicatorComponent.objects.all().values()
        resource_name = 'indicator_calculation'

    def get_object_list(self,request):

        try:
            indicator_id = request.GET['indicator_id']
        except KeyError:
            indicator_id = -1

        qs = CalculatedIndicatorComponent.objects\
            .filter(indicator_id=indicator_id)\
            .values('id','indicator_id','indicator_component_id'
            ,'indicator_component__short_name','calculation')

        return qs


class CustomChartResource(BaseModelResource):

    class Meta(BaseModelResource.Meta):
        resource_name = 'custom_chart'
        filtering = {
            "id": ALL,
        }

    def obj_create(self, bundle, **kwargs):

        post_data = bundle.data

        try:
            chart_id = int(post_data['id'])
            dashboard_id = CustomChart.objects.get(id=chart_id).dashboard_id
        except KeyError:
            chart_id = None
            dashboard_id = post_data['dashboard_id']

        chart_json = json.loads(post_data['chart_json'])

        defaults = {
            'dashboard_id' : dashboard_id,
            'chart_json': chart_json,
        }

        chart, created = CustomChart.objects.update_or_create(
            id=chart_id,\
            defaults=defaults
        )

        bundle.obj = chart
        bundle.data['id'] = chart.id

        return bundle


    def obj_delete_list(self, bundle, **kwargs):
        """
        """

        obj_id = int(bundle.request.GET[u'id'])
        CustomChart.objects.filter(id=obj_id).delete()

    def get_object_list(self,request):

        chart_id_list = []

        try:
            dashboard_id = request.GET['dashboard_id']
            chart_id_list = CustomChart.objects.filter(dashboard_id =\
                dashboard_id).values_list('id',flat=True)
        except KeyError:
            pass

        try:
            chart_id_list = list(request.GET['id'])
        except KeyError:
            pass

        return CustomChart.objects.filter(id__in = chart_id_list)\
            .values()


class CustomDashboardResource(BaseModelResource):

    class Meta(BaseModelResource.Meta):
        resource_name = 'custom_dashboard'
        filtering = {
            "id": ALL,
        }
        always_return_data = True

    def obj_create(self, bundle, **kwargs):

        post_data = bundle.data
        user_id = bundle.request.user.id

        try:
            dash_id = int(post_data['id'])
        except KeyError:
            dash_id = None

        default_office_id = 1 # FIXME int(post_data['default_office_id'][0])

        defaults = {
            'id' : dash_id,
            'title' : post_data['title'],
            'owner_id': user_id,
            'default_office_id' : default_office_id,
        }

        dashboard, created = CustomDashboard.objects.update_or_create(
            id=dash_id,\
            defaults=defaults
        )

        bundle.obj = dashboard
        bundle.data['id'] = dashboard.id

        return bundle

    def get_object_list(self,request):
        '''
        '''

        try:
            dash_id_list = list(request.GET['id'])
        except KeyError:
            dash_id_list = CustomDashboard.objects.all().values_list('id',flat=True)

        return CustomDashboard.objects.filter(id__in=dash_id_list).values()

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

        try:
            new_doc = self.post_doc_data(doc_data, request.user.id, doc_title)
        except Exception as err:
            pass

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

class LocationPermissionResource(BaseModelResource):

    class Meta(BaseModelResource.Meta):
        queryset = LocationPermission.objects.all().values()
        resource_name = 'location_permission'

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
            location_id = request.GET['location_id']
            all_location_ids = LocationTree.objects\
                .filter(parent_location_id = location_id).values_list('location_id',flat=True)
        except KeyError:
            all_location_ids = []

        return DocDataPoint.objects.filter(
            document_id = document_id,
            campaign_id = campaign_id,
            location_id__in=all_location_ids,
            ).values()

    class Meta(BaseModelResource.Meta):
        resource_name = 'doc_datapoint'

class ComputedDataPointResource(BaseModelResource):

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
            location_id = request.GET['location_id']
        except KeyError:
            location_id = None

        som_ids = DocumentSourceObjectMap.objects.filter(
            document_id = document_id,
        ).values_list('source_object_map_id',flat=True)

        indicator_id_list = list(SourceObjectMap.objects.filter(
            id__in = som_ids,\
            content_type = 'indicator',
            master_object_id__gt = 0,
        ).values_list('master_object_id',flat=True))

        queryset = DataPointComputed.objects.filter(
            location_id = location_id,
            campaign_id = campaign_id,
            indicator_id__in = indicator_id_list
        ).values('indicator_id','indicator__short_name','value')

        return queryset


    class Meta(BaseModelResource.Meta):
        resource_name = 'computed_datapoint'

class SourceObjectMapResource(BaseModelResource):

    def get_object_list(self,request):

        try:
            request.POST['id']
            som_id = request.POST['id']
            som_obj = SourceObjectMap.objects.get(id=som_id)
            som_obj.master_object_id = request.POST['master_object_id']
            som_obj.mapped_by_id = request.POST['mapped_by_id']
            som_obj.save()

            return SourceObjectMap.objects.filter(id=som_id).values()
        except KeyError:
            pass

        try:
            som_ids = DocumentSourceObjectMap.objects\
                .filter(document_id=request.GET['document_id']).\
                values_list('source_object_map_id',flat=True)

            qs = SourceObjectMap.objects.filter(id__in=som_ids).values()
        except KeyError:
            qs = SourceObjectMap.objects.filter(id=request.GET['id']).values()
        except KeyError:
            qs = SourceObjectMap.objects.all().values()

        return qs

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
                .values()

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

class CacheRefreshResource(BaseModelResource):

    def get_object_list(self, request):

        cr = CacheRefresh()
        cr.main()

        queryset = DocumentDetail.objects\
            .filter(document_id=1).values()

        return queryset


    class Meta(BaseModelResource.Meta):
        resource_name = 'refresh_cache'


class RefreshMasterResource(BaseModelResource):

    def get_object_list(self,request):

        document_id = request.GET['document_id']

        mr = MasterRefresh(request.user.id, document_id)
        mr.submissions_to_doc_datapoints()
        mr.sync_datapoint()

        cr = CacheRefresh()
        cr.main()

        doc_detail, created = DocumentDetail.objects.update_or_create(
            document_id = document_id,
            doc_detail_type_id = DocDetailType.objects.get(name = 'submission_processed_count').id,
            defaults= {'doc_detail_value': SourceSubmission.objects\
                .filter(process_status = 'PROCESSED',\
                    document_id = document_id).count()\
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
    location_id = int()
    type = unicode()
    properties = dict()
    geometry = dict()


class GeoResource(BaseNonModelResource):
    '''
    A non model resource that allows us to query for shapefiles based on a
    colletion of parameters.
    '''

    location_id = fields.IntegerField(attribute = 'location_id')
    type = fields.CharField(attribute = 'type')
    properties = fields.DictField(attribute = 'properties')
    geometry = fields.DictField(attribute = 'geometry')

    class Meta(BaseNonModelResource.Meta):
        object_class = GeoJsonResult
        resource_name = 'geo'
        filtering = {
            "location_id": ALL,
        }

    def get_object_list(self,request):
        '''
        parse the url, query the polygons table and do some
        ugly data munging to convert the results from the DB into geojson
        '''

        self.err = None
        err, locations_to_return = self.get_locations_to_return_from_url(request)
        ## since this is not a model resource i will filter explicitly #

        if err:
            self.err = err
            return []

        polygon_values_list = LocationPolygon.objects.filter(location_id__in=\
            locations_to_return).values()

        features = []

        for p in polygon_values_list:

            geo_dict = json.loads(p['geo_json'])

            geo_obj = GeoJsonResult()
            geo_obj.location_id = p['location_id']
            geo_obj.geometry = geo_dict['geometry']
            geo_obj.type = geo_dict['type']
            geo_obj.properties = {'location_id': p['location_id']}

            features.append(geo_obj)

        return features

    def obj_get_list(self,bundle,**kwargs):
        '''
        Outer method for get_object_list... this calls get_object_list and
        could be a point at which additional build_agg_rc_dfing may be applied
        '''

        return self.get_object_list(bundle.request)

    def dehydrate(self, bundle):

        bundle.data.pop("resource_uri",None)# = bundle.obj.location.id
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


##
def clean_post_data(post_data_dict):

    cleaned = {}
    for k,v in post_data_dict.iteritems():

        to_clean = v[0]
        cleaned_v = to_clean.replace("[u'","").replace("]","")
        cleaned[k] = cleaned_v

    return cleaned
