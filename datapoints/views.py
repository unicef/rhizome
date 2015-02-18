from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy
from django.views import generic
from django.template import RequestContext
from guardian.shortcuts import get_objects_for_user


from datapoints.models import DataPoint,Region,Indicator,Source
from datapoints.forms import *
from datapoints.cache_tasks.pivot_datapoint import full_cache_refresh

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

        CREATE TABLE datapoint_with_computed AS

        SELECT
        id
        ,indicator_id
        ,region_id
        ,campaign_id
        ,value
        ,is_agg
        ,CAST(0 as BOOLEAN) as is_calc
        FROM agg_datapoint;

        -- make ID column auto increment
        DROP SEQUENCE IF EXISTS dwc_seq;
        CREATE SEQUENCE dwc_seq;
        ALTER TABLE datapoint_with_computed ALTER COLUMN id SET DEFAULT nextval('dwc_seq');
        --ALTER TABLE datapoint_with_computed ALTER COLUMN id SET NOT NULL;
        ALTER SEQUENCE dwc_seq OWNED BY datapoint_with_computed.id;

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
        ON 1=1
        INNER JOIN calculated_indicator_component whole
        ON part.indicator_id = whole.indicator_id
        AND whole.calculation = 'WHOLE'
        AND part.calculation = 'PART'
        INNER JOIN agg_datapoint d_part
        ON part.indicator_component_id = d_part.indicator_id
        INNER JOIN agg_datapoint d_whole
        ON whole.indicator_component_id = d_whole.indicator_id
        AND d_part.campaign_id = d_whole.campaign_id
        AND d_part.region_id = d_whole.region_id;


        ----- SUM OF PARTS ------
        INSERT INTO datapoint_with_computed
        (indicator_id,region_id,campaign_id,value,is_calc)

        SELECT
        i_part.indicator_id
        ,region_id
        ,campaign_id
        ,SUM(ad.value) as value
        ,CAST(1 as BOOLEAN) as is_calc
        FROM calculated_indicator_component i_part
        INNER JOIN agg_datapoint ad
        ON i_part.indicator_component_id = ad.indicator_id
        WHERE i_part.calculation = 'PART_TO_BE_SUMMED'
        GROUP BY i_part.indicator_id,region_id,campaign_id;

        GRANT SELECT ON datapoint_with_computed TO djangoapp;

        INSERT INTO datapoint_with_computed
        (indicator_id,region_id,campaign_id,value,is_calc)
        SELECT
        x.indicator_id
        ,x.region_id
        ,x.campaign_id
        ,x.calc_value
        ,CAST(1 as BOOLEAN) as is_calc
        FROM (
          SELECT
          part.to_calc_ind_id  as indicator_id
          ,part.region_id
          ,part.campaign_id
          ,(whole.value - part.value) / NULLIF(whole.value,0) as calc_value
          FROM (
            SELECT d.value, d.region_id, d.campaign_id, d.indicator_id, cic.calculation, cic.indicator_id as to_calc_ind_id
            FROM calculated_indicator_component cic
            INNER JOIN datapoint d
            ON cic.indicator_component_id = d.indicator_id
            WHERE calculation = 'PART_OF_DIFFERENCE'
          ) part
          INNER JOIN (
            SELECT d.value, d.region_id, d.campaign_id, d.indicator_id, cic.calculation, cic.indicator_id as to_calc_ind_id
            FROM calculated_indicator_component cic
            INNER JOIN datapoint d
            ON cic.indicator_component_id = d.indicator_id
            WHERE calculation = 'WHOLE_OF_DIFFERENCE'
          ) whole
          ON part.to_calc_ind_id = whole.to_calc_ind_id
          AND part.region_id = whole.region_id
          AND part.campaign_id = whole.campaign_id
        )x
        WHERE x.calc_value IS NOT NULL;

        SELECT id FROM agg_datapoint LIMIT 1;

    """)

    for x in curs:
        print x

    return HttpResponseRedirect('/datapoints/regions/')



def agg_datapoint(request):

    # insert leave level data #

    DataPoint.objects.raw("""

    TRUNCATE TABLE agg_datapoint;

    INSERT INTO agg_datapoint
    (region_id, campaign_id, indicator_id, value, is_agg)

    SELECT
        region_id, campaign_id, indicator_id, value, 't'
    FROM datapoint d;
    """)

    region_loop = {
        0 : 'settlement',
        1 : 'sub-district',
        2 : 'district',
        3 : 'province',
        # 4 : 'country',
    }

    for k,v in region_loop.iteritems():

        curs = DataPoint.objects.raw("""
            INSERT INTO agg_datapoint
            (region_id, campaign_id, indicator_id, value, is_agg)

            SELECT
                r.parent_region_id, campaign_id, indicator_id, SUM(value), 't'
            FROM agg_datapoint ag
            INNER JOIN region r
                ON ag.region_id = r.id
            INNER JOIN region_type rt
                ON r.region_type_id = rt.id
                AND rt.name = %s
            GROUP BY r.parent_region_id, ag.indicator_id, ag.campaign_id;

        SELECT id FROM agg_datapoint LIMIT 1;
        """,[v])

        for x in curs:
            print x


    return HttpResponseRedirect('/datapoints/regions/')




def pivot_datapoint(request):

    full_cache_refresh()

    return HttpResponseRedirect('/datapoints/regions/')
