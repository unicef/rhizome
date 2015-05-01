import json
from pprint import pprint

from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.core.urlresolvers import reverse_lazy
from django.core.exceptions import ObjectDoesNotExist
from django.core import serializers
from django.views import generic
from django.contrib.auth.models import User,Group
from django.template import RequestContext
from guardian.shortcuts import get_objects_for_user
from pandas import read_csv
from pandas import DataFrame
import gspread
import re
import itertools
from functools import partial

from datapoints.models import DataPoint,Region,Indicator,Source,ReconData
from datapoints.forms import *
from datapoints.cache_tasks import CacheRefresh,cache_indicator_abstracted

from datapoints.mixins import PermissionRequiredMixin

USER_METADATA = 'static/users_metadata_mockup.json'
DEFAULT_LIMIT = 50
MAX_LIMIT = 500


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

    def get_queryset(self):

        ## if this user has permissions to view entire office
        ## then find the regions that fall under that
        offices = get_objects_for_user(self.request.user,
            'datapoints.view_office')
        if offices:
            regions = Region.objects.filter(office=offices)

        ## now check to see if they have region level permissions
        else:
            regions = get_objects_for_user(self.request.user
                , 'datapoints.view_region')

        ## TO DO : find all of the sub regions of the regions
        ##         the user is permitted to see

        regions_leaf_level = regions #some recursive query

        ## now get all the relevant data points
        dps = DataPoint.objects.filter(region=regions_leaf_level)

        return dps

class DataEntryView(IndexView):

    model=DataPoint
    template_name = 'data-entry/index.html'
    context_object_name = 'top_datapoints'

    def get_queryset(self):

        ## TO DO: add indicator set page and permissions

        ## if this user has permissions to view entire office
        ## then find the regions that fall under that
        offices = get_objects_for_user(self.request.user,
            'datapoints.view_office')
        if offices:
            regions = Region.objects.filter(office=offices)

        ## now check to see if they have region level permissions
        else:
            regions = get_objects_for_user(self.request.user
                , 'datapoints.view_region')

        ## TO DO : find all of the sub regions of the regions
        ##         the user is permitted to see

        regions_leaf_level = regions #some recursive query

        ## now get all the relevant data points
        dps = DataPoint.objects.filter(region=regions_leaf_level)

        return dps

class DashBoardView(IndexView):
    paginate_by = 50

    template_name = 'dashboard/index.html'
    context_object_name = 'user_dashboard'

    def get_queryset(self):
        return DataPoint.objects.all()[:1]

class DataPointCreateView(PermissionRequiredMixin, generic.CreateView):

    model=DataPoint
    success_url=reverse_lazy('datapoints:datapoint_index')
    template_name='datapoints/create.html'
    form_class = DataPointForm
    permission_required = 'datapoints.add_datapoint'

    def form_valid(self, form):
    # this inserts into the changed_by field with  the user who made the insert
        obj = form.save(commit=False)
        obj.changed_by = self.request.user
        obj.source_id = Source.objects.get(source_name='data entry').id
        obj.source_datapoint_id = -1

        obj.save()
        return HttpResponseRedirect(self.success_url)

class DataPointUpdateView(PermissionRequiredMixin,generic.UpdateView):

    model=DataPoint
    success_url = reverse_lazy('datapoints:datapoint_index')
    template_name = 'datapoints/update.html'
    form_class = DataPointForm
    permission_required = 'datapoints.change_datapoint'

    def form_valid(self, form):
    # this sets the changed_by field to the user who made the update
        obj = form.save(commit=False)
        obj.changed_by = self.request.user
        obj.save()
        return HttpResponseRedirect(self.success_url)

class DataPointDeleteView(PermissionRequiredMixin,generic.DeleteView):

    model = DataPoint
    success_url = reverse_lazy('datapoints:datapoint_index');
    template_name ='datapoints/confirm_delete.html'
    permission_required = 'datapoints.delete_datapoint'

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
    success_url= reverse_lazy('indicators:indicator_index')
    template_name = 'indicators/create.html'
    permission_required = 'datapoints.add_indicator'


class IndicatorUpdateView(PermissionRequiredMixin,generic.UpdateView):

    model = Indicator
    success_url = reverse_lazy('indicators:indicator_index')
    template_name = 'indicators/update.html'
    permission_required = 'datapoints.change_indicator'



    ####################################
    ###### CALCULATED INDICATORS #######
    ####################################

class CalculatedIndicatorIndexView(IndexView):

    model = CalculatedIndicatorComponent
    template_name = 'indicators/calculated_index.html'
    context_object_name = 'top_calculated_indicators'


class CalculatedIndicatorCreateView(PermissionRequiredMixin,generic.CreateView):

    model = CalculatedIndicatorComponent
    success_url= reverse_lazy('indicators:calculated_indicator_index')
    template_name = 'indicators/create_calculated.html'
    # permission_required = 'datapoints.add_indicator'


    ###############
    ###############
    ### REGIONS ###
    ###############
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
    success_url=reverse_lazy('regions:region_index')


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
    success_url = reverse_lazy('regions:region_index')
    template_name = 'regions/update.html'
    permission_required = 'datapoints.change_region'

class RegionDeleteView(PermissionRequiredMixin,generic.DeleteView):

    model=Region
    success_url = reverse_lazy('regions:region_index')
    template_name = 'regions/confirm_delete.html'
    permission_required = 'datapoints.delete_region'


    ##############################
    ##############################
    #### FUNCTION BASED VIEWS ####
    ##############################
    ##############################


