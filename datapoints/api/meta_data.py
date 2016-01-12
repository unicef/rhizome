import json
import base64
import time

from tastypie.resources import ALL
from tastypie import fields
from tastypie.bundle import Bundle

from django.contrib.auth.models import User, Group
from django.core.files.base import ContentFile
from pandas import DataFrame
from pandas import notnull

from datapoints.api.base import BaseModelResource, BaseNonModelResource,\
    DataPointsException, get_locations_to_return_from_url
from datapoints.models import *
from source_data.models import *
from source_data.etl_tasks.refresh_master import MasterRefresh
from source_data.etl_tasks.transform_upload import DocTransform
from source_data.etl_tasks.sync_odk import OdkSync
from source_data.etl_tasks.sync_odk import OdkJarFileException
from datapoints.agg_tasks import AggRefresh
from datapoints.cache_meta import cache_all_meta
from tastypie.exceptions import ImmediateHttpResponse
from django.http import HttpResponse


class CampaignResource(BaseModelResource):
    class Meta(BaseModelResource.Meta):
        resource_name = 'campaign'

    def get_object_list(self, request):


        if self.top_lvl_location_id == 4721: ## hack to get sherine off my back !
            qs = Campaign.objects.all()
        else:
            qs = Campaign.objects.filter(\
                top_lvl_location_id = self.top_lvl_location_id)

        try:
            requested_ids = request.GET['id__in'].split(",")
            return qs.filter(id__in = requested_ids).values()
        except:
            return qs.values()


class LocationResource(BaseModelResource):
    class Meta(BaseModelResource.Meta):
        queryset = Location.objects.all().values()
        resource_name = 'location'

    def get_object_list(self, request):

        location_ids = get_locations_to_return_from_url(request)
        qs = Location.objects.filter(id__in=location_ids).values()

        return qs


class IndicatorResource(BaseModelResource):

    class Meta(BaseModelResource.Meta):
        resource_name = 'indicator'
        filtering = {
            "id": ALL,
        }

    def get_object_list(self, request):

        ind_ids = IndicatorToOffice.objects\
            .filter(office_id = Location.objects.get(id = self\
            .top_lvl_location_id).office_id )\
            .values_list('indicator_id',flat=True)

        return Indicator.objects.filter(id__in=ind_ids).values()

    def detail_uri_kwargs(self, bundle_or_obj):
        kwargs = {}

        if isinstance(bundle_or_obj, Bundle):
            kwargs['pk'] = bundle_or_obj.obj.id
        else:
            kwargs['pk'] = bundle_or_obj.id

        return kwargs

    def obj_create(self, bundle, **kwargs):

        post_data = bundle.data

        try:
            ind_id = int(post_data['id'])
            if ind_id == -1:
                ind_id = None
        except KeyError:
            ind_id = None

        try:
            defaults = {
                'name': post_data['name'],
                'short_name': post_data['short_name'],
                'description': post_data['description'],
                'data_format': post_data['data_format']
            }
        except Exception as error:
            data = {
                'error': 'Please provide ' + str(error) + ' for the indicator.',
                'code': -1
            }
            raise ImmediateHttpResponse(response=HttpResponse(json.dumps(data),
                                        status=500,
                                        content_type='application/json'))


        try:
            ind, created = Indicator.objects.update_or_create(
                id=ind_id,
                defaults=defaults
            )
        except Exception as error:
            data = {
                'error': error.message,
                'code': -1
            }
            raise ImmediateHttpResponse(response=HttpResponse(json.dumps(data),
                                        status=422,
                                        content_type='application/json'))

        bundle.obj = ind
        bundle.data['id'] = ind.id

        return bundle

class TypeResource(BaseModelResource):
    class Meta(BaseModelResource.Meta):
        queryset = CampaignType.objects.all().values()
        resource_name = 'campaign_type'


class LocationTypeResource(BaseModelResource):
    class Meta(BaseModelResource.Meta):
        queryset = LocationType.objects.all().values()
        resource_name = 'location_type'


