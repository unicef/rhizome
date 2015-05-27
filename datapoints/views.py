import json
from pprint import pprint
import datetime
from datetime import date

import gspread
import re
import itertools
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.core.urlresolvers import reverse_lazy, reverse
from django.core.exceptions import ObjectDoesNotExist
from django.core import serializers
from django.views import generic
from django.contrib.auth.models import User,Group
from django.contrib.auth.decorators import login_required

from django.template import RequestContext

from guardian.shortcuts import get_objects_for_user
from pandas import read_csv
from pandas import DataFrame
from functools import partial

from datapoints.models import *
from datapoints.forms import *
from datapoints import cache_tasks
from datapoints.mixins import PermissionRequiredMixin
from datapoints.api.v2 import v2PostRequest, v2GetRequest, v2MetaRequest


class IndexView(generic.ListView):
    paginate_by = 20

    def get_queryset(self):
        return self.model.objects.order_by('-created_at')

    ###################
    ###################
    ### DATA POINTS ###
    ###################
    ###################

class DataPointIndexView(IndexView):

    model=DataPoint
    template_name = 'datapoints/index.html'
    context_object_name = 'top_datapoints'


def data_entry(request):

    return render_to_response('data-entry/index.html',
        context_instance=RequestContext(request))

def dashboard_builder(request):

    return render_to_response('dashboard-builder/index.html',
        context_instance=RequestContext(request))

def visualization_builder(request):

    return render_to_response('dashboard-builder/visualization_builder.html',
        context_instance=RequestContext(request))


class DashBoardView(IndexView):
    paginate_by = 50

    template_name = 'dashboard/index.html'
    context_object_name = 'user_dashboard'

    def get_queryset(self):
        return DataPoint.objects.all()[:1]


    #################
    ### CAMPAIGNS ###
    #################

class CampaignIndexView(IndexView):

    model = Campaign
    template_name = 'campaigns/index.html'
    context_object_name = 'top_campaigns'


class CampaignCreateView(PermissionRequiredMixin,generic.CreateView):

    model = Campaign
    success_url = reverse_lazy('datapoints:campaign_index')
    template_name = 'campaigns/create.html'
    permission_required = 'datapoints.add_campaign'


class CampaignUpdateView(PermissionRequiredMixin,generic.UpdateView):

    model=Campaign
    success_url = reverse_lazy('datapoints:campaign_index')
    template_name = 'campaigns/create.html'
    form_class = CampaignForm
    # permission_required = 'datapoints.change_campaign'


    ##################
    ##################
    ### INDICATORS ###
    ##################
    ##################


class IndicatorIndexView(IndexView):

    model = Indicator
    template_name = 'indicators/index.html'
    context_object_name = 'top_indicators'

    paginate_by = 10000


class IndicatorCreateView(PermissionRequiredMixin,generic.CreateView):

    model = Indicator
    success_url= reverse_lazy('datapoints:indicator_index')
    template_name = 'indicators/create.html'
    permission_required = 'datapoints.add_indicator'


class IndicatorUpdateView(PermissionRequiredMixin,generic.UpdateView):

    model = Indicator
    success_url = reverse_lazy('datapoints:indicator_index')
    template_name = 'indicators/update.html'
    permission_required = 'datapoints.change_indicator'

    ###############
    ### REGIONS ###
    ###############

class RegionIndexView(IndexView):

    model = Region
    template_name = 'regions/index.html'
    context_object_name = 'top_regions'

class RegionCreateView(PermissionRequiredMixin,generic.CreateView):

    model=Region
    template_name='regions/create.html'
    permission_required = 'datapoints.add_region'
    form_class = RegionForm
    success_url=reverse_lazy('datapoints:region_index')


    def form_valid(self, form):
        # this inserts into the changed_by field with  the user who made the insert

        obj = form.save(commit=False)
        obj.changed_by = self.request.user
        obj.source_id = Source.objects.get(source_name='data entry').id
        obj.source_id = -1

        obj.save()
        return HttpResponseRedirect(self.success_url)


class RegionUpdateView(PermissionRequiredMixin,generic.UpdateView):

    model = Region
    success_url = reverse_lazy('datapoints:region_index')
    template_name = 'regions/update.html'
    permission_required = 'datapoints.change_region'


    ##########################
    ## PERMISSION CREATION ###
    ##########################

def view_user_permissions(request):

    # user_id = request.user.id

    # region_permissions = RegionPermission.objects.filter(user_id = user_id).values()
    region_permissions = RegionPermission.objects.all()

    return render_to_response('xtra/user_permissions.html',\
        {'region_permissions':region_permissions},\
        context_instance=RequestContext(request))


