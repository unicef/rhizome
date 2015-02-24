import json
from pprint import pprint

from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy
from django.views import generic
from django.template import RequestContext
from guardian.shortcuts import get_objects_for_user
from pandas import read_csv
from pandas import DataFrame
import gspread

from datapoints.models import DataPoint,Region,Indicator,Source
from datapoints.forms import *
from datapoints.cache_tasks.pivot_datapoint import full_cache_refresh
from polio.secrets import gdoc_u, gdoc_p

from datapoints.mixins import PermissionRequiredMixin


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


class IndicatorDeleteView(PermissionRequiredMixin,generic.DeleteView):

    model = Indicator
    success_url = reverse_lazy('indicators:indicator_index')
    template_name = 'indicators/confirm_delete.html'
    permission_required = 'datapoints.delete_indicator'

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
        obj.source_region_id = -1

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


def calc_datapoint(request):

    curs = DataPoint.objects.raw("""
    	DROP TABLE IF EXISTS datapoint_with_computed;

    	CREATE TABLE datapoint_with_computed
    	(
    		id SERIAL
    		,indicator_id INTEGER
    		,region_id INTEGER
    		,campaign_id INTEGER
    		,value FLOAT
    		,is_agg BOOLEAN
    		,is_calc BOOLEAN
    	);

    	INSERT INTO datapoint_with_computed
    	(indicator_id,region_id,campaign_id,value,is_agg,is_calc)

    	SELECT
    		indicator_id
    		,region_id
    		,campaign_id
    		,value
    		,is_agg
    		,CAST(0 as BOOLEAN) as is_calc
    	FROM agg_datapoint;

    	CREATE UNIQUE INDEX  dwc_uq_ix on datapoint_with_computed (region_id, indicator_id, campaign_id);

        ---- SUM OF PARTS ------
        INSERT INTO datapoint_with_computed
        (indicator_id,region_id,campaign_id,value,is_calc)

        SELECT
        	cic.indicator_id
        	,ad.region_id
        	,ad.campaign_id
        	,SUM(ad.value) as value
            ,'t'
        FROM agg_datapoint ad
        INNER JOIN calculated_indicator_component cic
        ON ad.indicator_id = cic.indicator_component_id
        AND cic.calculation = 'PART_TO_BE_SUMMED'
        GROUP BY ad.campaign_id, ad.region_id, cic.indicator_id;

        ----- PART / WHOLE ------
        INSERT INTO datapoint_with_computed
        (indicator_id,region_id,campaign_id,value,is_calc)

        SELECT
        part.indicator_id as master_indicator_id
        ,d_part.region_id
        ,d_part.campaign_id
        ,d_part.value / NULLIF(d_whole.value,0) as value
        ,CAST(1 as BOOLEAN) as is_calc
        FROM(
          SELECT max(id) as max_dp_id FROM datapoint_with_computed
        ) x
        INNER JOIN calculated_indicator_component part
            ON 1 = 1
        INNER JOIN calculated_indicator_component whole
            ON part.indicator_id = whole.indicator_id
            AND whole.calculation = 'WHOLE'
            AND part.calculation = 'PART'
        INNER JOIN datapoint_with_computed d_part
            ON part.indicator_component_id = d_part.indicator_id
        INNER JOIN datapoint_with_computed d_whole
            ON whole.indicator_component_id = d_whole.indicator_id
            AND d_part.campaign_id = d_whole.campaign_id
            AND d_part.region_id = d_whole.region_id;

        CREATE INDEX ind_ix on datapoint_with_computed (indicator_id);
        CLUSTER datapoint_with_computed using ind_ix;

        INSERT INTO datapoint_with_computed
        (indicator_id,region_id,campaign_id,value,is_calc)


        SELECT
			denom.master_indicator_id
          		,denom.region_id
          		,denom.campaign_id
          		,(CAST(num_whole.value as FLOAT) - CAST(num_part.value as FLOAT)) / NULLIF(CAST(denom.value AS FLOAT),0) as calculated_value
               , CAST(1 AS BOOLEAN) as is_calc
          FROM (
          	SELECT
          		cic.indicator_id as master_indicator_id
          		,ad.region_id
          		,ad.indicator_id
          		,ad.campaign_id
          		,ad.value
          	FROM agg_datapoint ad
          	INNER JOIN calculated_indicator_component cic
          	ON cic.indicator_component_id = ad.indicator_id
          	AND calculation = 'PART_OF_DIFFERENCE'
          )num_part

          INNER JOIN (
          	SELECT
          		cic.indicator_id as master_indicator_id
          		,ad.region_id
          		,ad.indicator_id
          		,ad.campaign_id
          		,ad.value
          	FROM agg_datapoint ad
          	INNER JOIN calculated_indicator_component cic
          	ON cic.indicator_component_id = ad.indicator_id
          	AND calculation = 'WHOLE_OF_DIFFERENCE'

          )num_whole
          ON num_part.master_indicator_id = num_whole.master_indicator_id
          AND num_part.region_id = num_whole.region_id
          AND num_part.campaign_id = num_whole.campaign_id

          INNER JOIN
          (
          	SELECT
          		cic.indicator_id as master_indicator_id
          		,ad.region_id
          		,ad.indicator_id
          		,ad.campaign_id
          		,ad.value
          	FROM agg_datapoint ad
          	INNER JOIN calculated_indicator_component cic
          	ON cic.indicator_component_id = ad.indicator_id
          	AND calculation = 'WHOLE_OF_DIFFERENCE_DENOMINATOR'
          )denom
          ON num_whole.region_id = denom.region_id
          AND num_whole.master_indicator_id = denom.master_indicator_id
         AND num_whole.campaign_id = denom.campaign_id;

        SELECT id FROM datapoint_with_computed LIMIT 1;
    """)

    for x in curs:
        print x

    return HttpResponseRedirect('/datapoints/cache_control/')


