import sys
import os
import pprint as pp
import pandas as pd
import csv

from dateutil import parser
from decimal import InvalidOperation

from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db import IntegrityError
from django.contrib.auth.models import User

from datapoints.models import Indicator, DataPoint, Region, Campaign, Office, Source
from source_data.models import *
from source_data.etl_tasks.shared_utils import map_indicators, map_campaigns, map_regions

class VcmSettlementTransform(object):

    def __init__(self,request_guid):

        self.requist_guid = request_guid
        self.source_id = Source.objects.get(source_name ='odk').id

    def refresh_source_regions(self):

        region_dict_list = []

        to_process_df = pd.DataFrame(list(VCMSettlement.objects.filter\
            (process_status__status_text='TO_PROCESS').values()))

        cols = [col.lower() for col in to_process_df]

        for row in to_process_df.values:
            row_dict = {}

            row_dict['region_string'] = row[cols.index('settlementname')]
            row_dict['settlement_code'] = row[cols.index('settlementcode')]
            row_dict['lat'] = row[cols.index('settlementgps_latitude')]
            row_dict['lon'] = row[cols.index('settlementgps_latitude')]
            row_dict['source_guid'] = row[cols.index('key')]

            region_dict_list.append(row_dict)

        mappings = map_regions(region_dict_list,self.source_id)
        pp.pprint(mappings)

        return mappings



class VcmSummaryTransform(object):
    def __init__(self,request_guid):
        print 'initializing VCM ETL Object'

        self.request_guid = request_guid
        self.source_id = Source.objects.get(source_name ='odk').id


    def pre_process_odk(self):

        all_meta_mappings = {}

        to_process_df = pd.DataFrame(list(VCMSummaryNew.objects.filter\
            (process_status__status_text='TO_PROCESS').values()))

        all_meta_mappings['campaigns'] = self.get_campaign_mappings(to_process_df)
        all_meta_mappings['indicators'] = self.get_indicator_mappings(to_process_df)
        all_meta_mappings['regions'] = self.get_region_mappings(to_process_df)

        pp.pprint(all_meta_mappings)

        return all_meta_mappings



        ##########################
        #### META DATA INGEST ####
        ##########################

    def get_region_mappings(self,df):

        region_dict_list = []

        sett_codes = df.groupby('settlementcode')

        for sett_code in sett_codes:

            region_dict = {'settlement_code':sett_code[0]}
            region_dict_list.append(region_dict)

        region_mapping = map_regions(region_dict_list,self.source_id)

        return region_mapping

    def get_indicator_mappings(self,df):

        indicator_strings = [col.lower() for col in df]
        indicator_mapping = map_indicators(indicator_strings,self.source_id)

        return indicator_mapping


    def get_campaign_mappings(self,df):

        source_campaign_strings = []

        gb_df = df.groupby('date_implement')

        for record in gb_df['date_implement']:
            source_campaign_strings.append(record[0])

        campaign_mapping = map_campaigns(source_campaign_strings,self.source_id)

        return campaign_mapping


        def vcm_summary_to_source_datapoints(self):
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
                    changed_by_id = User.objects.get(username='odk').id
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
                row.process_status=ProcessStatus.objects.get(status_text='SUCESS_INSERT')
                row.save()

            except IntegrityError:
                # THIS SHOULD BE AN UPDATE SO THAT NEWER REGIONS ARE INSERTED #
                # AND THE OLD ONES ARE BROUGTH UP FOR REVIEW #

                # THIS SHOULD ALSO BE ABSTRACTED TO WORK FOR ALL' MASTER' OBJECTS
                row.process_status=ProcessStatus.objects.get(status_text='ALREADY_EXISTS')
                row.save()
