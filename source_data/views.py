import xlrd, csv, pandas, pprint as pp

from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.db import IntegrityError
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist

from pandas.io.excel import read_excel

from source_data.forms import DocumentForm
from source_data.models import Document,CsvUpload,ProcessStatus
from datapoints.models import Source
from meta_map.models import *


def file_upload(request):
    # Handle file upload
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = Document(docfile = request.FILES['docfile'])
            newdoc.created_by = request.user
            newdoc.save()

            file_path = newdoc.docfile.url

            if file_path.endswith('xls') or file_path.endswith('xlsx'):

                mappings = process_xls(file_path,newdoc.id)

                return document_review(request,newdoc.id,mappings)

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



def process_xls(f_path,document_id):

    wb = xlrd.open_workbook(f_path)

    for sheet in wb.sheets():
        # process_sheet(sheet)

        if sheet.nrows == 0:
            pass
        else:
            mappings = process_sheet(f_path,sheet.name,document_id)
            return mappings


def process_sheet(file_path,sheet_name,document_id):

    df = read_excel(file_path,sheet_name)
    cols = [col.lower() for col in df]

    mappings = auto_map_metadata(df)

    return mappings

    # for i,(row) in enumerate(df.values):
    #
    #     row_basics = {}
    #
    #     region_string = row[cols.index('lga')] + '-' + row[cols.index('state')] \
    #         + '-' + row[cols.index('ward')] + '-' + str(row[cols.index('settlement')])
    #
    #     row_basics['row_number'] = i
    #     row_basics['region_string'] = region_string
    #     row_basics['campaign_string'] = str(row[cols.index('datesoc')])
    #     # row_basics['uniquesoc'] = row[cols.index('uniquesoc')]
    #
    #     for i,(cell) in enumerate(row):
    #
    #         to_create = row_basics
    #         to_create['column_value'] = cols[i]
    #         to_create['cell_value'] = cell
    #         to_create['status_id'] = ProcessStatus.objects.get(status_text='TO_PROCESS').id
    #         to_create['document_id'] = document_id
    #
    #         try:
    #             CsvUpload.objects.create(**to_create)
    #
    #         except IntegrityError as e:
    #             print e



def auto_map_metadata(sheet_df):

    all_meta_mappings = {}
    source_id = Source.objects.get(source_name ='Spreadsheet Upload').id

    all_meta_mappings['campaigns'] = map_campaigns(sheet_df,source_id)
    all_meta_mappings['indicators'] = map_indicators(sheet_df,source_id)
    all_meta_mappings['regions'] = map_regions(sheet_df,source_id)

    return all_meta_mappings

def map_indicators(sheet_df,source_id):
    indicator_mapping = {}
    cols = [col.lower() for col in sheet_df]

    for col_name in cols:

        source_indicator, created = SourceIndicator.objects.get_or_create(
            source_id = source_id,
            indicator_string = col_name
        )

        try:
            indicator_id = IndicatorMap.objects.get(source_indicator_id = source_indicator.id)
            indicator_mapping[col_name] = indicator_id
            source_indicator.mapped_status='MAPPED'
        except ObjectDoesNotExist:
            indicator_mapping[col_name] = None

    return indicator_mapping


def map_campaigns(sheet_df,source_id):

    ## CAMPAIGN MAPPING ##
    campaign_mapping = {}
    campaigns = sheet_df.groupby('DateSoc')

    for campaign in campaigns:
        print campaign[0]

        source_campaign, created = SourceCampaign.objects.get_or_create(
            source_id = source_id,
            campaign_string = campaign[0]
        )
        try:
            campaign_id = CampaignMap.objects.get(source_campaign_id = source_campaign.id)
            campaign_mapping[campaign] = campaign_id
            source_indicator.mapped_status='MAPPED'
        except ObjectDoesNotExist:
            campaign_mapping[source_campaign] = None

    return campaign_mapping

def map_regions(sheet_df,source_id):

    return {'foo':'bar'}

def document_review(request,document_id,mappings):

    doc_data = []

    r = {'problem':'Indicators to Map','recs':len(mappings['indicators'])}
    r2 = {'problem':'Campaigns to Map','recs':len(mappings['campaigns'])}
    r3 = {'problem':'Regions To Map','recs':len(mappings['regions'])}


    doc_data.append(r)
    doc_data.append(r2)
    doc_data.append(r3)


    return render_to_response(
        'upload/document_review.html',
        {'doc_data': doc_data},
        context_instance=RequestContext(request),
    )
