import json
from pprint import pprint
import datetime
from datetime import date

import re
import itertools
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.core.urlresolvers import reverse_lazy, reverse
from django.core.exceptions import ObjectDoesNotExist
from django.core import serializers
from django.views import generic
from django.views.decorators.cache import cache_control as django_cache_control
from django.contrib.auth.models import User,Group
from django.contrib.auth.decorators import login_required

from django.template import RequestContext

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

def dashboard_list(request):

    return render_to_response('dashboard-builder/list.html',
        context_instance=RequestContext(request))

def dashboard_builder(request,dashboard_id=None):

    return render_to_response('dashboard-builder/index.html', {'dashboard_id': dashboard_id },
        context_instance=RequestContext(request))

def chart_builder(request,dashboard_id):

    return render_to_response('dashboard-builder/chart_builder.html', {'dashboard_id': dashboard_id },
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


class CampaignCreateView(PermissionRequiredMixin,generic.CreateView):

    model = Campaign
    success_url = '/ufadmin/campaigns'
    template_name = 'campaigns/create.html'
    permission_required = 'datapoints.add_campaign'


class CampaignUpdateView(PermissionRequiredMixin,generic.UpdateView):

    model=Campaign
    success_url = '/ufadmin/campaigns'
    template_name = 'campaigns/create.html'
    form_class = CampaignForm
    # permission_required = 'datapoints.change_campaign'


    ##################
    ##################
    ### INDICATORS ###
    ##################
    ##################


class IndicatorCreateView(PermissionRequiredMixin,generic.CreateView):

    model = Indicator
    success_url= '/ufadmin/indicators'
    template_name = 'indicators/create.html'
    permission_required = 'datapoints.add_indicator'


class IndicatorUpdateView(PermissionRequiredMixin,generic.UpdateView):

    model = Indicator
    success_url = '/ufadmin/indicators'
    template_name = 'indicators/upsert.html'
    permission_required = 'datapoints.change_indicator'

    ###############
    ### REGIONS ###
    ###############


class RegionCreateView(PermissionRequiredMixin,generic.CreateView):

    model=Region
    template_name='regions/create.html'
    permission_required = 'datapoints.add_region'
    form_class = RegionForm
    success_url= '/ufadmin/regions'

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
    success_url = '/ufadmin/regions'
    template_name = 'regions/update.html'
    permission_required = 'datapoints.change_region'


class UFAdminView(IndexView):

    model = Region
    template_name = 'ufadmin/index.html'
    context_object_name = 'uf_admin'


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

    return HttpResponseRedirect(reverse('datapoints:cache_control'))


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


def refresh_metadata(request):
    '''
    This is what happens when you click the "refresh_metadata" button
    '''

    indicator_cache_data = cache_tasks.cache_indicator_abstracted()
    user_cache_data = cache_tasks.cache_user_abstracted()
    user_permission_data = cache_tasks.cache_user_permissions()

    return HttpResponseRedirect(reverse('datapoints:cache_control'))


class GroupCreateView(PermissionRequiredMixin, generic.CreateView):

    model = Group
    template_name = 'group_create.html'


class GroupEditView(PermissionRequiredMixin,generic.UpdateView):

    model = Group
    template_name = 'group_update.html'

    def get_success_url(self):

        requested_group_id = self.get_object().id

        return reverse_lazy('datapoints:group_update',kwargs={'pk':
            requested_group_id})

    def get_context_data(self, **kwargs):

        context = super(GroupEditView, self).get_context_data(**kwargs)
        group_obj = self.get_object()
        context['group_id'] = group_obj.id

        return context

class UserCreateView(PermissionRequiredMixin,generic.CreateView):

    model = User
    template_name = 'user_create.html'
    form_class = UserCreateForm

    def form_valid(self, form):

        new_user = form.save()

        return HttpResponseRedirect(reverse('datapoints:user_update', \
            kwargs={'pk':new_user.id}))


class UserEditView(PermissionRequiredMixin,generic.UpdateView):

    model = User
    template_name = 'user_edit.html'
    form_class = UserEditForm

    def get_success_url(self):

        requested_user_id = self.get_object().id

        return reverse_lazy('datapoints:user_update',kwargs={'pk':
            requested_user_id})

    def get_context_data(self, **kwargs):

        context = super(UserEditView, self).get_context_data(**kwargs)
        user_obj = self.get_object()
        context['user_id'] = user_obj.id

        return context

def v2_meta_api(request,content_type):

    return v2_api(request,content_type,True)


@django_cache_control(must_revalidate=True, max_age=3600,private=True)
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
