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


def user_portal(request):

    # pRse the campaign param from url.. if none, default to latest
    try:
        campaign_id = request.GET['campaign_id']
    except KeyError:
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
    campaigns = Campaign.objects.all()

    return render_to_response(
        'data_entry/user_portal.html',
        {'docs':docs,'to_do':to_do,'campaigns':campaigns,'campaign_id':campaign_id},
        RequestContext(request),
    )


def mark_doc_as_processed(request,document_id):

    doc = Document.objects.get(id=document_id)
    doc.is_processed = True
    doc.save()

    return HttpResponseRedirect(reverse('source_data:user_portal'))  # encode like done below


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

def populate_document_meta(document_id):

    source_indicator_breakdown = []

    doc_meta_limit_1 = DocumentMeta.objects.raw('''
        SELECT id FROM document_meta WHERE document_id = %s LIMIT 1'''\
        ,[document_id])

    has_meta = sum(1 for dm in doc_meta_limit_1)

    if has_meta == 0:

        create_source_meta_data(document_id)

        doc_meta_raw = DocumentMeta.objects.raw('''

        DROP TABLE IF EXISTS _tmp_meta_for_doc;
        CREATE TEMP TABLE _tmp_meta_for_doc AS

        SELECT * FROM source_datapoint where document_id = %s;

        INSERT INTO document_meta
        (document_id, source_string, model_type, source_object_id, master_object_id,source_datapoint_count)

        SELECT
        	sd.document_id
        	,si.indicator_string
        	,'indicator'
        	,si.id as source_indicator_id
        	,COALESCE(im.master_indicator_id,-1)
        	,COUNT(*) AS C
        FROM _tmp_meta_for_doc sd
        INNER JOIN source_indicator si
        	ON sd.indicator_string = si.indicator_string
        LEFT JOIN indicator_map im
        	ON si.id = im.source_indicator_id
        LEFT JOIN datapoint d
        	ON im.master_indicator_id = d.indicator_id
        	AND sd.id = d.source_datapoint_id
        GROUP BY sd.document_id, si.indicator_string, si.id, im.master_indicator_id

        UNION ALL

        SELECT DISTINCT
        	sd.document_id
        	,sr.region_code
        	,'region'
        	,sr.id as source_region_id
        	,COALESCE(rm.master_region_id,-1)
        	,0
        FROM _tmp_meta_for_doc sd
        INNER JOIN source_region sr
        	ON sd.region_code = sr.region_code
        LEFT JOIN region_map rm
        	ON sr.id = rm.source_region_id
        LEFT JOIN datapoint d
        	ON rm.master_region_id = d.region_id
        	AND sd.id = d.source_datapoint_id

        UNION ALL

        SELECT DISTINCT
        	sd.document_id
        	,sc.campaign_string
        	,'campaign'
        	,sc.id as source_campaign_id
        	,COALESCE(cm.master_campaign_id,-1)
        	,0
        FROM _tmp_meta_for_doc sd
        INNER JOIN source_campaign sc
        	ON sd.campaign_string = sc.campaign_string
        LEFT JOIN campaign_map cm
        	ON sc.id = cm.source_campaign_id
        LEFT JOIN datapoint d
        	ON cm.master_campaign_id = d.campaign_id
        	AND sd.id = d.source_datapoint_id;

        SELECT * FROM document_meta
        WHERE document_id = %s
        ORDER BY master_object_id desc;''', [document_id,document_id])

    else:

        doc_meta_raw = DocumentMeta.objects.raw('''

        UPDATE document_meta
        SET master_object_id = im.master_indicator_id
        FROM indicator_map im
        WHERE model_type = 'indicator'
        AND source_object_id = im.source_indicator_id
        AND document_id = %s;

        UPDATE document_meta
        SET master_object_id = rm.master_region_id
        FROM region_map rm
        WHERE model_type = 'region'
        AND source_object_id = rm.source_region_id
        AND document_id = %s;

        UPDATE document_meta
        SET master_object_id = cm.master_campaign_id
        FROM campaign_map cm
        WHERE model_type = 'campaign'
        AND source_object_id = cm.source_campaign_id
        AND document_id = %s;

        SELECT * FROM document_meta
        WHERE document_id = %s
        ORDER BY master_object_id desc;''', [document_id,document_id,\
            document_id,document_id])

    for row in doc_meta_raw:

        if row.model_type == 'indicator':

            ind_dict = {}
            ind_dict['indicator_string'] = row.source_string
            ind_dict['master_indicator_id'] = row.master_object_id
            ind_dict['source_indicator_id'] = row.source_object_id
            ind_dict['source_datapoint_count'] = row.source_datapoint_count

            source_indicator_breakdown.append(ind_dict)

    return source_indicator_breakdown

def document_review(request,document_id):

    sdp_ids = SourceDataPoint.objects.filter(document_id = document_id)\
        .values_list('id',flat=True)

    m = MasterRefresh(sdp_ids,user_id=request.user.id\
        ,document_id=document_id,indicator_id=None)

    source_indicator_breakdown = populate_document_meta(document_id)

    return render_to_response(
        'upload/document_review.html',
        {'to_review': source_indicator_breakdown,'document_id': document_id},
        RequestContext(request),
    )

def sync_source_datapoints(request,document_id,master_indicator_id):

    mr = MasterRefresh()

    pass


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

        return HttpResponseRedirect(reverse('source_data:document_review'\
            , kwargs={'document_id': document_id}))

    elif file_type == 'Region':

        rt = RegionTransform(document_id,file_type,{})
        err,valid_df = rt.validate()
        src_regions = rt.insert_source_regions(valid_df)

        to_map = SourceRegion.objects.filter(regionmap__isnull=True,
            document_id = document_id)

        return render_to_response(
            'data_entry/final_review.html',
            {'document_id': document_id, 'to_map':to_map},
            RequestContext(request),
        )

def map_document_metadata(request,document_id):

    meta_list = []

    to_map_raw = DocumentMeta.objects.raw('''
    SELECT
    	*
    FROM document_meta
    WHERE document_id = %s
    ''',[document_id])

    for row in to_map_raw:

        meta_dict = {}
        meta_dict['source_string'] = row.source_string
        meta_dict['source_object_id'] = row.source_object_id
        meta_dict['master_object_id'] = row.master_object_id
        meta_dict['model_type'] = row.model_type

        meta_list.append(meta_dict)

    return render_to_response(
        'data_entry/meta_map.html',
        {'document_id': document_id, 'to_map':meta_list},
        RequestContext(request),
    )

######### DOCUMENT RELATED VIEWS ##########

class DocumentIndex(generic.ListView):

    context_object_name = "documents"
    template_name = 'document_list.html'
    model = Document


######### META MAPPING ##########


class CreateMap(PermissionRequiredMixin, generic.CreateView):

    template_name='map/map.html'
    success_url=reverse_lazy('source_data:user_portal')
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