class RegionPermissionCreateView(PermissionRequiredMixin,generic.CreateView):

    model=RegionPermission
    template_name='xtra/create_region_permissions.html'
    form_class = RegionPermissionForm
    success_url=reverse_lazy('datapoints:view_user_permissions')


    ##############################
    ##############################
    #### FUNCTION BASED VIEWS ####
    ##############################
    ##############################

def cache_control(request):

    cache_jobs = CacheJob.objects.all().\
        exclude(response_msg='NOTHING_TO_PROCESS').order_by('-id')

    return render_to_response('cache_control.html',{'cache_jobs':cache_jobs},
    context_instance=RequestContext(request))


def refresh_cache(request):

    cr = cache_tasks.CacheRefresh()

    return HttpResponseRedirect('/datapoints/cache_control/')

def test_data_coverage(request):

    failed = ReconData.objects.raw("SELECT * FROM fn_test_data_accuracy()")

    final_qa_data = []
    for row in failed:
        row_d = {'region_id':row.region_id,
    	'campaign_id':row.campaign_id,
        'indicator_id':row.indicator_id,
        'target_value':row.target_value,
        'actual_value':row.actual_value}

        final_qa_data.append(row_d)

    test_count = ReconData.objects.count()
    qa_score = 1 - float((len(final_qa_data))/ float(test_count))

    return render_to_response('qa_data.html',
        {'qa_data': final_qa_data, 'qa_score':qa_score},\
        context_instance=RequestContext(request))

def qa_failed(request,region_id,campaign_id,indicator_id):
    # http://localhost:8000/datapoints/qa_failed/233/12910/99

    '''
    for an indicator_id, region_id, campaign_id, value try to figure out
    why the data is in correct.
    '''

    expected_value = ReconData.objects.get(region_id=region_id\
        ,campaign_id=campaign_id,indicator_id=indicator_id).target_value

    try:
        actual_value = DataPointComputed.objects.get(region_id=region_id\
            ,campaign_id=campaign_id,indicator_id=indicator_id).value
    except ObjectDoesNotExist:
        actual_value = None

    md_array = []
    sub_md_array = []

    md = ReconData.objects.raw('''
    SELECT
    	rd.id
    	,cic.indicator_component_id
    	,cic.calculation
    	,rd.region_id
    	,rd.indicator_id
        ,COALESCE(CAST(ad.value AS VARCHAR),'MISSING') as actual_value
    FROM recon_data rd
    INNER JOIN calculated_indicator_component cic
    ON rd.indicator_id = cic.indicator_id
    AND cic.indicator_id = %s
    AND rd.region_id = %s
    AND rd.campaign_id = %s
    LEFT JOIN agg_datapoint ad
    ON cic.indicator_component_id = ad.indicator_id
    AND ad.region_id = rd.region_id
    AND ad.campaign_id = rd.campaign_id
    ;''',[indicator_id,region_id,campaign_id])

    for row in md:
        row_dict = {
            'campaign_id': row.campaign_id,
            'indicator_id': row.indicator_id,
            'region_id': row.region_id,
            'actual_value': row.actual_value,
        }

        md_array.append(row_dict)

    sub_md = ReconData.objects.raw('''
    SELECT
    	rd.id
    	,cic.indicator_component_id
    	,cic.calculation
    	,r.id as region_id
    	,rd.indicator_id
    	,COALESCE(CAST(ad.value AS VARCHAR),'MISSING') actual_value
    FROM recon_data rd
    INNER JOIN calculated_indicator_component cic
    ON rd.indicator_id = cic.indicator_id
    AND cic.indicator_id = %s
    AND rd.region_id = %s
    AND rd.campaign_id = %s
    INNER JOIN region r
    ON rd.region_id = r.parent_region_id
    LEFT JOIN agg_datapoint ad
    ON cic.indicator_component_id = ad.indicator_id
    AND ad.region_id = r.id
    AND ad.campaign_id = rd.campaign_id''',[indicator_id,region_id,campaign_id])

    for row in sub_md:
        row_dict = {
            'campaign_id': row.campaign_id,
            'indicator_id': row.indicator_id,
            'region_id': row.region_id,
            'actual_value': row.actual_value,
        }

        sub_md_array.append(row_dict)


    return render_to_response('missing_data.html',{'calculation_breakdown':\
        md_array,'region_id':region_id,'campaign_id':campaign_id,\
        'indicator_id':indicator_id,'expected_value':expected_value
        ,'actual_value':actual_value,'sub_region_calculation_breakdown':sub_md_array}
        ,context_instance=RequestContext(request))

####

def parse_url_args(request,keys):

    request_meta = {}

    for k in keys:

        try:
            request_meta[k] = request.GET[k]
        except KeyError:
            request_meta[k] = None

    return request_meta


