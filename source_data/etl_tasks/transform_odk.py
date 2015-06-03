import pandas as pd
import json
import traceback
from pprint import pprint

from django.db import IntegrityError
from django.contrib.auth.models import User

from datapoints.models import Region, Office, Source
from source_data.models import *
from source_data.etl_tasks.shared_utils import map_regions

try:
    import source_data.prod_odk_settings as odk_settings
except ImportError:
    import source_data.dev_odk_settings as odk_settings


class VcmSummaryTransform(object):
    def __init__(self,request_guid,document_id, to_process_df):

        self.request_guid = request_guid
        self.source_id = Source.objects.get(source_name ='odk').id
        self.source_datapoints = []
        self.document_id = document_id
        self.to_process_df = to_process_df

        self.process_status_id = ProcessStatus.objects\
            .get(status_text='SUCCESS_INSERT').id


    def vcm_summary_to_source_datapoints(self):

        self.to_process_df.columns = map(str.lower, self.to_process_df)
        column_list = self.to_process_df.columns.tolist()

        for row_number, row in enumerate(self.to_process_df.values):

            row_dict = dict(zip(column_list,row))

            self.process_row(row_dict,row_number)

        return None, 'processed : ' + str(len(to_process)) + ' records'


    def process_row(self,row_dict,row_number):

        row_batch = []

        print '======\n' * 2
        pprint(row_dict)

        region_code = row_dict['settlementcode']
        campaign_string = row_dict['date_implement']
        source_guid = row_dict['key']

        for cell_no, (indicator_string, cell_value) in enumerate(row_dict.iteritems()):

            if cell_value != "" and cell_value != "nan":
                pass

            else:

                cell_guid =  'doc_id: ' + str(self.document_id) + ' row_no: ' + \
                    str(row_number) + ' cell_no: ' + str(cell_no) \
                    + ' indicator_string: ' + str(indicator_string)


                cleaned_cell_value = self.clean_cell_value(cell_value)

                sdp = SourceDataPoint(**{
                    'region_code' : region_code,
                    'campaign_string' : campaign_string,
                    'indicator_string' : indicator_string,
                    'cell_value' : cleaned_cell_value,
                    'row_number' : row_number,
                    'source_id': self.source_id,
                    'document_id' : self.document_id,
                    'source_guid' : source_guid,
                    'status_id' : self.process_status_id,
                    'guid': cell_guid
                })
                row_batch.append(sdp)

            try:
                SourceDataPoint.objects.bulk_create(row_batch)
            except IntegrityError:
                pass


    def clean_cell_value(self,cell_value):

        if cell_value == 'yes':
            cleaned = 1
        elif cell_value == 'no':
            cleaned = 0
        else:
            cleaned = cell_value

        return cleaned


    ###########################
    ##### VCM SETTLEMENT ######
    ###########################

    def map_vcm_settlement_regions(self):

        to_process = VCMSettlement.objects.filter(process_status__status_text='TO_PROCESS')
        for row in to_process:

            try:
                created = Region.objects.create(
                  full_name = row.settlementname ,\
                  settlement_code = row.settlementcode ,\
                  office = Office.objects.get(name='Nigeria') ,\
                  latitude = row.settlementgps_latitude ,\
                  longitude = row.settlementgps_longitude ,\
                  source = Source.objects.get(source_name='odk') ,\
                  source_guid = row.key
                )
                row.process_status=ProcessStatus.objects.get(status_text='SUCCESS_INSERT')
                row.save()

            except IntegrityError:
                # THIS SHOULD BE AN UPDATE SO THAT NEWER REGIONS ARE INSERTED #
                # AND THE OLD ONES ARE BROUGTH UP FOR REVIEW #

                # THIS SHOULD ALSO BE ABSTRACTED TO WORK FOR ALL' MASTER' OBJECTS
                row.process_status=ProcessStatus.objects.get(status_text='ALREADY_EXISTS')
                row.save()
