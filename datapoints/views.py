from django.shortcuts import get_object_or_404, render, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse, reverse_lazy
from django.views import generic
from django.contrib.auth.decorators import permission_required
from django.utils.decorators import method_decorator
from django.db import connection
from django.template import RequestContext
from guardian.shortcuts import get_objects_for_user

from datapoints.sql_queries import *
from datapoints.models import DataPoint,Region,Indicator,Document
from datapoints.forms import * #RegionForm,IndicatorForm,DataPointForm,DocumentForm,DataPointSearchForm

from datapoints.mixins import PermissionRequiredMixin

class IndexView(generic.ListView):
    paginate_by = 5

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

class DashBoardView(IndexView):
    paginate_by = 50

    template_name = 'dashboard/index.html'
    context_object_name = 'user_dashboard'

    def raw_query(self, sql_string):
      cursor = connection.cursor()
      cursor.execute(sql_string)
      rows = cursor.fetchall()

      return rows

    def get_queryset(self):
        rows = []
        ind_pct = self.raw_query(show_indicator_pct_aggregation)
        region_agg = self.raw_query(show_region_aggregation)

        for row in ind_pct:
            rows.append(row)

        for row in region_agg:
            rows.append(row)


        return rows

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


    ##################
    ##################
    ### INDICATORS ###
    ##################
    ##################


class IndicatorIndexView(IndexView):

    model = Indicator
    template_name = 'indicators/index.html'
    context_object_name = 'top_indicators'

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

    #####################
    ### INDICATOR PCT ###
    #####################

class IndicatorPctIndexView(IndexView):

    model = IndicatorPct
    template_name = 'indicator_pct/index.html'
    context_object_name = 'top_indicator_pct'

class IndicatorPctCreateView(PermissionRequiredMixin,generic.CreateView):

    model = IndicatorPct
    success_url = reverse_lazy('indicators:indicator_pct_index')
    template_name = 'indicator_pct/create.html'
    permission_required = 'datapoints.add_indicatorpct'


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
    success_url = reverse_lazy('regions:create_region_relationship')
    template_name='regions/create.html'
    permission_required = 'datapoints.add_region'


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

    ############################
    ### REGION RELATIONSHIPS ###
    ############################

class RegionRelationshipIndexView(IndexView):
    model = RegionRelationship
    template_name = 'region_relationships/index.html'
    context_object_name = 'top_region_relationships'

class RegionRelationshipCreateView(PermissionRequiredMixin,generic.CreateView):

    model = RegionRelationship
    success_url = reverse_lazy('regions:region_index')
    template_name = 'region_relationships/create.html'
    permission_required = 'datapoints.add_regionrelationship'


    ##################################
    ### REGION RELATIONSHIPS TYPES ###
    ##################################

class RegionRelagionshipTypeIndexView(IndexView):

    model = RegionRelationshipType
    template_name = 'region_relationships/type_index.html'
    context_object_name = 'top_region_relationship_types'

class RegionRelationshipTypeCreateView(PermissionRequiredMixin,
    generic.CreateView):

    model = RegionRelationshipType
    success_url = reverse_lazy('regions:region_index')
    template_name = 'region_relationships/type_create.html'
    permission_required = 'datapoints.add_regionrelationship'


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


def file_upload(request):
    # Handle file upload
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = Document(docfile = request.FILES['docfile'])
            newdoc.save()

    else:
        form = DocumentForm() # A empty, unbound form

    # Load documents for the list page
    documents = Document.objects.all()

    # Render list page with the documents and the form
    return render_to_response(
        'datapoints/file_upload.html',
        {'documents': documents, 'form': form},
        context_instance=RequestContext(request)
    )
