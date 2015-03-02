import hashlib
from django.utils import simplejson
from itertools import chain
from pprint import pprint

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib import messages
from django.views import generic
from django.core.urlresolvers import reverse, reverse_lazy
from django.http import HttpResponseRedirect,HttpResponse
from django.db.utils import IntegrityError

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

    accepted_file_formats = ['.csv','.xls','.xlsx']

    if request.method == 'GET':
        form = DocumentForm()

        return render_to_response(
            'upload/file_upload.html',
            {'form': form},
            context_instance=RequestContext(request)
        )


    elif request.method == 'POST':

        file_type = request.POST['file_type']

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
        newdoc = Document.objects.create(docfile=to_upload,created_by=created_by)

        return HttpResponseRedirect(reverse('source_data:map_header',\
            kwargs={'document_id':newdoc.id,'file_type':file_type}))

def map_header(request,document_id,file_type):

    if file_type == 'Region':

        return HttpResponseRedirect(reverse('source_data:pre_process_file',\
            kwargs={'document_id':document_id,'file_type':file_type}))

    else:
        dt = DocTransform(document_id,file_type,{})
        file_columns = [col for col in dt.df]

        return render_to_response(
            'upload/map_header.html',
            { 'file_columns':file_columns,
              'document_id':document_id,
              'file_type':file_type },
            RequestContext(request))


def document_review(request,document_id):

    sdp_ids = SourceDataPoint.objects.filter(document_id = document_id)\
        .values_list('id',flat=True)

    meta_breakdown = populate_document_metadata(document_id)

    doc_obj = Document.objects.get(id = document_id)
    sdp_count, dp_count = doc_obj.source_datapoint_count\
        , doc_obj.master_datapoint_count

    return render_to_response(
        'upload/document_review.html',
        {'source_indicator_breakdown': meta_breakdown['indicator_breakdown'],
        'source_region_breakdown': meta_breakdown['region_breakdown'],
        'source_campaign_breakdown': meta_breakdown['campaign_breakdown'],
        'document_id': document_id }
        ,RequestContext(request))

def populate_document_metadata(document_id):

    meta_breakdown = {}
    indicator_breakdown,region_breakdown,campaign_breakdown = [],[],[]

    si_raw = SourceIndicator.objects.raw(
    '''
    DROP TABLE IF EXISTS _indicator_doc_meta;
    CREATE TEMP TABLE _indicator_doc_meta AS

    SELECT DISTINCT
          indicator_string
        , document_id
        , sd.indicator_string || '-' || sd.document_id as source_guid
        , COUNT(1) as source_datapoint_count
    FROM source_datapoint sd
    WHERE document_id = %s
    GROUP by sd.document_id, sd.indicator_string ;

    INSERT INTO source_indicator
    (indicator_string, document_id,source_guid)

    SELECT indicator_string, document_id,source_guid
    FROM _indicator_doc_meta idm
    WHERE NOT EXISTS (
    	SELECT 1 FROM source_indicator si
    	WHERE idm.indicator_string = si.indicator_string
    );

    --

    SELECT
         si.id
        ,si.indicator_string
        ,COALESCE(im.master_indicator_id,-1) as master_indicator_id
        ,idm.source_datapoint_count
        ,x.indicator_datapoint_count
    FROM _indicator_doc_meta idm
    INNER JOIN source_indicator si
        ON idm.indicator_string = si.indicator_string
    LEFT JOIN indicator_map im
        ON si.id = im.source_indicator_id
    LEFT JOIN (
        SELECT
            d.indicator_id
            ,count(*) AS indicator_datapoint_count
        FROM source_datapoint sd
        INNER JOIN datapoint d
        ON sd.id = d.source_datapoint_id
        WHERE document_id = %s
        GROUP BY d.indicator_id
    )x
    ON im.master_indicator_id = x.indicator_id
    ORDER BY 3
    ''',[document_id,document_id])

    for row in si_raw:
        row_dict = {
            'source_indicator_id':row.id,
            'indicator_string':row.indicator_string,
            'master_indicator_id':row.master_indicator_id,
            'source_datapoint_count':row.source_datapoint_count,
            'indicator_datapoint_count':row.indicator_datapoint_count
        }

        indicator_breakdown.append(row_dict)

    sc_raw = SourceCampaign.objects.raw(
        '''
        DROP TABLE IF EXISTS _campaign_doc_meta;
        CREATE TEMP TABLE _campaign_doc_meta AS

        SELECT DISTINCT
              campaign_string
            , document_id
            , sd.campaign_string || '-' || sd.document_id as source_guid
        FROM source_datapoint sd
        WHERE document_id = %s;

        INSERT INTO source_campaign
        (campaign_string, document_id,source_guid)

        SELECT campaign_string, document_id,source_guid
        FROM _campaign_doc_meta cdm
        WHERE NOT EXISTS (
        	SELECT 1 FROM source_campaign sc
        	WHERE cdm.campaign_string = sc.campaign_string
        );

        --

        SELECT
             sc.id
            ,sc.campaign_string
            ,COALESCE(cm.master_campaign_id,-1) as master_campaign_id
        FROM _campaign_doc_meta cdm
        INNER JOIN source_campaign sc
            ON cdm.campaign_string = sc.campaign_string
        LEFT JOIN campaign_map cm
            ON sc.id = cm.source_campaign_id
        ORDER BY 3
        ''',[document_id])

    for row in sc_raw:
        row_dict = {
            'source_campaign_id':row.id,
            'campaign_string':row.campaign_string,
            'master_campaign_id':row.master_campaign_id
        }

        campaign_breakdown.append(row_dict)

    sr_raw = SourceCampaign.objects.raw(
        '''
        DROP TABLE IF EXISTS _region_doc_meta;
        CREATE TEMP TABLE _region_doc_meta AS

        SELECT DISTINCT
              region_code
            , document_id
            , sd.region_code || '-' || sd.document_id as source_guid
            , CAST(0 AS BOOLEAN) as is_high_risk
        FROM source_datapoint sd
        WHERE document_id = %s;

        INSERT INTO source_region
        (region_code, document_id,source_guid,is_high_risk)

        SELECT region_code, document_id,source_guid,is_high_risk
        FROM _region_doc_meta rdm
        WHERE NOT EXISTS (
        	SELECT 1 FROM source_region sr
        	WHERE rdm.region_code = sr.region_code
        );

        --

        SELECT
             sr.id
            ,sr.region_code
            ,COALESCE(rm.master_region_id,-1) as master_region_id
        FROM _region_doc_meta rdm
        INNER JOIN source_region sr
            ON rdm.region_code = sr.region_code
        LEFT JOIN region_map rm
            ON sr.id = rm.source_region_id
        ORDER BY 3
        ''',[document_id])

    for row in sr_raw:
        row_dict = {
            'source_region_id':row.id,
            'region_string':row.region_code,
            'master_region_id':row.master_region_id
        }

        region_breakdown.append(row_dict)

    meta_breakdown['indicator_breakdown'] = indicator_breakdown
    meta_breakdown['region_breakdown'] = region_breakdown
    meta_breakdown['campaign_breakdown'] = campaign_breakdown

    return meta_breakdown

