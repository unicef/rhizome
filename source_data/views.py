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
from source_data.etl_tasks.transform_upload import DocTransform
from source_data.etl_tasks.refresh_master import MasterRefresh
from source_data.api import EtlTask

### File Upload Below ###

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

        created_by = request.user
        to_upload = request.FILES['docfile']
        newdoc = Document.objects.create(docfile=to_upload,created_by=created_by)

        dt = DocTransform(newdoc.id)
        sdps = dt.dp_df_to_source_datapoints()

        return HttpResponseRedirect('/doc_review/overview/%s' % newdoc.id)

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

    dt = DocTransform(document_id)
    sdps = dt.dp_df_to_source_datapoints()

    populate_document_metadata(document_id)

    return HttpResponseRedirect(reverse('doc_review'\
        , kwargs={'document_id': document_id}))


######### DOCUMENT RELATED VIEWS ##########

class DocumentIndex(generic.ListView):

    context_object_name = "documents"
    template_name = 'document_list.html'
    model = Document


def refresh_master(request,document_id):

    mr = MasterRefresh(request.user.id, document_id)
    mr.main()

    return HttpResponseRedirect('/doc_review/overview/%s' % document_id)


def odk_review(request):

    odk_job_data = ODKForm.objects.all()

    return render_to_response('odk_review.html'
        ,{'odk_job_data': odk_job_data})
