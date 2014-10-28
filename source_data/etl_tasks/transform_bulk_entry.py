import uuid

from datapoints.models import Source
from source_data.models import *

def bulk_data_to_sdps(bulk_data,campaign_string,delimiter,document_id):

    campaign_string = campaign_string
    source_datapoints = []


    rows = bulk_data.split('\r')

    header = rows[0].split(delimiter)
    del rows[0]

    for row_number ,(row) in enumerate(rows):

        source_guid = str(uuid.uuid4()) ## Each Row needs a unique ID

        cells = row.split(delimiter)

        for i,(cell) in enumerate(cells):

            if i > 0: # this assumes the region is always zero indexed

                # try:
                sdp = SourceDataPoint.objects.create(
                    indicator_string = header[i],
                    region_string = cells[0],
                    campaign_string = campaign_string,
                    cell_value = cell,
                    source_guid = source_guid,
                    row_number= row_number,
                    source_id = Source.objects.get(source_name='data entry').id,
                    document_id = document_id,
                    status_id = ProcessStatus.objects.get(status_text='TO_PROCESS').id
                )
                source_datapoints.append(sdp)
                # except


    not_parsed = { 'r':'q' }

    return source_datapoints, not_parsed