class IndicatorTagResource(BaseModelResource):
    class Meta(BaseModelResource.Meta):
        queryset = IndicatorTag.objects.all().values('id', 'parent_tag_id', 'tag_name', 'parent_tag__tag_name')
        resource_name = 'indicator_tag'
        filtering = {
            "id": ALL,
        }

    def get_object_list(self, request):
        try:
            tag_id = request.GET['id']
            return IndicatorTag.objects.filter(id=tag_id).values()
        except KeyError:
            return super(IndicatorTagResource, self).get_object_list(request)

    def obj_create(self, bundle, **kwargs):
        post_data = bundle.data

        try:
            id = int(post_data['id'])
            if id == -1:
                id = None
        except KeyError:
            id = None

        tag_name = post_data['tag_name']

        defaults = {
            'tag_name': tag_name
        }

        try:
            parent_tag_id = int(post_data['parent_tag_id'])
            defaults = {
                'tag_name': tag_name,
                'parent_tag_id': parent_tag_id
            }
        except KeyError:
            pass

        tag, created = IndicatorTag.objects.update_or_create(
            id=id,
            defaults=defaults
        )

        bundle.obj = tag
        bundle.data['id'] = tag.id

        return bundle


class IndicatorToTagResource(BaseModelResource):
    class Meta(BaseModelResource.Meta):
        # queryset = IndicatorToTag.objects.all().values()
        resource_name = 'indicator_to_tag'

    def obj_create(self, bundle, **kwargs):

        indicator_id = bundle.data['indicator_id']
        indicator_tag_id = bundle.data['indicator_tag_id']

        it = IndicatorToTag.objects.create(
            indicator_id=indicator_id,
            indicator_tag_id=indicator_tag_id,
        )

        bundle.obj = it
        bundle.data['id'] = it.id

        return bundle

    def get_object_list(self, request):

        try:
            indicator_id = request.GET['indicator_id']
        except KeyError:
            indicator_id = -1

        qs = IndicatorToTag.objects \
            .filter(indicator_id=indicator_id) \
            .values('id', 'indicator_id', 'indicator__short_name', 'indicator_tag__tag_name')

        return qs

    def obj_delete_list(self, bundle, **kwargs):
        """
        """

        obj_id = int(bundle.request.GET[u'id'])
        IndicatorToTag.objects.filter(id=obj_id).delete()


