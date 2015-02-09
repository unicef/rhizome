import hashlib
from itertools import chain

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib import messages
from django.views import generic
from django.core.urlresolvers import reverse, reverse_lazy
from django.http import HttpResponseRedirect

from datapoints.mixins import PermissionRequiredMixin
from datapoints.models import DataPoint, Responsibility
from source_data.forms import *
from source_data.models import *
from source_data.etl_tasks.transform_upload import DocTransform,RegionTransform
from source_data.etl_tasks.refresh_master import MasterRefresh
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


def review_sdps_by_document(request,document_id):

    source_datapoints = SourceDataPoint.objects.filter(document_id=document_id)

    return render_to_response(
        'upload/document_review.html',
        {'to_review': source_datapoints,'document_id': document_id},
        RequestContext(request),
    )


def refresh_master_by_document_id(request,document_id):

    source_datapoints = SourceDataPoint.objects.filter(
        document_id=document_id,\
        status = ProcessStatus.objects.get(status_text='TO_PROCESS'))#[:1000]

    source_regions = SourceRegion.objects.filter(document_id=document_id)

    m = MasterRefresh(source_datapoints,user_id = request.user.id,document_id=document_id)
    m.main()


    ## Need to Handle region uploads here as well.
    region_strings = [sd.region_string for sd in source_datapoints] + \
        [sr.region_string for sr in source_regions]

    indicator_strings = [sd.indicator_string for sd in source_datapoints]
    campaign_strings = [sd.campaign_string for sc in source_datapoints]

    doc_datapoints = DataPoint.objects.filter(source_datapoint_id__in=
        SourceDataPoint.objects.filter(document_id=document_id))

    si = SourceIndicator.objects.filter(indicatormap__isnull=True,
        indicator_string__in=indicator_strings)

    cp = SourceCampaign.objects.filter(campaignmap__isnull=True,
        campaign_string__in=campaign_strings)

    rg = SourceRegion.objects.filter(regionmap__isnull=True,
        region_string__in=region_strings)

    to_map = chain(si,cp,rg)

    i_m = IndicatorMap.objects.filter(source_indicator__document_id=document_id)
    c_m = CampaignMap.objects.filter(source_campaign__document_id=document_id)
    r_m = RegionMap.objects.filter(source_region__document_id=document_id)

    all_mapped = chain(i_m, c_m, r_m)


    return render_to_response(
        'data_entry/final_review.html',
        {'datapoints': doc_datapoints, 'document_id': document_id,\
         'to_map':to_map, 'all_mapped':all_mapped },
         RequestContext(request),)

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

def pre_process_file(request,document_id,file_type):

    if file_type == 'Datapoint':

        column_mappings = {}
        column_mappings['campaign_col'] = request.GET['campaign_col']
        column_mappings['value_col'] = request.GET['value_col']
        column_mappings['region_col'] = request.GET['region_col']
        column_mappings['indicator_col'] = request.GET['indicator_col']

        dt = DocTransform(document_id,file_type,column_mappings)
        sdps = dt.dp_df_to_source_datapoints()

        return render_to_response(
            'upload/document_review.html',
            {'document_id':document_id,'to_review':sdps},
            RequestContext(request),
        )

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
