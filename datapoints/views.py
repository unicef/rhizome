from django.shortcuts import get_object_or_404, render, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse, reverse_lazy
from django.views import generic
from django.contrib.auth.decorators import permission_required
from django.utils.decorators import method_decorator
from django.db import connection
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


def pivot_datapoint(request):

    full_cache_refresh()

    return HttpResponseRedirect('/datapoints/regions/')
