import hashlib
from itertools import chain
from pprint import pprint
import json

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib import messages
from django.views import generic
from django.core.urlresolvers import reverse, reverse_lazy
from django.http import HttpResponseRedirect,HttpResponse
from django.db.utils import IntegrityError
from pandas import DataFrame, notnull

from datapoints.mixins import PermissionRequiredMixin
from datapoints.models import DataPoint, Responsibility
from source_data.forms import *
from source_data.models import *
from source_data.etl_tasks.transform_upload import DocTransform,RegionTransform
from source_data.etl_tasks.refresh_master import MasterRefresh\
    ,create_source_meta_data
from source_data.api import EtlTask


### File Upload Below ###

def file_upload(request):

    source_id = Source.objects.get(source_name='datapoint_upload').id

    accepted_file_formats = ['.csv','.xls','.xlsx']

    if request.method == 'GET':
        form = DocumentForm()

        return render_to_response(
            'upload/file_upload.html',
            {'form': form},
            context_instance=RequestContext(request)
        )


    elif request.method == 'POST':

        try:
            to_upload = request.FILES['docfile']

        except KeyError:
            msg = 'Please add a file to upload'
            messages.add_message(request, messages.INFO,msg)

            return render_to_response(
                'upload/file_upload.html',
                context_instance=RequestContext(request)
            )

        # If the document is of an invalid format
        if not any(str(to_upload.name).endswith(ext) for ext in accepted_file_formats):
            msg = 'Please upload either .CSV, .XLS or .XLSX file format'
            messages.add_message(request, messages.INFO,msg)

            return render_to_response(
                'upload/file_upload.html',
                context_instance=RequestContext(request)
            )

        created_by = request.user
        newdoc = Document.objects.create(docfile=to_upload,\
            created_by=created_by,source_id=source_id)
        file_columns = get_doc_file_cols(to_upload)

        return render_to_response(
            'upload/map_header.html',
            {'file_columns': file_columns,'document_id':newdoc.id},
            context_instance=RequestContext(request)
        )

def get_doc_file_cols(to_upload):

    for i,(line) in enumerate(to_upload):

        if i == 0:
            header_data = line.split('\r')[0]
            header = header_data.split(',')

    return header

def map_header(request,document_id):

    column_mappings = {}
    column_mappings['campaign_col'] = request.GET['campaign_col']
    column_mappings['value_col'] = request.GET['value_col']
    column_mappings['region_code_col'] = request.GET['region_code_col']
    column_mappings['indicator_col'] = request.GET['indicator_col']

    dt = DocTransform(document_id,column_mappings)
    file_columns = [col for col in dt.df]

    return render_to_response(
        'upload/map_header.html',
        { 'file_columns':file_columns,
          'document_id':document_id },
        RequestContext(request))


def field_mapping(request,document_id):

    meta_breakdown = populate_document_metadata(document_id)

    return render_to_response(
        'upload/field_mapping.html',
        {'document_id': document_id }
        ,RequestContext(request))


def populate_document_metadata(document_id):

    meta_breakdown = []

    raw_qs = DocumentDetail.objects.raw('''
        SELECT * FROM fn_populate_doc_meta(%s)''',[document_id])

    inserted_ids = [x.id for x in raw_qs]

    return meta_breakdown


def pre_process_file(request,document_id):

    column_mappings = {}
    column_mappings['campaign_col'] = request.GET['campaign_col']
    column_mappings['value_col'] = request.GET['value_col']
    column_mappings['region_code_col'] = request.GET['region_code_col']
    column_mappings['indicator_col'] = request.GET['indicator_col']

    dt = DocTransform(document_id,column_mappings)

    try:
        sdps = dt.dp_df_to_source_datapoints()
    except IntegrityError:
        sdps = SourceDataPoint.objects.filter(
            document_id = document_id)

    populate_document_metadata(document_id)

    return HttpResponseRedirect(reverse('source_data:field_mapping'\
        , kwargs={'document_id': document_id}))


def refresh_master_no_indicator(request,document_id):

    mr = MasterRefresh(document_id = document_id, indicator_id = None,\
        user_id = request.user.id)

    mr.source_dps_to_dps()

    return HttpResponseRedirect(reverse('source_data:field_mapping'\
        , kwargs={'document_id': document_id}))


######### DOCUMENT RELATED VIEWS ##########

class DocumentIndex(generic.ListView):

    context_object_name = "documents"
    template_name = 'document_list.html'
    model = Document


def refresh_master(request):

    job_guid = hashlib.sha1(str(random.random())).hexdigest()

    t = EtlTask('refresh_master',job_guid)

    task_data = t.data

    return render_to_response('map/master_refresh.html'
        ,{'task_data': task_data})


def odk_review(request):

    task_data = {'hello':'goodbye'}

    odk_job_data = EtlJob.objects.filter(task_name__contains='odk')[:50]

    return render_to_response('odk_review.html'
        ,{'odk_job_data': odk_job_data})