def sync_source_datapoints(request,document_id,master_indicator_id):

    mr = MasterRefresh(request.user.id,document_id,master_indicator_id)

    mr.source_dps_to_dps()
    mr.sync_regions()

    return HttpResponseRedirect(reverse('source_data:document_review'\
        , kwargs={'document_id': document_id}))


def pre_process_file(request,document_id,file_type):

    if file_type == 'Datapoint':

        column_mappings = {}
        column_mappings['campaign_col'] = request.GET['campaign_col']
        column_mappings['value_col'] = request.GET['value_col']
        column_mappings['region_code_col'] = request.GET['region_code_col']
        column_mappings['indicator_col'] = request.GET['indicator_col']

        dt = DocTransform(document_id,file_type,column_mappings)

        try:
            sdps = dt.dp_df_to_source_datapoints()
        except IntegrityError:
            sdps = SourceDataPoint.objects.filter(
                document_id = document_id)

        populate_document_metadata(document_id)

        return HttpResponseRedirect(reverse('source_data:document_review'\
            , kwargs={'document_id': document_id}))

    elif file_type == 'Region':

        rt = RegionTransform(document_id,file_type,{})
        err,valid_df = rt.validate()
        src_regions = rt.insert_source_regions(valid_df)

        to_map = []
        to_map_raw = SourceRegion.objects.raw('''
            SELECT
                sr.id
                ,sr.id as source_object_id
                ,sr.region_string as source_string
                ,COALESCE(rm.master_region_id,-1) as master_object_id
            FROM source_region sr
            LEFT JOIN region_map rm
            ON sr.id = rm.source_region_id
            WHERE sr.document_id = %s''',[document_id]
        )

        for row in to_map_raw:
            row_dict = {}
            row_dict['source_string'] = row.source_string
            row_dict['source_object_id'] = row.source_object_id
            row_dict['master_object_id'] = row.master_object_id
            row_dict['model_type'] = 'region'


        return render_to_response(
            'data_entry/meta_map.html',
            {'document_id': document_id, 'to_map':to_map},
            RequestContext(request),
        )

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


######### META MAPPING ##########


class CreateMap(PermissionRequiredMixin, generic.CreateView):

    template_name='map/map.html'
    success_url=reverse_lazy('source_data:document_index')
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

    def get_initial(self):
        return { 'source_indicator': self.kwargs['pk'] }


class RegionMapCreateView(CreateMap):

    model=RegionMap
    form_class = RegionMapForm


    def get_initial(self):
        return { 'source_region': self.kwargs['pk'] }


class CampaignMapCreateView(CreateMap):

    model=CampaignMap
    form_class = CampaignMapForm

    def get_initial(self):
        return { 'source_campaign': self.kwargs['pk'] }


class ShowSourceIndicator(generic.DetailView):

    context_object_name = "source_indicator"
    template_name = 'map/source_indicator.html'
    model = SourceIndicator


class EtlJobIndex(generic.ListView):

    context_object_name = "etl_jobs"
    template_name = 'etl_jobs.html'
    model = EtlJob
    paginate_by = 25


def un_map(request,map_id,db_model,document_id):

    if db_model == 'Region':

        RegionMap.objects.get(id=map_id).delete()

    elif db_model == 'Indicator':

        IndicatorMap.objects.get(id=map_id).delete()

    elif db_model == 'Campaign':

        CampaignMap.objects.get(id=map_id).delete()


    return HttpResponseRedirect(reverse('source_data:refresh_master_by_document_id'\
        ,kwargs={'document_id':document_id}))


def refresh_master(request):

    job_guid = hashlib.sha1(str(random.random())).hexdigest()

    t = EtlTask('refresh_master',job_guid)

    task_data = t.data

    print task_data

    return render_to_response('map/master_refresh.html'
        ,{'task_data': task_data})
