import xlrd
import csv
import pandas
import hashlib
import pprint as pp

from django.shortcuts import render,render_to_response
from django.template import RequestContext
from django.db import IntegrityError
from django.contrib import messages
from django.views import generic
from django.core.urlresolvers import reverse, reverse_lazy
from django.http import HttpResponseRedirect, HttpResponse
from pandas.io.excel import read_excel
from itertools import chain

from datapoints.mixins import PermissionRequiredMixin
from source_data.forms import *
from source_data.models import *
from source_data.etl_tasks.transform_upload import DocTransform
from source_data.etl_tasks.refresh_master import MasterRefresh
from source_data.etl_tasks.transform_bulk_entry import bulk_data_to_sdps
from source_data.api import EtlTask

def data_entry(request):

    data_entry_form = DataEntryForm()

    if request.method == 'GET':


        return render_to_response(
            'data_entry/basic.html',
            {'data_entry_form': data_entry_form },
            RequestContext(request),
        )

    else:
        bulk_data = request.POST['bulk_data']
        campaign = request.POST['campaign']

        source_datapoints, not_parsed = bulk_data_to_sdps(bulk_data,campaign)

        to_review = source_datapoints

        return render_to_response(
            'data_entry/basic.html',
            {'to_review': to_review ,'data_entry_form': data_entry_form },
            RequestContext(request),
        )


def file_upload(request):

    accepted_file_formats = ['.csv','.xls','.xlsx']

    if request.method == 'GET':
        form = DocumentForm()

        return render_to_response(
            'upload/file_upload.html',
            {'form': form},
            context_instance=RequestContext(request)
        )


    elif request.method == 'POST':

        to_upload = request.FILES['docfile']
        # If the document is of an invalid format
        if not any(str(to_upload.name).endswith(ext) for ext in accepted_file_formats):
            msg = 'Please upload either .CSV, .XLS or .XLSX file format'
            messages.add_message(request, messages.INFO,msg)

        created_by = request.user
        newdoc = Document.objects.create(docfile=to_upload,created_by=created_by)

        return HttpResponseRedirect(reverse('source_data:pre_process_file',kwargs={'pk':newdoc.id}))  # encode like done below


def pre_process_file(request,pk):


    dt = DocTransform(pk)
    header_list  = dt.df.columns.values
    column_mapping = dt.get_essential_columns()

    return render_to_response(
        'upload/document_review.html',
        {'doc_data': column_mapping,'header_list':header_list},
        RequestContext(request),
    )



######### META MAPPING ##########


class CreateMap(PermissionRequiredMixin, generic.CreateView):

    template_name='map/map.html'
    success_url=reverse_lazy('datapoints:datapoint_index')
    # permission_required = 'datapoints.add_datapoint'

    def form_valid(self, form):
    # this inserts into the changed_by field with  the user who made the insert
        obj = form.save(commit=False)
        obj.mapped_by = self.request.user
        # obj.source_id = Source.objects.get(source_name='data entry').id
        obj.save()
        return HttpResponseRedirect(self.success_url)


class IndicatorMapCreateView(CreateMap):

    model=IndicatorMap
    form_class = IndicatorMapForm
    context_object_name = 'indicator_to_map'
    template_name = 'map/map.html'
    success_url=reverse_lazy('source_data:to_map')

    def get_initial(self):
        return { 'source_indicator': self.kwargs['pk'] }


class RegionMapCreateView(CreateMap):

    model=RegionMap
    form_class = RegionMapForm
    success_url=reverse_lazy('source_data:to_map')

    def get_initial(self):
        return { 'source_region': self.kwargs['pk'] }


class CampaignMapCreateView(CreateMap):

    model=CampaignMap
    form_class = CampaignMapForm
    success_url=reverse_lazy('source_data:to_map')

    def get_initial(self):
        return { 'source_campaign': self.kwargs['pk'] }


class ToMap(generic.ListView):

    model = SourceIndicator
    template_name = 'map/to_map.html'
    context_object_name = 'items'

    def get_queryset(self):

        si = SourceIndicator.objects.filter(indicatormap__isnull=True)
        cp = SourceCampaign.objects.filter(campaignmap__isnull=True)
        rg = SourceRegion.objects.filter(regionmap__isnull=True)

        for r in rg:
            print r.source

        return chain(si,cp,rg)


class ShowSourceIndicator(generic.DetailView):

    context_object_name = "source_indicator"
    template_name = 'map/source_indicator.html'
    model = SourceIndicator



def refresh_master(request):

    job_guid = hashlib.sha1(str(random.random())).hexdigest()

    t = EtlTask('refresh_master',job_guid)

    task_data = t.data

    print task_data

    return render_to_response('map/master_refresh.html',
    {'task_data': task_data})