def search(request):

    if request.method =='POST':
      ## THIS IS UGLY ##
      kwargs = {}
      if request.POST['indicator'] != u'':
          kwargs.update({'indicator': request.POST['indicator']})
      if request.POST['region'] != u'':
          kwargs.update({'region': request.POST['region']})
      if request.POST['changed_by'] != u'':
          kwargs.update({'changed_by': request.POST['changed_by']})
      if request.POST['campaign'] != u'':
          kwargs.update({'campaign': request.POST['campaign']})

      results = DataPoint.objects.filter(**kwargs)

      return render_to_response('datapoints/index.html',
        {'top_datapoints':results},
        context_instance=RequestContext(request))

    else:
      return render_to_response('datapoints/search.html',
        {'form':DataPointSearchForm},
        context_instance=RequestContext(request))


def populate_dummy_ngo_dash(request):

    ng_dash_df = read_csv('datapoints/tests/_data/ngo_dash.csv')
    campaign_id = 201

    region_ids = []
    batch = []

    dist_r = ng_dash_df['region_id'].unique()

    for r in dist_r:

        df_filtered_by_region = ng_dash_df[ng_dash_df['region_id'] == r]

        valid_cols_df = df_filtered_by_region[['indicator_id','value']]
        ix_df = valid_cols_df.set_index('indicator_id')

        x = ix_df.to_dict()
        cleaned_json = json.dumps(x['value'], ensure_ascii=False)

        dda_dict = {
            'region_id': r,
            'campaign_id':campaign_id,
            'indicator_json':x['value']
        }

        DataPointAbstracted.objects.filter(campaign_id = campaign_id\
            , region_id = r).delete()

        DataPointAbstracted.objects.create(**dda_dict)

    return HttpResponseRedirect('/datapoints/cache_control/')


def cache_control(request):

    cache_jobs = CacheJob.objects.all().\
        exclude(response_msg='NOTHING_TO_PROCESS').order_by('-id')

    return render_to_response('cache_control.html',{'cache_jobs':cache_jobs},
    context_instance=RequestContext(request))


def refresh_cache(request):

    cr = CacheRefresh()

    return HttpResponseRedirect('/datapoints/cache_control/')

def load_gdoc_data(request):

    err_msg = 'none!'

    # gc = gspread.login(gdoc_u,gdoc_p)
    gc = gspread.login('fix','me')
    worksheet = gc.open("Master Dashboard QA").sheet1
    list_of_lists = worksheet.get_all_values()
    gd_df = DataFrame(list_of_lists[1:],columns = list_of_lists[0])
    gd_df = gd_df[gd_df['region_id'] != '0']
    gd_dict = gd_df.transpose().to_dict()

    batch = []

    for k,v in gd_dict.iteritems():

        if v['region_id'] == '#N/A':
            pass

        v['success_flag'] = 0
        recon_d = ReconData(**v)
        batch.append(recon_d)

    ReconData.objects.all().delete()

    try:
        ReconData.objects.bulk_create(batch)
    except Exception as err:
        err_msg = err

    return render_to_response('qa_data.html',
        {'err_msg': err_msg},context_instance=RequestContext(request))

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


def api_user(request):

    users = User.objects.all()
    for (k,v) in request.GET.iteritems():
        verb = k.split('.')[0]
        if verb == 'search':
            keywords = re.split('(?<!\\\)\ ', v.lower())
            users = _user_search(users, keywords)
        elif verb == 'filter':
            terms = k.split('.')
            users = _user_filter(users, terms, v)
        elif verb == 'sort':
            if 'sort_direction' in request.GET:
                sd = request.GET['sort_direction']
                try:
                    users = _user_sort(users, v, sd)
                except:
                    return HttpResponse({'error': 'Cannot Sort on Field'})
            else:
                users = _user_sort(users, v)
    if 'sort' not in request.GET:
        users = _user_sort(users, 'last_name', 'asc')
    offset = 0
    if 'offset' in request.GET:
        offset = int(request.GET['offset'])
    limit = DEFAULT_LIMIT
    if 'limit' in request.GET:
        limit = int(request.GET['limit'])
    my_users = [ MyUser(pk=u.id).get_dict() for u in users ]
    my_users = my_users[offset:offset+limit]
    total_count = len(my_users)
    resp = {}
    resp['error'] = None
    resp['meta'] = {
        'limit': limit,
        'offset': offset,
        'total_count': total_count
    }
    resp['objects'] = my_users
    resp['requested_params'] = [ {k: v} for (k,v) in request.GET.iteritems()]
    return HttpResponse(json.dumps(resp),
            content_type='application/json')



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


def transform_indicators(request):

    response_data = cache_indicator_abstracted()

    return HttpResponse(json.dumps(response_data)\
        , content_type="application/json")


def api_indicator(request):

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
        ON i.id = ia.indicator_id
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


def bad_data(request):

    dp_curs = BadData.objects.raw('''
        SELECT * FROM bad_data
    ''')

    dp_data = [{'id':dp.id, 'error_type':dp.error_type, 'doc_id':dp.document_id} for\
        dp in dp_curs]

    return render_to_response('bad_data.html',{'dp_data':dp_data}
        ,context_instance=RequestContext(request))
