import sys, os

from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db import IntegrityError
from datapoints.models import Indicator, DataPoint, Region, Campaign, Office, Source
from source_data.models import VCMSummaryNew,VCMSettlement,ProcessStatus
from django.contrib.auth.models import User

from dateutil import parser
from decimal import InvalidOperation

import pprint as pp
import pandas as pd
import csv


class VcmEtl(object):
    def __init__(self,request_guid):
        print 'initializing VCM ETL Object'

        self.request_guid = request_guid

        self.column_to_indicator_map = self.build_indicator_map()
        self.non_indicator_fields = ['submissiondate','deviceid','simserial',\
            'phonenumber','dateofreport','date_implement','settlementcode',\
            'meta_instanceid','key', 'id','process_status_id','request_guid',\
            'created_at']


    def build_indicator_map(self):

        self.inds = Indicator.objects.all()
        self.source_columns = VCMSummaryNew._meta.get_all_field_names()

        # map columns to indicators #
        column_to_indicator_map = {}
        for col in self.source_columns:
            if col in [ind.name for ind in self.inds]:
                column_to_indicator_map[col] = Indicator.objects.get(name=col).id

        return column_to_indicator_map


    def ingest_vcm_datapoints(self):
        to_process = pd.DataFrame(list(VCMSummaryNew.objects.filter(process_status__status_text='TO_PROCESS').values()))


        print 'ROWS TO PROCESS: ' + str(len(to_process))

        column_list = to_process.columns.tolist()

        for i, row in enumerate(to_process.values):
            print 'processing row: ' + str(i)

            row_dict = {}
            for row_i,cell in enumerate(row):
                row_dict[column_list[row_i]] = cell

            row_process_status = self.process_row(row_dict)
            process_status = ProcessStatus.objects.get(status_text=row_process_status)
            row_obj = VCMSummaryNew.objects.get(id=row_dict['id'])
            row_obj.process_status = process_status
            row_obj.save()


    def process_row(self,row_dict):

        try:
            sett_code = row_dict['settlementcode'].replace('.0','')
            region_id = Region.objects.get(settlement_code=sett_code).id
        except TypeError:
            return 'VCM_SUMMARY_NO_SETT_CODE'
            ## Settlement Is Null
        except ValueError:
            return 'VCM_SUMMARY_NO_CAMPAIGN'
        except ObjectDoesNotExist:
            return 'VCM_SUMMARY_NO_SETT_CODE'

        try:
            date_impl = parser.parse(row_dict['date_implement'])
            campaign_id = Campaign.objects.get(start_date=date_impl).id
        except TypeError:
            return 'VCM_SUMMARY_NO_CAMPAIGN'
        except ValueError:
            return 'VCM_SUMMARY_NO_CAMPAIGN'

        except ObjectDoesNotExist:
              return 'VCM_SUMMARY_NO_CAMPAIGN'


        all_cell_status = []


        # process all cells in the row that represnet an indicator value
        for column_name,cell_value, in row_dict.iteritems():

              if column_name not in self.non_indicator_fields:

                  source_guid = row_dict['key'] + '_' + column_name
                  cell_status = self.process_cell(region_id,campaign_id,column_name,cell_value,source_guid)
                  all_cell_status.append(cell_status)

        # HANDLE DUPE ENTRIES BETTER #
        if 'ALREADY_EXISTS' in all_cell_status:
            return 'ALREADY_EXISTS'
        else:
            return 'SUCESS_INSERT'



    def process_cell(self,region_id,campaign_id,column_name,cell_value,src_key):

        if cell_value == "nan":
            return

        if column_name in self.non_indicator_fields:
            return

        cleaned_cell_value = self.clean_cell_value(cell_value)

        indicator_id = Indicator.objects.get(name = column_name).id
        source_id = Source.objects.get(source_name = 'odk').id

        try:
            dp = DataPoint.objects.get_or_create(
                indicator_id = indicator_id, \
                region_id = region_id, \
                campaign_id = campaign_id, \
                value =  cleaned_cell_value, \
                source_id = source_id, \
                source_guid = src_key, \
                changed_by_id = User.objects.get(source_name='odk')
            )
        except IntegrityError as e:
            return 'ALREADY_EXISTS'
            # NEED TO HANDLE DUPE DATA POINTS BETTER #

        return 'SUCESS_INSERT'


    def clean_cell_value(self,cell_value):

        # cell_value = cell_value.lower()

        if cell_value == 'yes':
            cleaned = 1
        elif cell_value == 'no':
            cleaned = 0
        else:
            cleaned = cell_value

        return cleaned

        ##########################
        #### META DATA INGEST ####
        ##########################

    def ingest_indicators(self):

        v = VCMSummaryNew()
        all_fields = v._meta.fields

        indicators = []
        for f in all_fields:
            if f.name not in self.non_indicator_fields:
                indicators.append(f.name)

        for i in indicators:
            try:
                created = Indicator.objects.create(name = i,description = i, \
                  is_reported = 1)
            except IntegrityError:
                pass

    def ingest_regions(self):

        to_process = VCMSettlement.objects.filter(process_status__status_text='TO_PROCESS')
        for row in to_process:
            print row

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
                row.process_status=ProcessStatus.objects.get(status_text='SUCESS_INSERT')
                row.save()

            except IntegrityError:
                # THIS SHOULD BE AN UPDATE SO THAT NEWER REGIONS ARE INSERTED #
                # AND THE OLD ONES ARE BROUGTH UP FOR REVIEW #

                # THIS SHOULD ALSO BE ABSTRACTED TO WORK FOR ALL' MASTER' OBJECTS
                row.process_status=ProcessStatus.objects.get(status_text='ALREADY_EXISTS')
                row.save()



    def ingest_campaigns(self):
        all_data = VCMSummaryNew.objects.all()
        all_campaigns = []

        # Ensure the Office ID is in there
        try:
            ng_office_id = Office.objects.get(name='Nigeria')
        except ObjectDoesNotExist:
            ng_office = Office.objects.create(name='Nigeria')
            ng_office_id = ng_office.id

        for row in all_data:
            if row.date_implement == 'nan':
                return

            try:
                created = Campaign.objects.create(
                    name = 'Nigeria Starting:' + row.date_implement, \
                    office = ng_office_id, \
                    start_date = parser.parse(row.date_implement), \
                    end_date = parser.parse(row.date_implement)
                )
            except IntegrityError:
                pass
