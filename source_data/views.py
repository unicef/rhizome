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
from pandas import DataFrame

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

    raw_qs = Document.objects.raw(
    '''
    -----					-----------
    -- BUILD TEMP TABLE TO WORK WITH --
    -----					-----------

    DROP TABLE IF EXISTS _doc_meta;
    CREATE TABLE _doc_meta AS

    SELECT
    	document_id
    	,indicator_string
    	,campaign_string
    	,region_code
    FROM source_datapoint
    WHERE document_id = 974;

    DROP TABLE IF EXISTS _doc_meta_cnt;
    CREATE TABLE _doc_meta_cnt AS

    SELECT
    	*
    	,CAST(NULL AS INT) AS source_object_id
    	,CAST(-1 AS INT) as master_object_id
    FROM (
    	SELECT
    		'source_indicator' as db_model
    		,indicator_string as source_string
    		,COUNT(1) AS cnt
    	FROM _doc_meta
    	GROUP BY indicator_string

    	UNION ALL

    	SELECT
    		'source_campaign' as db_model
    		,campaign_string
    		,COUNT(1) AS c
    	FROM _doc_meta
    	GROUP BY campaign_string

    	UNION ALL

    	SELECT
    		'source_region' as db_model
    		,region_code
    		,COUNT(1) AS c
    	FROM _doc_meta
    	GROUP BY region_code
    )x
    INNER JOIN (
    	SELECT document_id
    	FROM _doc_meta LIMIT 1
    )y
    ON 1=1;


    -----					-----
    -- insert source meta data --
    -----					------

    -- INDICATORS --

    INSERT INTO source_indicator
    (indicator_string, document_id,source_guid)

    SELECT dmc.source_string, dmc.document_id, dmc.source_string || '-' || dmc.document_id
    FROM _doc_meta_cnt dmc
    WHERE db_model = 'source_indicator'
    AND NOT EXISTS (
    	SELECT 1 FROM source_indicator si
    	WHERE dmc.db_model = 'source_indicator'
    	AND dmc.source_string = si.indicator_string
    );

    UPDATE _doc_meta_cnt dmc
    SET
    	source_object_id = si.id
    FROM source_indicator si
    WHERE dmc.db_model = 'source_indicator'
    AND dmc.source_string = si.indicator_string;

    -- MASTER REGION ID --
    UPDATE _doc_meta_cnt dmc
    SET
    	master_object_id = im.master_indicator_id
    FROM indicator_map im
    WHERE dmc.db_model = 'source_indicator'
    AND dmc.source_object_id = im.source_indicator_id;

    -- REGIONS --

    INSERT INTO source_region
    (region_code,document_id,source_guid)

    SELECT dmc.source_string, dmc.document_id, dmc.source_string || '-' || dmc.document_id
    FROM _doc_meta_cnt dmc
    WHERE db_model = 'source_region'
    AND NOT EXISTS (
    	SELECT 1 FROM source_region sr
    	WHERE dmc.db_model = 'source_region'
    	AND dmc.source_string = sr.region_code
    );

    UPDATE _doc_meta_cnt dmc
    SET
    	source_object_id = sr.id
    FROM source_region sr
    WHERE dmc.db_model = 'source_region'
    AND dmc.source_string = sr.region_code;

    UPDATE _doc_meta_cnt dmc
    SET
    	master_object_id = rm.master_region_id
    FROM region_map rm
    WHERE dmc.db_model = 'source_region'
    AND dmc.source_object_id = rm.source_region_id;

    -- CAMPAIGNS --

    INSERT INTO source_campaign
    (campaign_string,document_id,source_guid)

    SELECT dmc.source_string, dmc.document_id, dmc.source_string || '-' || dmc.document_id
    FROM _doc_meta_cnt dmc
    WHERE db_model = 'source_campaign'
    AND NOT EXISTS (
    	SELECT 1 FROM source_campaign sc
    	WHERE dmc.db_model = 'source_campaign'
    	AND dmc.source_string = sc.campaign_string
    );

    -- SOURCE CAMPAIGN ID --
    UPDATE _doc_meta_cnt dmc
    SET
    	source_object_id = sc.id
    FROM source_campaign sc
    WHERE dmc.db_model = 'source_campaign'
    AND dmc.source_string = sc.campaign_string;

    -- MASTER CAMPAIGN ID --
    UPDATE _doc_meta_cnt dmc
    SET
    	master_object_id = cm.master_campaign_id
    FROM campaign_map cm
    WHERE dmc.db_model = 'source_campaign'
    AND dmc.source_object_id = cm.source_campaign_id;

    --- RETURN TO RAW QUERYSET -----

    SELECT
    	document_id as id
    	,db_model
    	,source_string
    	,source_object_id
    	,master_object_id
    	,cnt
    FROM _doc_meta_cnt
    ORDER BY db_model;''',[document_id,document_id])

    for row in raw_qs:
        row_dict = {
            'db_model':row.db_model,
            'source_object_id':row.source_object_id,
            'source_string':row.source_string,
            'master_object_id':row.master_object_id,
            'source_datapoint_count':row.cnt,
        }

        meta_breakdown.append(row_dict)

    return meta_breakdown

def sync_source_datapoints(request,document_id,master_indicator_id):

    mr = MasterRefresh(request.user.id,document_id,master_indicator_id)

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

    # return render_to_response(
    #     'data_entry/meta_map.html',
    #     {'document_id': document_id, 'to_map':to_map},
    #     RequestContext(request),
    # )

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