class CalculatedIndicatorComponentResource(BaseModelResource):
    class Meta(BaseModelResource.Meta):
        # queryset = CalculatedIndicatorComponent.objects.all().values()
        resource_name = 'indicator_calculation'

    def get_object_list(self, request):

        try:
            indicator_id = request.GET['indicator_id']
        except KeyError:
            indicator_id = -1

        qs = CalculatedIndicatorComponent.objects \
            .filter(indicator_id=indicator_id) \
            .values('id', 'indicator_id', 'indicator_component_id', 'indicator_component__short_name', 'calculation')

        return qs

    def obj_create(self, bundle, **kwargs):
        indicator_id = bundle.data['indicator_id']
        component_id = bundle.data['component_id']
        type_info = bundle.data['typeInfo']

        it = CalculatedIndicatorComponent.objects.create(
            indicator_id=indicator_id,
            indicator_component_id=component_id,
            calculation=type_info,
        )

        bundle.obj = it
        bundle.data['id'] = it.id

        return bundle

    def obj_delete_list(self, bundle, **kwargs):
        """
        """

        obj_id = int(bundle.request.GET[u'id'])
        CalculatedIndicatorComponent.objects.filter(id=obj_id).delete()


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
            'dashboard_id': dashboard_id,
            'chart_json': chart_json,
        }

        chart, created = CustomChart.objects.update_or_create(
            id=chart_id,
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

    def get_object_list(self, request):

        chart_id_list = []

        try:
            dashboard_id = request.GET['dashboard_id']
            chart_id_list = CustomChart.objects\
                .filter(dashboard_id=dashboard_id).values_list('id', flat=True)
        except KeyError:
            pass

        try:
            chart_id_list = list(request.GET['id'])
        except KeyError:
            pass

        return CustomChart.objects.filter(id__in=chart_id_list) \
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

        default_office_id = 1  # FIXME int(post_data['default_office_id'][0])

        title = post_data['title']

        try:
            description = post_data['description']
        except KeyError:
            description = ''

        try:
            layout = int(post_data['layout'])
        except KeyError:
            layout = 0

        defaults = {
            'id': dash_id,
            'title': title,
            'description': description,
            'owner_id': user_id,
            'default_office_id': default_office_id,
            'layout': layout
        }

        if(CustomDashboard.objects.filter(title=title).count() > 0 and (dash_id is None)):
            raise DataPointsException('the custom dashboard "{0}" already exists'.format(title))

        dashboard, created = CustomDashboard.objects.update_or_create(id=dash_id, defaults=defaults)

        bundle.obj = dashboard
        bundle.data['id'] = dashboard.id
        return bundle

    def obj_delete_list(self, bundle, **kwargs):
        """
        """

        obj_id = int(bundle.request.GET[u'id'])
        CustomChart.objects.filter(dashboard_id=obj_id).delete()
        CustomDashboard.objects.filter(id=obj_id).delete()

    def get_object_list(self, request):
        '''
        '''

        try:
            dash_id = request.GET['id']
            return CustomDashboard.objects.filter(id=dash_id).values()
        except KeyError:
            return CustomDashboard.objects.all().values()


class DocumentResource(BaseModelResource):
    docfile = fields.FileField(attribute="csv", null=True, blank=True)

    class Meta(BaseModelResource.Meta):
        queryset = Document.objects.all().order_by('-created_at').values()
        max_limit = 10
        resource_name = 'source_doc'
        filtering = {
            "id": ALL,
        }

    def obj_create(self, bundle, **kwargs):
        '''
        If post, create file and return the JSON of that object.
        If get, just query the source_doc table with request parameters
        '''

        doc_data = bundle.data['docfile']

        try:
            doc_id = bundle.data['id']
        except KeyError:
            doc_id = None

        try:
            doc_title = bundle.data['doc_title'] + '-' + str(int(time.time()))
        except KeyError:
            doc_title = doc_data[:10]

        new_doc = self.post_doc_data(doc_data, bundle.request.user.id, doc_title, doc_id)

        bundle.obj = new_doc
        bundle.data['id'] = new_doc.id

        return bundle

    def post_doc_data(self, post_data, user_id, doc_title, doc_id):

        # when posting from ODK, i dont add the file_meta.. from the webapp
        # i do.  I should change so the post requests are consistent but
        # tryign to get this working for now.

        try:
            file_meta, base64data = post_data.split(',')
        except ValueError:
            base64data = post_data

        file_content = ContentFile(base64.b64decode(base64data))
        file_header = file_content.readline()

        sd, created = Document.objects.update_or_create(
            id=doc_id,
            defaults={'doc_title': doc_title, 'created_by_id': user_id, \
                'file_header': file_header}
        )

        sd.docfile.save(sd.guid, file_content)

        return sd


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

    def obj_create(self, bundle, **kwargs):

        new_obj = UserGroup.objects.create(**bundle.data)
        bundle.obj = new_obj
        bundle.data['id'] = new_obj.id

        return bundle

    def obj_delete_list(self, bundle, **kwargs):
        """
        """

        user_id = int(bundle.request.GET[u'user_id'])
        group_id = int(bundle.request.GET[u'group_id'])
        UserGroup.objects.filter(user_id=user_id, group_id=group_id)\
            .delete()

    def get_object_list(self, request):

        try:
            user_id = request.GET['user_id']
            return UserGroup.objects \
                .filter(user_id=user_id).values()
        except KeyError:
            return UserGroup.objects.all().values()


class LocationPermissionResource(BaseModelResource):
    class Meta(BaseModelResource.Meta):
        resource_name = 'location_responsibility'

    def get_object_list(self, request):

        return LocationPermission.objects\
            .filter(user_id=request.GET['user_id']).values()

    def obj_create(self, bundle, **kwargs):
        '''
        '''

        lp_obj, created = LocationPermission.objects.get_or_create(
            user_id = bundle.data['user_id'], defaults = {
                'top_lvl_location_id' : bundle.data['location_id']
            })

        if not created:
            lp_obj.top_lvl_location_id = bundle.data['location_id']
            lp_obj.save()

        bundle.obj = lp_obj
        bundle.data['id'] = lp_obj.id

        return bundle

class DocumentDetailResource(BaseModelResource):
    class Meta(BaseModelResource.Meta):
        resource_name = 'doc_detail'
        filtering = {
            "id": ALL,
            "document": ALL,
        }

    def obj_create(self, bundle, **kwargs):

        post_data = bundle.data

        defaults = {
            'doc_detail_value': post_data['doc_detail_value'],
        }

        chart, created = DocumentDetail.objects.update_or_create(
            document_id=post_data['document_id'],
            doc_detail_type_id=post_data['doc_detail_type_id'],
            defaults=defaults
        )

        bundle.obj = chart
        bundle.data['id'] = chart.id

        return bundle

    def get_object_list(self, request):

        try:
            doc_detail_type = request.GET['doc_detail_type']
            return  DocumentDetail.objects\
                .filter(doc_detail_type__name=doc_detail_type)\
                .values('id','doc_detail_type_id','doc_detail_type__name',\
                    'document_id', 'doc_detail_value')
        except KeyError:
            pass

        try:
            doc_id = request.GET['document_id']
            return  DocumentDetail.objects\
                .filter(document_id=doc_id)\
                .values('id','doc_detail_type_id','doc_detail_type__name',\
                    'document_id', 'doc_detail_value')
        except KeyError:
            return DocumentDetail.objects.all()\
                .values('id','doc_detail_type_id','doc_detail_type__name',\
                'document_id', 'doc_detail_value')


class DocDataPointResource(BaseModelResource):
    class Meta(BaseModelResource.Meta):
        resource_name = 'doc_datapoint'

    def get_object_list(self, request):

        queryset = DocDataPoint.objects.filter(
            document_id=request.GET['document_id'],
            # campaign_id=campaign_id,
            # location_id__in=all_location_ids,
        )[:50].values('location__name', 'indicator__short_name', 'campaign__name', 'value')

        return queryset


class ComputedDataPointResource(BaseModelResource):
    class Meta(BaseModelResource.Meta):
        resource_name = 'computed_datapoint'

    def get_object_list(self, request):

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
            document_id=document_id,
        ).values_list('source_object_map_id', flat=True)

        indicator_id_list = list(SourceObjectMap.objects.filter(
            id__in=som_ids,
            content_type='indicator',
            master_object_id__gt=0,
        ).values_list('master_object_id', flat=True))

        queryset = DataPointComputed.objects.filter(
            location_id=location_id,
            campaign_id=campaign_id,
            indicator_id__in=indicator_id_list
        ).values('indicator_id', 'indicator__short_name', 'value')

        return queryset


