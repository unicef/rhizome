import hashlib
from django.utils import simplejson
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


def mark_doc_as_processed(request,document_id):

    doc = Document.objects.get(id=document_id)
    doc.is_processed = True
    doc.save()

    return HttpResponseRedirect(reverse('source_data:document_index'))

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


def document_review(request,document_id):

    meta_breakdown = populate_document_metadata(document_id)
    mb_df = DataFrame(meta_breakdown)
    no_ix_df = mb_df.reset_index(drop=True)

    print mb_df

    ind_dict = no_ix_df[no_ix_df['db_model'] == 'source_indicator']\
        .transpose().to_dict()
    ind_breakdown =  [v for k,v in ind_dict.iteritems()]

    ##
    camp_dict = no_ix_df[no_ix_df['db_model'] == 'source_campaign']\
        .transpose().to_dict()
    camp_breakdown =  [v for k,v in camp_dict.iteritems()]

    ##
    region_dict = no_ix_df[no_ix_df['db_model'] == 'source_region']\
        .transpose().to_dict()
    region_breakdown =  [v for k,v in region_dict.iteritems()]

    return render_to_response(
        'upload/document_review.html',
        {'source_indicator_breakdown': ind_breakdown,
        'source_region_breakdown': region_breakdown,
        'source_campaign_breakdown': camp_breakdown,
        'document_id': document_id }
        ,RequestContext(request))

def populate_document_metadata(document_id):

    meta_breakdown = []

    raw_qs = Document.objects.raw('''

        SELECT * FROM fn_populate_doc_meta(%s)

        ''',[document_id])

    for row in raw_qs:
        row_dict = {
            'document_id' : row.id,
            'db_model':row.db_model,
            'source_object_id':row.source_object_id,
            'source_string':row.source_string,
            'master_object_id':row.master_object_id,
            'source_object_count':row.source_object_cnt,
            'master_object_count':row.master_object_cnt,
        }

        meta_breakdown.append(row_dict)

    return meta_breakdown

def sync_source_datapoints(request,document_id,master_id):

    mr = MasterRefresh(request.user.id,document_id,master_id)

    mr.source_dps_to_dps()
    mr.sync_regions()

    return HttpResponseRedirect(reverse('source_data:document_review'\
        , kwargs={'document_id': document_id}))


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

    return HttpResponseRedirect(reverse('source_data:document_review'\
        , kwargs={'document_id': document_id}))


def refresh_master_no_indicator(request,document_id):

    mr = MasterRefresh(document_id = document_id, indicator_id = None, user_id = request.user.id)

    mr.source_dps_to_dps()

    return HttpResponseRedirect(reverse('source_data:document_review'\
        , kwargs={'document_id': document_id}))


######### DOCUMENT RELATED VIEWS ##########

class DocumentIndex(generic.ListView):

    context_object_name = "documents"
    template_name = 'document_list.html'
    model = Document


class EtlJobIndex(generic.ListView):

    context_object_name = "etl_jobs"
    template_name = 'etl_jobs.html'
    model = EtlJob
    paginate_by = 25


def refresh_master(request):

    job_guid = hashlib.sha1(str(random.random())).hexdigest()

    t = EtlTask('refresh_master',job_guid)

    task_data = t.data

    return render_to_response('map/master_refresh.html'
        ,{'task_data': task_data})

def api_document_review(request):

    try:
        document_id = request.GET['document_id']
    except KeyError:
        return HttpResponse(json.dumps({'error':'document_id is a required parameter'})\
            , content_type="application/json")


    meta_breakdown = []

    raw_qs = Document.objects.raw('''\
        SELECT * FROM fn_populate_doc_meta(%s)''',[document_id])

    for row in raw_qs:
        row_dict = {
            'db_model':row.db_model,
            'source_object_id':row.source_object_id,
            'source_string':row.source_string,
            'master_object_id':row.master_object_id,
        }

        meta_breakdown.append(row_dict)

    mb_df = DataFrame(meta_breakdown)
    df_no_nan = mb_df.where((notnull(mb_df)), None)
    no_ix_df = df_no_nan.reset_index(drop=True)

    ind_dict = no_ix_df[no_ix_df['db_model'] == 'source_indicator']\
        .transpose().to_dict()
    indicator_breakdown =  [v for k,v in ind_dict.iteritems()]

    ##
    camp_dict = no_ix_df[no_ix_df['db_model'] == 'source_campaign']\
        .transpose().to_dict()
    camp_breakdown =  [v for k,v in camp_dict.iteritems()]

    ##
    region_dict = no_ix_df[no_ix_df['db_model'] == 'source_region']\
        .transpose().to_dict()
    region_breakdown =  [v for k,v in region_dict.iteritems()]

    response_objects = { \
        'regions': region_breakdown,
        'campaigns': camp_breakdown,
        'indicators': indicator_breakdown,
        }

    response_data = {'objects':response_objects }

    return HttpResponse(json.dumps(response_data)\
        , content_type="application/json")


def api_map_meta(request):

    objects, error, meta = None, None, {}
    required_params = {'object_type':None,'source_object_id':None,\
        'master_object_id':None}

    map_model_lookup  = {
        'indicator':IndicatorMap,
        'region':RegionMap,
        'campaign':CampaignMap
        }

    ## POPULATE THE META_DICT WITH THE REQUIRED PARAMS AND THEIR VALUES ##
    for param in required_params:

        try:
            # FIND THE PARAMETER FROM THE REQUEST
            meta[param] = request.POST[param].replace('[u','').replace(']','')
        except KeyError:  ## IF PARAM IS MISSING ##
            error = '%s is a required parameter' % param
            response_data = {'objects':objects,'error':error, 'meta':meta}

            return HttpResponse(json.dumps(response_data)\
                , content_type="application/json")

    meta['user_id'] = request.user.id

    ## LOOK UP THE OBJECT AND CREATE OR UPDATE THE MAPPING TABLE $$
    map_object = map_model_lookup[meta['object_type']]

    ## CREATE OR UPDATE THE MAP ##
    error, map_row_id = upsert_mapping(meta,map_object)

    ## RETURN DATA TO API ##
    objects = {'object_id': map_row_id}
    response_data = {'error':error,'objects':objects, 'meta':meta }

    return HttpResponse(json.dumps(response_data)\
        , content_type="application/json")


def upsert_mapping(meta,map_object):

    request_source_id, request_master_id, request_user_id = \
        int(meta['source_object_id']),int(meta['master_object_id']),\
        int(meta['user_id'])

    try:
        db_obj, created = map_object.objects.get_or_create(
            source_object_id = request_source_id,
            defaults = {
                'master_id':request_master_id,
                'mapped_by_id':request_user_id
            })

        if not created:
            db_obj.master_id = request_master_id
            db_obj.mapped_by_id = request_user_id
            db_obj.save()


    except Exception as err:
        return str(err), None


    return None, db_obj.id
