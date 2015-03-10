import pandas as pd
import json
import traceback

from django.db import IntegrityError
from django.contrib.auth.models import User

from datapoints.models import Region, Office, Source
from source_data.models import *
from source_data.etl_tasks.shared_utils import map_regions

try:
    import source_data.prod_odk_settings as odk_settings
except ImportError:
    import source_data.dev_odk_settings as odk_settings

class VcmSettlementTransform(object):

    def __init__(self,request_guid):

        self.requist_guid = request_guid
        self.source_id = Source.objects.get(source_name ='odk').id

    def refresh_source_regions(self):

        try:
            region_codes = []

            to_process_df = pd.DataFrame(list(VCMSettlement.objects.filter\
                (process_status__status_text='TO_PROCESS').values()))

            cols = [col.lower() for col in to_process_df]

            for row in to_process_df.values:
                row_dict = {}

                row_dict['region_code'] = row[cols.index('settlementname')]
                row_dict['settlement_code'] = row[cols.index('settlementcode')]
                row_dict['lat'] = row[cols.index('settlementgps_latitude')]
                row_dict['lon'] = row[cols.index('settlementgps_longitude')]

                row_data = json.dumps(row_dict)

                region_codes.append(row_data)

            mappings = map_regions(region_codes,self.source_id)
        except Exception:
            err = traceback.format_exc()
            return err, None

        return None, 'ODK SOURCE REGIONS REFRESHED'



class VcmSummaryTransform(object):
    def __init__(self,request_guid):

        self.request_guid = request_guid
        self.source_id = Source.objects.get(source_name ='odk').id
        self.source_datapoints = []
        self.document_id = self.get_document_id()


    def get_document_id(self):

        doc, created = Document.objects.get_or_create(
            docfile = odk_settings.EXPORT_DIRECTORY + 'New_VCM_Summary.csv',
            created_by_id = User.objects.get(username='odk').id,
            source_id = Source.objects.get(source_name='odk').id,
        )

        return doc.id


    def vcm_summary_to_source_datapoints(self):

        try:
            to_process = pd.DataFrame(list(VCMSummaryNew.objects.filter(\
                process_status__status_text='TO_PROCESS').values()))

            column_list = to_process.columns.tolist()

            for row_number, row in enumerate(to_process.values):

                row_dict = {}
                for row_i,cell in enumerate(row):
                    row_dict[column_list[row_i]] = cell

                print 'processing row number: ' + str(row_number)

                self.process_row(row_dict,row_number)

                process_status_id = ProcessStatus.objects.get(status_text='SUCCESS_INSERT').id
                row_obj = VCMSummaryNew.objects.get(key=row_dict['key'])

                row_obj.process_status_id = process_status_id
                row_obj.save()

        except Exception:
            err = traceback.format_exc()
            return err, None

        return None, 'processed : ' + str(len(to_process)) + ' records'


    def process_row(self,row_dict,row_number):


        # row level variables
        region_code = row_dict['settlementcode']
        campaign_string = row_dict['date_implement']
        source_guid = row_dict['key']

        for indicator_string, cell_value in row_dict.iteritems():

            self.process_cell(region_code,campaign_string,indicator_string,\
                cell_value,source_guid,row_number)


    def process_cell(self,region_code,campaign_string,indicator_string,\
            cell_value,src_key,row_number):

        if cell_value == "" or cell_value == "nan":
            return

        cleaned_cell_value = self.clean_cell_value(cell_value)

        try:
            sdp = SourceDataPoint.objects.create(
                region_code = region_code,
                campaign_string = campaign_string,
                indicator_string =  indicator_string,
                cell_value = cleaned_cell_value,
                row_number = row_number,
                source = Source.objects.get(source_name='odk'),
                document_id = self.document_id,
                source_guid = src_key,
                status = ProcessStatus.objects.get(status_text='TO_PROCESS')
            )
            self.source_datapoints.append(sdp)
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