class SourceObjectMapResource(BaseModelResource):
    class Meta(BaseModelResource.Meta):
        resource_name = 'source_object_map'

    def obj_create(self, bundle, **kwargs):

        post_data = bundle.data

        som_id = int(post_data['id'])

        som_obj = SourceObjectMap.objects.get(id=som_id)
        master_object_id = post_data['master_object_id']
        som_obj.master_object_id = master_object_id
        som_obj.master_object_name = self.get_master_object_name(som_obj)
        som_obj.mapped_by_id = post_data['mapped_by_id']
        som_obj.save()

        bundle.obj = som_obj
        bundle.data['id'] = som_obj.id
        bundle.data['master_object_name'] = som_obj.master_object_name

        return bundle

    def get_master_object_name(self, som_obj):

        # som_obj = SourceObjectMap.objects.get(id=3078)
        qs_map = {
            'indicator': ['short_name',Indicator.objects.get],
            'location': ['name',Location.objects.get],
        }

        obj_display_field = qs_map[som_obj.content_type][0]
        qs = qs_map[som_obj.content_type][1]

        master_obj = qs(id=som_obj.master_object_id).__dict__
        master_object_name = master_obj[obj_display_field]

        return master_object_name

    def get_object_list(self, request):

        try:
            som_ids = DocumentSourceObjectMap.objects \
                .filter(document_id=request.GET['document_id']). \
                values_list('source_object_map_id', flat=True)

            qs = SourceObjectMap.objects.filter(id__in=som_ids).values()
        except KeyError:
            qs = SourceObjectMap.objects.filter(id=request.GET['id']).values()
        except KeyError:
            qs = SourceObjectMap.objects.all().values()

        return qs


