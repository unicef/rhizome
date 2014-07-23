from django.shortcuts import get_object_or_404, render, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.views import generic
from django.contrib.auth.decorators import permission_required
from django.utils.decorators import method_decorator
from django.db import connection
from django.template import RequestContext

from datapoints.sql_queries import show_dashboard
from datapoints.models import DataPoint,Region,Indicator,Document
from datapoints.forms import * #RegionForm,IndicatorForm,DataPointForm,DocumentForm,DataPointSearchForm

from datapoints.mixins import PermissionRequiredMixin

class IndexView(generic.ListView):
    paginate_by = 10

    def get_queryset(self):
        return self.model.objects.order_by('-created_at')[:10]

    ###################
    ###################
    ###################
    ### DATA POINTS ###
    ###################
    ###################
    ###################

class DataPointIndexView(IndexView):

    model=DataPoint
    template_name = 'datapoints/index.html'
    context_object_name = 'top_datapoints'


class DashBoardView(IndexView):

    template_name = 'dashboard/index.html'
    context_object_name = 'user_dashboard'

    def get_queryset(self):
        cursor = connection.cursor()
        raw_sql = show_dashboard
        cursor.execute(raw_sql)
        rows = cursor.fetchall()

        return rows

class DataPointCreateView(PermissionRequiredMixin, generic.CreateView):

    model=DataPoint
    success_url="/datapoints"
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
    success_url="/datapoints"
    template_name='datapoints/update.html'
    form_class = DataPointForm
    permission_required = 'datapoints.change_datapoint'

    def form_valid(self, form):
    # this sets the changed_by field to the user who made the update
        obj = form.save(commit=False)
        obj.changed_by = self.request.user
        obj.save()
        return HttpResponseRedirect(self.success_url)

class DataPointDeleteView(PermissionRequiredMixin,generic.DeleteView):

    model=DataPoint
    success_url="/datapoints"
    template_name="datapoints/confirm_delete.html"
    permission_required = 'datapoints.add_datapoint'

    #########################
    ### REPORTING PERIODS ###
    #########################

class ReportingPeriodIndexView(IndexView):

    model=ReportingPeriod
    template_name = 'reporting_periods/index.html'
    context_object_name = 'top_reporting_periods'


class ReportingPeriodCreateView(PermissionRequiredMixin,generic.CreateView):

    model=ReportingPeriod
    success_url="/datapoints/reporting_periods"
    template_name='reporting_periods/create.html'

    ##################
    ##################
    ##################
    ### INDICATORS ###
    ##################
    ##################
    ##################

class IndicatorIndexView(IndexView):

    model=Indicator
    template_name = 'indicators/index.html'
    context_object_name = 'top_indicators'

class IndicatorCreateView(PermissionRequiredMixin,generic.CreateView):

    model=Indicator
    success_url="/datapoints/indicators
    "
    template_name='indicators/create.html'

class IndicatorUpdateView(PermissionRequiredMixin,generic.UpdateView):

    model=Indicator
    success_url="/datapoints/indicators"
    template_name='indicators/update.html'

class IndicatorDeleteView(PermissionRequiredMixin,generic.DeleteView):

    model=Indicator
    success_url="/datapoints/indicators"
    template_name="indicators/confirm_delete.html"

    #####################
    ### INDICATOR PCT ###
    #####################

class IndicatorPctIndexView(IndexView):

    model=IndicatorPct
    template_name = 'indicator_pct/index.html'
    context_object_name = 'top_indicator_pct'

class IndicatorPctCreateView(generic.CreateView):

    model=IndicatorPct
    success_url="/datapoints/indicators/indicator_pct"
    template_name='indicator_pct/create.html'

    ###############
    ###############
    ###############
    ### REGIONS ###
    ###############
    ###############
    ###############

class RegionIndexView(IndexView):

    model = Region
    template_name = 'regions/index.html'
    context_object_name = 'top_regions'

class RegionCreateView(PermissionRequiredMixin,generic.CreateView):

    model=Region
    success_url="/datapoints/regions/region_relationships/create"
    template_name='regions/create.html'

class RegionUpdateView(PermissionRequiredMixin,generic.UpdateView):

    model=Region
    success_url="/datapoints/regions"
    template_name='regions/update.html'

class RegionDeleteView(PermissionRequiredMixin,generic.DeleteView):

    model=Region
    success_url="/datapoints/regions"
    template_name="regions/confirm_delete.html"


    ############################
    ### REGION RELATIONSHIPS ###
    ############################

class RegionRelationshipIndexView(IndexView):
    model=RegionRelationship
    template_name = 'region_relationships/index.html'
    context_object_name = 'top_region_relationships'

class RegionRelationshipCreateView(PermissionRequiredMixin,generic.CreateView):

    model=RegionRelationship
    success_url="/datapoints/regions"
    template_name='region_relationships/create.html'

    ##################################
    ### REGION RELATIONSHIPS TYPES ###
    ##################################

class RegionRelagionshipTypeIndexView(IndexView):

    model=RegionRelationshipType
    template_name = 'region_relationships/type_index.html'
    context_object_name = 'top_region_relationship_types'

class RegionRelationshipTypeCreateView(PermissionRequiredMixin,
    generic.CreateView):

    model=RegionRelationshipType,
    success_url="/datapoints/regions"
    template_name='region_relationships/type_create.html'

    ##############################
    ##############################
    ##############################
    #### FUNCTION BASED VIEWS ####
    ##############################
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
      if request.POST['reporting_period'] != u'':
          kwargs.update({'reporting_period': request.POST['reporting_period']})

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
