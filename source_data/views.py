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

        return HttpResponseRedirect('/source_data/map_header/%s' % newdoc.id)

def map_header(request,document_id):

    file_columns = get_doc_file_cols(Document.objects.get(id=document_id).docfile)

    return render_to_response(
        'upload/map_header.html',
        {'file_columns': file_columns,'document_id':document_id},
        context_instance=RequestContext(request)
    )

def process_file(request,document_id):

    doc_mappings = request.GET

    for k,v in doc_mappings.iteritems():
        doc_detail_type = DocDetailType.objects.get(name=k)
        doc_detail, created = DocumentDetail.objects.get_or_create(
            doc_detail_type_id = doc_detail_type.id ,
            document_id = document_id,
            defaults = {
                'doc_detail_value':v
            }
        )

    dt = DocTransform(request.user.id, document_id)
    source_submissions = dt.process_file()
    mr = MasterRefresh(request.user.id, document_id)
    mr.refresh_doc_meta()
    mr.refresh_submission_details()

    return_url = '/datapoints/source-data/Nigeria/2015/06/viewraw/%s' % \
        document_id

    return HttpResponseRedirect(return_url)


def get_doc_file_cols(to_upload):

    for i,(line) in enumerate(to_upload):

        if i == 0:
            header_data = line.split('\r')[0]
            header = header_data.split(',')

    return header

def odk_review(request):

    odk_job_data = ODKForm.objects.all()

    return render_to_response('odk_review.html'
        ,{'odk_job_data': odk_job_data})