class SourceSubmissionResource(BaseModelResource):
    class Meta(BaseModelResource.Meta):
        resource_name = 'source_submission'

    def get_object_list(self, request):

        try:
            # see: https://trello.com/c/IGNzN87U/296-3-collapse-source-submission-adn-submission-detail
            qs = SourceSubmission.objects.filter(document_id=request.GET['document_id'])[:50].values()
        except KeyError:
            qs = SourceSubmission.objects.filter(id=request.GET['id']).values()

        return qs


class DocTransFormResource(BaseModelResource):
    class Meta(BaseModelResource.Meta):
        resource_name = 'transform_upload'

    def get_object_list(self, request):
        doc_id = request.GET['document_id']
        dt = DocTransform(request.user.id, doc_id)
        dt.main()

        return Document.objects.filter(id=doc_id).values()


class AggRefreshResource(BaseModelResource):
    class Meta(BaseModelResource.Meta):
        resource_name = 'refresh_cache'

    def get_object_list(self, request):
       '''
       If no campaign is provided, find one datapoitn that needs processing,
       then find the related campaign based on the

       To Do -- Make a method on the Datapoint model called..
       get_campaign_for_datapoint so that this logic can be easily extended.

       This needs cleanup.
       '''

       try:
           campaign_id = request.GET['campaign_id']
           AggRefresh(campaign_id)
           return Campaign.objects.filter(id=campaign_id).values()
       except KeyError:
           campsign_id = None

       try:
           one_dp_that_needs_agg = DataPoint.objects\
               .filter(cache_job_id = -1)[0]
       except IndexError:
           return Office.objects.all().values()

       location_id = one_dp_that_needs_agg.location_id
       data_date = one_dp_that_needs_agg.data_date

       date_no_datetime = data_date.date()
       campaigns_in_date_range = Campaign.objects.filter(
           start_date__lte = date_no_datetime, end_date__gt = data_date)

       parent_location_list = LocationTree.objects\
           .filter(location_id = location_id)\
           .values_list('parent_location_id',flat=True)

       for c in campaigns_in_date_range:
           if c.top_lvl_location_id in parent_location_list:
               campaign_id = c.id
               AggRefresh(c.id)

               return Campaign.objects.filter(id=campaign_id).values()

       ## if code reaches here that means there is noting to process ##
       return Office.objects.all().values()




class RefreshMasterResource(BaseModelResource):
    class Meta(BaseModelResource.Meta):
        resource_name = 'refresh_master'

    def get_object_list(self, request):
        document_id = request.GET['document_id']

        mr = MasterRefresh(request.user.id, document_id)
        mr.main()

        doc_detail, created = DocumentDetail.objects.update_or_create(
            document_id=document_id,
            doc_detail_type_id=DocDetailType.objects.get(name='submission_processed_count').id,
            defaults={
                'doc_detail_value': SourceSubmission.objects.filter(
                    process_status='PROCESSED',
                    document_id=document_id).count()
            },
        )

        doc_detail, created = DocumentDetail.objects.update_or_create(
            document_id=document_id,
            doc_detail_type_id=DocDetailType.objects.get(name='doc_datapoint_count').id,
            defaults={
                'doc_detail_value': DocDataPoint.objects.filter(document_id=document_id).count()
            },
        )

        doc_detail, created = DocumentDetail.objects.update_or_create(
            document_id=document_id,
            doc_detail_type_id=DocDetailType.objects.get(name='datapoint_count').id,
            defaults={
                'doc_detail_value': DataPoint.objects.filter(
                    source_submission_id__in=SourceSubmission.objects.filter(
                        document_id=document_id).values_list('id', flat=True)).count()
            },
        )

        queryset = DocumentDetail.objects \
            .filter(document_id=document_id).values('id','doc_detail_type_id'\
                ,'doc_detail_type__name','document_id', 'doc_detail_value')

        return queryset


