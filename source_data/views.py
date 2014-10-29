import xlrd
import csv
import pandas
import hashlib
import pprint as pp
from itertools import chain


from django.shortcuts import render,render_to_response
from django.template import RequestContext
from django.db import IntegrityError, connection
from django.contrib import messages
from django.views import generic
from django.core.urlresolvers import reverse, reverse_lazy
from django.http import HttpResponseRedirect, HttpResponse
from pandas.io.excel import read_excel

from datapoints.mixins import PermissionRequiredMixin
from datapoints.models import DataPoint, Responsibility
from source_data.forms import *
from source_data.models import *
from source_data.etl_tasks.transform_upload import DocTransform
from source_data.etl_tasks.refresh_master import MasterRefresh
from source_data.etl_tasks.transform_bulk_entry import bulk_data_to_sdps
from source_data.api import EtlTask


def user_portal(request,campaign_id=None):

    if campaign_id is None:
        campaign_id = Campaign.objects.all().order_by('-start_date')[0].id

    raw_sql = '''select * from responsibility r
            where user_id = %s
            and not exists
            (
            	select 1 from datapoint d
            	where campaign_id = %s
            	and r.indicator_id = d.indicator_id
            	and r.region_id = d.region_id
                order by r.indicator_id
            )'''

    to_do = Responsibility.objects.raw(raw_sql % (request.user.id,campaign_id))
    

    docs = Document.objects.filter(created_by=request.user.id,is_processed=False)

    return render_to_response(
        'data_entry/user_portal.html',
        {'docs':docs,'to_do':to_do},
        RequestContext(request),
    )


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

        document = Document.objects.create(
            doc_text =bulk_data,
            created_by = request.user,
            )

        source_datapoints, not_parsed = bulk_data_to_sdps(
            bulk_data = bulk_data,
            campaign_string = request.POST['campaign'],
            delimiter = request.POST['delimiter'],
            document_id = document.id)

        return HttpResponseRedirect(reverse('source_data:review_sdps_by_document'\
                ,kwargs={'document_id':document.id}))


def review_sdps_by_document(request,document_id):

    source_datapoints = SourceDataPoint.objects.filter(document_id=document_id)

    return render_to_response(
        'upload/document_review.html',
        {'to_review': source_datapoints,'document_id': document_id},
        RequestContext(request),
    )


def refresh_master_by_document_id(request,document_id):

    source_datapoints = SourceDataPoint.objects.filter(document_id=document_id)

    m = MasterRefresh(source_datapoints,user_id = request.user.id,document_id=document_id)
    m.main()

    si = SourceIndicator.objects.filter(indicatormap__isnull=True,document_id=document_id)
    cp = SourceCampaign.objects.filter(campaignmap__isnull=True,document_id=document_id)
    rg = SourceRegion.objects.filter(regionmap__isnull=True,document_id=document_id)

    to_map = chain(si,cp,rg)

    doc_datapoints = DataPoint.objects.filter(source_datapoint_id__in=
        SourceDataPoint.objects.filter(document_id=document_id))

    return render_to_response(
        'data_entry/final_review.html',
        {'datapoints': doc_datapoints, 'document_id': document_id, 'to_map':to_map},
        RequestContext(request),
    )

def mark_doc_as_processed(request,document_id):

    doc = Document.objects.get(id=document_id)
    doc.is_processed = True
    doc.save()

    return HttpResponseRedirect(reverse('source_data:user_portal'))  # encode like done below




### Bulk Upload Stuff Above ###

            ####

### File Upload Stuff Below ###



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
    # success_url=reverse_lazy('source_data:to_map')

    def get_initial(self):
        return { 'source_indicator': self.kwargs['pk'] }


class RegionMapCreateView(CreateMap):

    model=RegionMap
    form_class = RegionMapForm
    # success_url=reverse_lazy('source_data:to_map')

    def get_initial(self):
        return { 'source_region': self.kwargs['pk'] }


class CampaignMapCreateView(CreateMap):

    model=CampaignMap
    form_class = CampaignMapForm
    # success_url=reverse_lazy('source_data:to_map')

    def get_initial(self):
        return { 'source_campaign': self.kwargs['pk'] }



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
