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

from datapoints.api.base import BaseModelResource, BaseNonModelResource, DataPointsException
from datapoints.models import Campaign, Location, Indicator, IndicatorTag, CampaignType, \
    LocationType, IndicatorToTag, CustomChart, CustomDashboard, CalculatedIndicatorComponent, UserGroup, \
    LocationResponsibility, IndicatorPermission, DocDataPoint, DataPointComputed, ChartType, DataPoint, \
    ChartTypeToIndicator, Office, IndicatorBound, IndicatorToTag, IndicatorToOffice
from source_data.models import Document, DocumentDetail, DocumentSourceObjectMap, SourceObjectMap, DocDetailType, \
    SourceSubmission
from source_data.etl_tasks.refresh_master import MasterRefresh
from source_data.etl_tasks.transform_upload import DocTransform
from datapoints.agg_tasks import AggRefresh
from datapoints.cache_meta import cache_all_meta
from tastypie.exceptions import ImmediateHttpResponse
from django.http import HttpResponse


class CampaignResource(BaseModelResource):
    class Meta(BaseModelResource.Meta):
        queryset = Campaign.objects.all().values()
        resource_name = 'campaign'
        filtering = {
            "id": ALL,
        }


class LocationResource(BaseModelResource):
    def get_object_list(self, request):

        try:
            pr_id = request.GET['parent_location_id']
            if pr_id == '-1':
                pr_id = None

            qs = Location.objects.filter(parent_location_id=pr_id).values()

        except KeyError:
            qs = Location.objects.all().values()

        return qs

    class Meta(BaseModelResource.Meta):
        queryset = Location.objects.all().values()
        resource_name = 'location'

class IndicatorResult(object):
    id = int()
    description = unicode()
    short_name = unicode()
    slug = unicode()
    name = unicode()
    data_format = unicode()
    bound_json = list()
    tag_json = list()
    office_id = list()


class IndicatorResource(BaseNonModelResource):
    id = fields.IntegerField(attribute='id',null=True)
    name = fields.CharField(attribute='name')
    short_name = fields.CharField(attribute='short_name')
    slug = fields.CharField(attribute='slug',null=True)
    description = fields.CharField(attribute='description')
    data_format = fields.CharField(attribute='data_format',null=True)
    bound_json = fields.ListField(attribute='bound_json',null=True)
    tag_json = fields.ListField(attribute='tag_json',null=True)
    office_id = fields.ListField(attribute='office_id',null=True)

    class Meta(BaseNonModelResource.Meta):
        object_class = IndicatorResult
        resource_name = 'indicator'

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

        defaults = {
            'name': post_data['name'],
            'short_name': post_data['short_name'],
            'description': post_data['description'],
            'data_format': post_data['data_format']
        }

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


    def obj_get_list(self, bundle, **kwargs):
        '''
        Outer method for get_object_list... this calls get_object_list and
        could be a point at which additional build_agg_rc_dfing may be applied
        '''

        return self.get_object_list(bundle.request)

    def get_indicator_ids_from_request(self, request):
        '''
        '''

        try:
            indicator_id_list = [request.GET['id']]
            return indicator_id_list
        except KeyError:
            pass

        try:
            x = request.GET['id__in'].split(',')
            return x
        except KeyError:
            pass

        try:
            office_id = request.GET['office_id']
            return self.get_indicator_id_by_office(office_id)
        except KeyError:
            pass

        return None

    def build_indicator_queryset(self, indicator_id_list):
        '''
        Based on the indicator_ids, we make 3 requests, one for the indicators
        one for the bounds, and another for the tags.
        '''

        tag_cols = ['indicator_id','indicator_tag_id']
        bound_cols = ['indicator_id','bound_name','mn_val','mx_val']
        ind_to_office_cols = ['indicator_id','office_id']

        if indicator_id_list:
            ## get tags ##
            tag_df = DataFrame(list(IndicatorToTag.objects.filter(indicator_id__in=\
                indicator_id_list).values_list(*tag_cols)),columns = tag_cols)

            bound_df = DataFrame(list(IndicatorBound.objects\
                .filter(indicator_id__in=indicator_id_list)\
                .values_list(*bound_cols)),columns = bound_cols)

            office_df = DataFrame(list(IndicatorToOffice.objects\
                .filter(indicator_id__in=indicator_id_list)\
                .values_list(*ind_to_office_cols)),columns = ind_to_office_cols)

            qs = Indicator.objects.filter(id__in=indicator_id_list)

        else:
            tag_df = DataFrame(list(IndicatorToTag.objects.all()\
                .values_list(*tag_cols)),columns = tag_cols)

            bound_df = DataFrame(list(IndicatorBound.objects.all()\
                .values_list(*bound_cols)),columns = bound_cols)

            office_df = DataFrame(list(IndicatorToOffice.objects\
                .all().values_list(*ind_to_office_cols))\
                ,columns = ind_to_office_cols)

            qs = Indicator.objects.all()

        bound_df = bound_df.where((notnull(bound_df)), None)
        tag_df = tag_df.where((notnull(tag_df)), None)
        # office_df = office_df.where((notnull(office_df)), None)

        return qs, bound_df, tag_df, office_df

    def get_object_list(self, request):
        indicator_batch = []

        indicator_id_list = self.get_indicator_ids_from_request(request)
        qs, bound_df, tag_df, office_df = \
            self.build_indicator_queryset(indicator_id_list)

        for row in qs:

            ## create the ResultObject and assign the basic variables ##
            ir = IndicatorResult()
            ir.id, ir.name, ir.description, ir.short_name, ir.slug, ir.data_format \
                = row.id, row.name, row.description, row.short_name,row.slug, row.data_format \

            ## look up the bounds / tags from the data two DFs created above ##
            filtered_tag_df = tag_df[tag_df['indicator_id'] == \
                row.id]
            filtered_bound_df = bound_df[bound_df['indicator_id'] == \
                row.id]
            filtered_office_df = office_df[office_df['indicator_id'] == \
                row.id]

            ir.bound_json= [row.to_dict() for ix, row in\
                filtered_bound_df.iterrows()]
            ir.tag_json = list(filtered_tag_df['indicator_tag_id'].unique())
            ir.office_id = list(filtered_office_df['office_id'].unique())

            indicator_batch.append(ir)

        return indicator_batch

    def get_indicator_id_by_office(self, office_id):

        indicator_ids = IndicatorToOffice.objects.filter(office_id=office_id)\
            .values_list('indicator_id',flat=True)

        return indicator_ids