class CacheMetaResource(BaseModelResource):
    def get_object_list(self, request):
        cache_all_meta()

        return Office.objects.all().values()

    class Meta(BaseModelResource.Meta):
        resource_name = 'cache_meta'


class SyncOdkResource(BaseModelResource):
    def get_object_list(self, request):

        required_param = 'odk_form_id'
        odk_form_id = None

        try:
            odk_form_id = request.GET[required_param]
        except KeyError:
            pass

        try:
            document_id = request.GET['document_id']
            odk_form_id = DocumentDetail.objects.get(
                document_id = document_id, doc_detail_type__name = 'odk_form_name'
            ).doc_detail_value
        except KeyError:
            pass

        if not odk_form_id:
            raise DataPointsException('"{0}" is a required parameter for this request'.format(required_param))

        try:
            odk_sync_object = OdkSync(odk_form_id, **{'user_id':request.user.id})
            document_id_list, sync_result_data = odk_sync_object.main()

        except OdkJarFileException as e:
            raise DataPointsException(e.errorMessage)

        return Document.objects.filter(id__in=document_id_list).values()

    class Meta(BaseModelResource.Meta):
        resource_name = 'sync_odk'


class QueueProcessResource(BaseModelResource):
    class Meta(BaseModelResource.Meta):
        resource_name = 'queue_process'

    def get_object_list(self, request):
        document_id = request.GET['document_id']

        SourceSubmission.objects.filter(document_id=document_id).update(process_status='TO_PROCESS')

        queryset = DocumentDetail.objects \
            .filter(document_id=document_id).values('id','doc_detail_type_id'\
                ,'doc_detail_type__name','document_id', 'doc_detail_value')

        return queryset


class DocDetailTypeResource(BaseModelResource):
    class Meta(BaseModelResource.Meta):
        queryset = DocDetailType.objects.all().values()
        resource_name = 'doc_detail_type'

class ChartTypeResult(object):
    id = int()
    name = unicode()

class ChartTypeTypeResource(BaseNonModelResource):
    id = fields.IntegerField(attribute='id')
    name = fields.CharField(attribute='name')

    class Meta(BaseNonModelResource.Meta):
        object_class = ChartTypeResult
        resource_name = 'chart_type'

    def obj_get_list(self, bundle, **kwargs):
        '''
        Outer method for get_object_list... this calls get_object_list and
        could be a point at which additional build_agg_rc_dfing may be applied
        '''

        return self.get_object_list(bundle.request)

    def get_object_list(self, request):

        chart_types =["PieChart","LineChart","BarChart","ColumnChart",\
            "ChoroplethMap","ScatterChart","TableChart"]
        qs = []

        for i,(ct) in enumerate(chart_types):

            ct_obj = ChartTypeResult()
            ct_obj.id = i
            ct_obj.name = ct
            qs.append(ct_obj)

        return qs

class OfficeResource(BaseModelResource):
    class Meta(BaseModelResource.Meta):
        queryset = Office.objects.all().values()
        resource_name = 'office'


def clean_post_data(post_data_dict):
    cleaned = {}
    for k, v in post_data_dict.iteritems():
        to_clean = v[0]
        cleaned_v = to_clean.replace("[u'", "").replace("]", "")
        cleaned[k] = cleaned_v

    return cleaned