def api_campaign(request):

    meta_keys = ['id','region__in','start_date','limit','offset']

    request_meta = parse_url_args(request,meta_keys)

    if request_meta['region__in']:

        c_raw = Campaign.objects.raw("""
            SELECT * FROM campaign WHERE id in (
                SELECT DISTINCT campaign_id FROM datapoint_with_computed
                WHERE region_id IN (%s)
            )
            """,[request_meta['region__in']])

    elif request_meta['id']:

        c_raw  = Campaign.objects.raw("""
            SELECT * FROM campaign c
            WHERE id = %s
            ;""",[request_meta['id'],request_meta['limit']\
            ,request_meta['offset']])

    else:

        c_raw  = Campaign.objects.raw("""SELECT * FROM campaign c ORDER BY \
            c.start_date desc;""")

    objects = [{'id': c.id, 'slug':c.slug, 'office_id':c.office_id, \
        'start_date': str(c.start_date), 'end_date': str(c.end_date )} \
            for c in c_raw]

    meta = { 'limit': request_meta['limit'],'offset': request_meta['offset'],\
        'total_count': len(objects)}

    response_data = {'objects':objects, 'meta':meta}

    return HttpResponse(json.dumps(response_data)\
        , content_type="application/json")


def api_region(request):

    meta_keys = ['limit','offset']
    request_meta = parse_url_args(request,meta_keys)

    r_raw = Campaign.objects.raw("SELECT * FROM region")

    objects = [{'id': r.id,'name': r.name, 'office_id':r.office_id, 'parent_region_id':\
        r.parent_region_id, 'region_type_id': r.region_type_id} for r in r_raw]

    meta = { 'limit': request_meta['limit'],'offset': request_meta['offset'],\
        'total_count': len(objects)}

    response_data = {'objects':objects, 'meta':meta}

    return HttpResponse(json.dumps(response_data)\
        , content_type="application/json")


def refresh_metadata(request):

    indicator_cache_data = cache_tasks.cache_indicator_abstracted()
    user_cache_data = cache_tasks.cache_user_abstracted()

    return HttpResponseRedirect('/datapoints/cache_control/')


def api_indicator(request):
    '''
    TO BE REMOVED - Once transfer from v1/api to v2/api
    '''

    meta_keys = ['limit','offset']
    request_meta = parse_url_args(request,meta_keys)

    try:
        id__in = [int(ind_id) for ind_id in request.GET['id__in'].split(',')]
    except KeyError:
        id__in = [i for i in Indicator.objects.all().values_list('id',flat=True)]


    i_raw = Indicator.objects.raw("""
        SELECT
            i.*
            ,ia.bound_json
        FROM indicator i
        INNER JOIN indicator_abstracted ia
        ON i.id = ia.id
        WHERE i.id = ANY(%s)
        ORDER BY i.id
    """,[id__in])

    objects = [{'id':i.id, 'short_name':i.short_name,'name':i.name,\
                'description':i.description,'slug':i.slug,\
                'indicator_bounds':json.loads(i.bound_json)} for i in i_raw]

    meta = { 'limit': request_meta['limit'],'offset': request_meta['offset'],\
        'total_count': len(objects)}

    response_data = {'objects':objects, 'meta':meta}

    return HttpResponse(json.dumps(response_data)\
        , content_type="application/json")


class UserCreateView(PermissionRequiredMixin,generic.CreateView):

    model = User
    template_name = 'user_create.html'
    form_class = UserCreateForm
    # permission_required = 'datapoints.add_campaign'

    def form_valid(self, form):

        new_user = form.save()

        return HttpResponseRedirect(reverse('datapoints:user_edit', \
            kwargs={'pk':new_user.id}))


class UserEditView(PermissionRequiredMixin,generic.UpdateView):

    model = User
    template_name = 'user_edit.html'
    form_class = UserEditForm

    def get_success_url(self):

        requested_user_id = self.get_object().id

        return reverse_lazy('datapoints:user_edit',kwargs={'pk':
            requested_user_id})

    def get_context_data(self, **kwargs):

        context = super(UserEditView, self).get_context_data(**kwargs)
        user_obj = self.get_object()
        context['user_id'] = user_obj.id

        return context

def v2_meta_api(request,content_type):

    return v2_api(request,content_type,True)

@login_required
def v2_api(request,content_type,is_meta=False):

    if is_meta:
        request_object = v2MetaRequest(request, content_type)
        data = request_object.main()

    ## Handles Delete and Update.
    elif request.POST:
        request_object = v2PostRequest(request, content_type)
        data = request_object.main()

    else:
        request_object = v2GetRequest(request, content_type)
        data = request_object.main()

    return HttpResponse(json.dumps(data),content_type="application/json")