def agg_datapoint(request):

    # insert leave level data #

    curs = DataPoint.objects.raw("""

    TRUNCATE TABLE agg_datapoint;

    INSERT INTO agg_datapoint
    (region_id, campaign_id, indicator_id, value, is_agg)

    SELECT
        region_id, campaign_id, indicator_id, value, 't'
    FROM datapoint d
    WHERE value != 'NaN';
    --

    DROP INDEX IF EXISTS ag_uq_ix;
    CREATE UNIQUE INDEX  ag_uq_ix on agg_datapoint (region_id, indicator_id, campaign_id);

    SELECT id from datapoint limit 1;

    """)

    for x in curs:
        print x


    region_loop = {
        0 : 'settlement',
        1 : 'sub-district',
        2 : 'district',
        3 : 'province',
        # 4 : 'country',
    }

    for k,v in region_loop.iteritems():

        print 'TRYING .... %s' % v

        curs = DataPoint.objects.raw("""
            INSERT INTO agg_datapoint
            (region_id, campaign_id, indicator_id, value, is_agg)

            SELECT
                r.parent_region_id, campaign_id, indicator_id, SUM(COALESCE(value,0)), 't'
            FROM agg_datapoint ag
            INNER JOIN region r
                ON ag.region_id = r.id
            INNER JOIN region_type rt
                ON r.region_type_id = rt.id
                AND rt.name = %s
            WHERE NOT EXISTS (
            	SELECT 1 FROM agg_datapoint ag_2
            	WHERE 1 = 1
            	AND ag.indicator_id = ag_2.indicator_id
            	AND ag.campaign_id = ag_2.campaign_id
            	AND r.parent_region_id = ag_2.region_id
            )
            GROUP BY r.parent_region_id, ag.indicator_id, ag.campaign_id;

        SELECT id FROM datapoint LIMIT 1;
        """,[v])

        for x in curs:
            print x


    return HttpResponseRedirect('/datapoints/cache_control/')


def populate_dummy_ngo_dash(request):

    ng_dash_df = read_csv('datapoints/tests/_data/ngo_dash.csv')
    campaign_id = 201

    region_ids = []
    batch = []

    dist_r = ng_dash_df['region_id'].unique()

    for r in dist_r:

        print r

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


def pivot_datapoint(request):

    full_cache_refresh()

    return HttpResponseRedirect('/datapoints/cache_control/')

def cache_control(request):


    return render_to_response('cache_control.html',
    context_instance=RequestContext(request))


def gdoc_qa(request):

    gc = gspread.login(gdoc_u,gdoc_p)
    worksheet = gc.open("Dashboard QA | February 2015").sheet1
    list_of_lists = worksheet.get_all_values()
    gd_df = DataFrame(list_of_lists[1:],columns = list_of_lists[0])

    gd_df = gd_df[gd_df['region_id'] != '0']
    gd_df = gd_df[gd_df['indicator_id'] == '431']


    gd_dict = gd_df.transpose().to_dict()

    final_qa_data = []

    for k,v in gd_dict.iteritems():

        try:
            dwc = DataPointComputed.objects.get(
                region_id = v['region_id'],
                campaign_id = v['campaign_id'],
                indicator_id = v['indicator_id'],
            )

            v['computed_value'] = dwc.value

            if abs(float(dwc.value) - float(v['value']))< .001:
                passed = 1
            else:
                passed = 0

        except Exception:
            v['computed_value'] = -1
            passed = 0

        v['passed'] = passed

        if passed == 0:
            final_qa_data.append(v)


    indicator_breakdown = []
    missed_by_ind_id = DataFrame(final_qa_data).groupby('indicator_id')\
        .agg('count').transpose().to_dict()

    for k,v in missed_by_ind_id.iteritems():
        ind_dict = {'indicator_id':k ,'count_missed': v['value']}
        indicator_breakdown.append(ind_dict)

    qa_score = 1 - float((len(final_qa_data))/ float(len(gd_df)))

    return render_to_response('qa_data.html',
        {'qa_data': final_qa_data, 'qa_score':qa_score\
        ,'indicator_breakdown':indicator_breakdown},
        context_instance=RequestContext(request))
