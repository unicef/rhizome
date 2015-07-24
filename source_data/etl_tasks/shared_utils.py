from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError

from source_data.models import *
from datapoints.models import Office

def pivot_and_insert_src_datapoints(df,document_id,column_mappings):

    header = [col for col in df]
    source_datapoints = []

    source_id = Source.objects.get(source_name='data entry').id

    for row_number,(row) in enumerate(df.values):

        batch = []

        region_code = row[header.index(column_mappings['region_code_col'])]
        campaign_string = row[header.index(column_mappings['campaign_col'])]
        to_process_status = ProcessStatus.objects.get(status_text='TO_PROCESS').id

        for cell_no,(column_header) in enumerate(header):

            indicator_string = header[cell_no]

            row_guid =  'doc_id: ' + str(document_id) + ' row_no: ' + \
                str(row_number) + ' cell_no: ' + str(cell_no)

            sdp_dict = {
                'source_guid':row_guid,
                'guid':row_guid,
                'indicator_string': indicator_string,
                'region_code':region_code,
                'campaign_string':campaign_string,
                'cell_value':row[cell_no],
                'row_number':row_number,
                'source_id':source_id,
                'document_id':document_id,
                'status_id':to_process_status
            }

            sdp = SourceDataPoint(**sdp_dict)

            batch.append(sdp)

        SourceDataPoint.objects.bulk_create(batch)


    sdps = SourceDataPoint.objects.filter(document_id=document_id)
    return sdps
    # return source_datapoints
