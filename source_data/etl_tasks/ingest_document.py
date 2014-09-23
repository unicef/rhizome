import pprint as pp

from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from source_data.models import ProcessStatus, CsvUpload, SourceIndicator, IndicatorMap

def process_sheet_df(df,document_id):

    sheet_df_to_work_table(df,document_id)
    ingest_doc_to_master(document_id)

def sheet_df_to_work_table(df,document_id):

    cols = [col.lower() for col in df]
    print '=' * 50
    pp.pprint(cols)

    for i,(row) in enumerate(df.values):

        row_basics = {}
        #
        region_string = row[cols.index('lga')] + '-' + row[cols.index('state')] \
            + '-' + row[cols.index('ward')] + '-' + str(row[cols.index('settlement')])

        row_basics['row_number'] = i
        row_basics['region_string'] = region_string
        row_basics['campaign_string'] = str(row[cols.index('datesoc')])
        row_basics['uniquesoc'] = row[cols.index('uniquesoc')]
        #
        for i,(cell) in enumerate(row):

            to_create = row_basics
            to_create['column_value'] = cols[i]
            to_create['cell_value'] = cell


            to_create['status_id'] = ProcessStatus.objects.get(status_text='TO_PROCESS').id
            to_create['document_id'] = document_id

            try:
                CsvUpload.objects.create(**to_create)

            except IntegrityError as e:
                print e


def ingest_doc_to_master(document_id):

    to_process = CsvUpload.objects.filter(document_id=document_id)

    for record in to_process:
        csv_upload_record_to_datapoint(record)



def csv_upload_record_to_datapoint(record):

    source_ind_id = SourceIndicator.objects.get(indicator_string=record.column_value).id

    try:
        master_ind_id = IndicatorMap.objects.get(source_indicator_id=source_ind_id).master_indicator_id
    except ObjectDoesNotExist:
        return

    # DataPoint.objects.get_or_create(
    #     indicator_id = master_ind_id,
    #     region_id = master_reg_id,
    #     campaign_id = master_camp_id,
    #     value = record.cell_value,
    #     source_id = Source.objects.get(source_name='Spreadsheet Upload'),
    #     source_guid = record.guid
    # )