class CampaignTypeResource(BaseModelResource):
    class Meta(BaseModelResource.Meta):
        queryset = CampaignType.objects.all().values()
        resource_name = 'campaign_type'


class LocationTypeResource(BaseModelResource):
    class Meta(BaseModelResource.Meta):
        queryset = LocationType.objects.all().values()
        resource_name = 'location_type'


class IndicatorTagResource(BaseModelResource):
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

    class Meta(BaseModelResource.Meta):
        queryset = IndicatorTag.objects.all().values('id', 'parent_tag_id', 'tag_name', 'parent_tag__tag_name')
        resource_name = 'indicator_tag'
        filtering = {
            "id": ALL,
        }


class IndicatorToTagResource(BaseModelResource):
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

    class Meta(BaseModelResource.Meta):
        # queryset = IndicatorToTag.objects.all().values()
        resource_name = 'indicator_to_tag'


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
        queryset = Document.objects.all().values()
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
        sd, created = Document.objects.update_or_create(
            id=doc_id,
            defaults={'doc_title': doc_title, 'created_by_id': user_id}
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


class LocationResponsibilityResource(BaseModelResource):
    class Meta(BaseModelResource.Meta):
        # queryset = LocationResponsibility.objects.all().values()
        resource_name = 'location_responsibility'

    def get_object_list(self, request):

        try:
            user_id = request.GET['user_id']
            return LocationResponsibility.objects \
                .filter(user_id=user_id).values()
        except KeyError:
            return LocationResponsibility.objects.all().values()


    def obj_create(self, bundle, **kwargs):
        '''
        If post, create file and return the JSON of that object.
        If get, just query the source_doc table with request parameters
        '''

        new_obj = LocationResponsibility.objects.create(**bundle.data)
        bundle.obj = new_obj
        bundle.data['id'] = new_obj.id
        return bundle

    def obj_delete_list(self, bundle, **kwargs):
        """
        """

        obj_id = int(bundle.request.GET[u'id'])

        print 'DELETEING \n' * 10
        print obj_id
        print 'DELETEING \n' * 10

        LocationResponsibility.objects.get(id=obj_id).delete()

class GroupPermissionResource(BaseModelResource):
    class Meta(BaseModelResource.Meta):
        queryset = IndicatorPermission.objects.all().values()
        resource_name = 'group_permission'


class DocumentReviewResource(BaseModelResource):
    class Meta(BaseModelResource.Meta):
        queryset = IndicatorPermission.objects.all().values()
        resource_name = 'document_review'


class DocumentDetailResource(BaseModelResource):
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
            return DocumentDetail.objects \
                .filter(doc_detail_type__name=doc_detail_type).values()
        except KeyError:
            return DocumentDetail.objects.all().values()

    class Meta(BaseModelResource.Meta):
        resource_name = 'doc_detail'
        filtering = {
            "id": ALL,
            "document": ALL,
        }


class DocDataPointResource(BaseModelResource):
    def get_object_list(self, request):

        queryset = DocDataPoint.objects.filter(
            document_id=request.GET['document_id'],
            # campaign_id=campaign_id,
            # location_id__in=all_location_ids,
        )[:50].values('location__name', 'indicator__short_name', 'campaign__slug', 'value')

        return queryset

    class Meta(BaseModelResource.Meta):
        resource_name = 'doc_datapoint'


class ComputedDataPointResource(BaseModelResource):
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

    class Meta(BaseModelResource.Meta):
        resource_name = 'computed_datapoint'


class SourceObjectMapResource(BaseModelResource):
    def obj_create(self, bundle, **kwargs):

        post_data = bundle.data

        som_id = int(post_data['id'])

        som_obj = SourceObjectMap.objects.get(id=som_id)
        som_obj.master_object_id = post_data['master_object_id']
        som_obj.mapped_by_id = post_data['mapped_by_id']
        som_obj.save()

        bundle.obj = som_obj
        bundle.data['id'] = som_obj.id

        return bundle

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

    class Meta(BaseModelResource.Meta):
        resource_name = 'source_object_map'


class SourceSubmissionResource(BaseModelResource):
    def get_object_list(self, request):

        try:
            # see: https://trello.com/c/IGNzN87U/296-3-collapse-source-submission-adn-submission-detail
            qs = SourceSubmission.objects.filter(document_id=request.GET['document_id'])[:50].values()
        except KeyError:
            qs = SourceSubmission.objects.filter(id=request.GET['id']).values()

        return qs

    class Meta(BaseModelResource.Meta):
        resource_name = 'source_submission'


class DocTransFormResource(BaseModelResource):
    def get_object_list(self, request):
        doc_id = request.GET['document_id']
        dt = DocTransform(request.user.id, doc_id)
        dt.main()

        return Document.objects.filter(id=doc_id).values()

    class Meta(BaseModelResource.Meta):
        resource_name = 'transform_upload'


class AggRefreshResource(BaseModelResource):
    def get_object_list(self, request):
        AggRefresh()

        queryset = DocumentDetail.objects \
            .filter(document_id=1).values()

        return queryset

    class Meta(BaseModelResource.Meta):
        resource_name = 'refresh_cache'


class RefreshMasterResource(BaseModelResource):
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
            .filter(document_id=document_id).values()

        return queryset

    class Meta(BaseModelResource.Meta):
        resource_name = 'refresh_master'


class CacheMetaResource(BaseModelResource):
    def get_object_list(self, request):
        cache_all_meta()

        return Office.objects.all().values()

    class Meta(BaseModelResource.Meta):
        resource_name = 'cache_meta'

class QueueProcessResource(BaseModelResource):
    def get_object_list(self, request):
        document_id = request.GET['document_id']

        SourceSubmission.objects.filter(document_id=document_id).update(process_status='TO_PROCESS')

        queryset = DocumentDetail.objects \
            .filter(document_id=document_id).values()

        return queryset

    class Meta(BaseModelResource.Meta):
        resource_name = 'queue_process'


class DocDetailTypeResource(BaseModelResource):
    class Meta(BaseModelResource.Meta):
        queryset = DocDetailType.objects.all().values()
        resource_name = 'doc_detail_type'


class ChartTypeTypeResource(BaseModelResource):
    class Meta(BaseModelResource.Meta):
        queryset = ChartType.objects.all().values()
        resource_name = 'chart_type'

    def get_object_list(self, request):

        try:
            primary_indicator_id = request.GET['primary_indicator_id']
            chart_type_ids = ChartTypeToIndicator.objects.filter(
                indicator_id=primary_indicator_id)\
                .values_list('chart_type_id')

            return ChartType.objects.filter(id__in=chart_type_ids).values()
        except KeyError:
            return super(ChartTypeTypeResource, self).get_object_list(request)


class OfficeResult(object):
    id = int()
    name = unicode()
    latest_campaign_id = int()


class OfficeResource(BaseNonModelResource):
    id = fields.IntegerField(attribute='id')
    name = fields.CharField(attribute='name')
    latest_campaign_id = fields.IntegerField(attribute='latest_campaign_id')
    top_level_location_id = fields.IntegerField(attribute='top_level_location_id')

    class Meta(BaseNonModelResource.Meta):
        object_class = OfficeResult
        resource_name = 'office'
        filtering = {
            "id": ALL,
        }

    def obj_get_list(self, bundle, **kwargs):
        '''
        Outer method for get_object_list... this calls get_object_list and
        could be a point at which additional build_agg_rc_dfing may be applied
        '''

        return self.get_object_list(bundle.request)

    def get_object_list(self, request):

        # temporary -- this should be based on start_date / data completeness
        latest_campaign_lookup = {1: 43, 2: 41, 3: 45}
        location_lookup = {1: 1, 2: 2, 3: 3}

        qs = []
        for row in Office.objects.all():

            office_obj = OfficeResult()
            office_obj.id = row.id
            office_obj.name = row.name
            office_obj.latest_campaign_id = latest_campaign_lookup[row.id]
            office_obj.top_level_location_id = location_lookup[row.id]

            qs.append(office_obj)

        return qs

    def dehydrate(self, bundle):

        bundle.data.pop("resource_uri", None)
        return bundle


##
def clean_post_data(post_data_dict):
    cleaned = {}
    for k, v in post_data_dict.iteritems():
        to_clean = v[0]
        cleaned_v = to_clean.replace("[u'", "").replace("]", "")
        cleaned[k] = cleaned_v

    return cleaned
