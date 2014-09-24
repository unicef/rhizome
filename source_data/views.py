import xlrd
import csv
import pandas
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
from source_data.etl_tasks.pre_process_upload import PreIngest
from source_data.etl_tasks.transform_upload import DocIngest


def file_upload(request):
    # Handle file upload
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = Document(docfile = request.FILES['docfile'])
            newdoc.created_by = request.user
            newdoc.save()
            document_id = newdoc.id

            file_path = newdoc.docfile.url

            if file_path.endswith('xls') or file_path.endswith('xlsx'):

                ## FIND MAPPINGS ##
                p = PreIngest(file_path,newdoc.id)
                # p.df , p.mappings

                ## MOVE XLS INTO DATAPOINTS TABLE ##
                current_user_id = request.user.id
                d = DocIngest(document_id,p.mappings,p.df,current_user_id)
                # process_sheet_df(df,document_id,mappings)

                return document_review(request,newdoc.id,p.mappings)

            # if file is csv...

            else:
                messages.add_message(request, messages.INFO, 'Please\
                    upload either .CSV, .XLS or .XLSX file format')

    else:
        form = DocumentForm()

    return render_to_response(
        'upload/file_upload.html',
        {'form': form},
        context_instance=RequestContext(request)
    )



def document_review(request,document_id,mappings):

    to_map_message = []

    to_map_ind_count = SourceIndicator.objects.count() - IndicatorMap.objects.count()
    to_map_reg_count = SourceRegion.objects.count() - RegionMap.objects.count()
    to_map_cam_count = SourceCampaign.objects.count() - CampaignMap.objects.count()

    r =  {'to_map_count': to_map_ind_count, 'model':'indicator'}
    r2 = {'to_map_count': to_map_reg_count, 'model':'region'}
    r3 = {'to_map_count': to_map_cam_count, 'model':'campaign'}

    to_map_message.append(r)
    to_map_message.append(r2)
    to_map_message.append(r3)


    return render_to_response(
        'upload/document_review.html',
        {'doc_data': to_map_message},
        context_instance=RequestContext(request),
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
        return { 'source_campaign': self.kwargs['pk'] }


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

        return chain(si,cp,rg)



class ShowSourceIndicator(generic.DetailView):

    context_object_name = "source_indicator"
    template_name = 'map/source_indicator.html'
    model = SourceIndicator
