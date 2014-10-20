import pprint as pp

import xlrd
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from pandas.io.excel import read_excel

from source_data.models import *
from datapoints.models import DataPoint, Source


class DocTransform(object):

    def __init__(self,document_id):

        self.source_datapoints = []
        self.document_id = document_id
        self.file_path = settings.MEDIA_ROOT + \
            str(Document.objects.get(id=document_id).docfile)

    def create_df(self):

        if self.file_path.endswith('.csv'):
            df = pd.read_csv(self.file_path)
        else:
            wb = xlrd.open_workbook(self.file_path)
            sheet = wb.sheets()[0]

            df = read_excel(self.file_path,sheet.name)


        return df


    def pre_process_sheet(self,file_path,sheet_name,document_id):

        pass

    #
    # def sheet_df_to_source_datapoints(self):
    #     ## I AM HACKING THE SHIT OUT OF THIS RIGHT NOW TO GET SPREADSHEETS IN ##
    #
    #     cols = [col.lower() for col in self.df]
    #
    #     for i,(row) in enumerate(self.df.values):
    #
    #         row_basics = {}
    #
    #         # HACK ALERT #
    #         try:
    #             region_string = row[cols.index('lga')] + '-' + row[cols.index('state')] \
    #                 + '-' + row[cols.index('ward')] + '-' + str(row[cols.index('settlement')])
    #         except ValueError:
    #             pass
    #
    #         try:
    #             region_string = row[cols.index('lga')] + '-' + row[cols.index('state')] \
    #                 + '-' + row[cols.index('ward')] + '-' + str(row[cols.index('settlename')])
    #         except ValueError:
    #             pass
    #
    #         try:
    #             region_string = row[cols.index('lga')] + '-' + row[cols.index('state')] \
    #                 + '-' + row[cols.index('ward')] + '-' + str(row[cols.index('settlements')])
    #         except ValueError:
    #             pass
    #
    #         try:
    #             region_string = row[cols.index('lga')] + '-' + row[cols.index('state')] \
    #                 + '-' + row[cols.index('ward')]
    #         except ValueError:
    #             pass
    #
    #
    #         row_basics['row_number'] = i
    #         row_basics['region_string'] = region_string
    #
    #         try:
    #             row_basics['campaign_string'] = str(row[cols.index('datesoc')])
    #         except ValueError:
    #             pass
    #
    #         try:
    #             row_basics['campaign_string'] = str(row[cols.index('datemonitor')])
    #         except ValueError:
    #             pass
    #
    #         try:
    #             row_basics['source_guid'] = row[cols.index('mainmonid')]
    #         except ValueError:
    #             pass
    #
    #         try:
    #             row_basics['source_guid'] = row[cols.index('uniquekey')]
    #         except ValueError:
    #             pass
    #
    #
    #
    #         #
    #         for i,(cell) in enumerate(row):
    #
    #             to_create = row_basics
    #             to_create['indicator_string'] = cols[i]
    #             to_create['cell_value'] = cell
    #
    #
    #             to_create['status_id'] = ProcessStatus.objects.get(status_text='TO_PROCESS').id
    #             to_create['source_id'] = Source.objects.get(source_name='Spreadsheet Upload').id
    #             to_create['document_id'] = self.document_id
    #
    #             try:
    #                 created = SourceDataPoint.objects.create(**to_create)
    #                 self.source_datapoints.append(created)
    #             except IntegrityError as e:
    #                 print e


# import xlrd, pandas, pprint as pp
#
# from django.core.exceptions import ObjectDoesNotExist
# from pandas.io.excel import read_excel
#
# from datapoints.models import Source
# from source_data.models import *
# from source_data.etl_tasks.shared_utils import map_indicators
#
#
# class PreIngest(object):
#
#     def __init__(self,file_path,document_id):
#         self.file_path = file_path
#         self.document_id = document_id
#         self.source_id = Source.objects.get(source_name ='Spreadsheet Upload').id
#
#
#         self.df, self.mappings = self.main(file_path, document_id)
#
#     def main(self,file_path, document_id):
#         ''' in this method we create or find the source metadata and return the
#         values as a dictionary.'''
#
#         if file_path.endswith('.csv'):
#             print 'bla'
#
#         else:
#
#             wb = xlrd.open_workbook(file_path)
#
#             for sheet in wb.sheets():
#
#                 if sheet.nrows == 0:
#                     pass
#                 else:
#                     mappings = self.pre_process_sheet(file_path,sheet.name,document_id)
#                     return mappings
#
#         return df, mappings
#
#
#     def pre_process_sheet(self,file_path,sheet_name,document_id):
#
#         sheet_df = read_excel(file_path,sheet_name)
#         cols = [col.lower() for col in sheet_df]
#
#         all_meta_mappings = {}
#
#         all_meta_mappings['campaigns'] = self.map_campaigns(sheet_df)
#         all_meta_mappings['indicators'] = map_indicators(sheet_df,self.source_id)
#         all_meta_mappings['regions'] = self.map_regions(sheet_df)
#
#         return sheet_df,all_meta_mappings
#
#
#     def map_campaigns(self,sheet_df):
#
#         ## CAMPAIGN MAPPING ##
#         campaign_mapping = {}
#         campaigns = sheet_df.groupby('DateSoc')
#
#         for campaign in campaigns:
#
#             source_campaign, created = SourceCampaign.objects.get_or_create(
#                 source_id = self.source_id,
#                 campaign_string = campaign[0]
#             )
#             try:
#                 campaign_id = CampaignMap.objects.get(source_campaign_id = \
#                     source_campaign.id).master_campaign_id
#
#                 campaign_mapping[str(campaign[0])] = campaign_id
#             except ObjectDoesNotExist:
#                 pass
#
#         return campaign_mapping
#
#     def map_regions(self,df):
#         ## REGION MAPPING ##
#         region_mapping = {}
#
#
#         # HACKING FOR NOW TO DEAL WITH DIFFERENT COLUMN HEADERS
#         try:
#             df['region_string']  = df['Lga'] + '-' + df['State'] + '-' + \
#                 df['Ward'] + '-' + df['Settlement'].apply(str)
#         except KeyError:
#             pass
#
#         try:
#             df['region_string']  = df['Lga'] + '-' + df['State'] + '-' + \
#                 df['Ward'] + '-' + df['SettleName'].apply(str)
#         except KeyError:
#             pass
#
#
#
#         regions = df.groupby('region_string')
#
#         for region in regions:
#
#             source_region_id, created = SourceRegion.objects.get_or_create(
#                 source_id = self.source_id,
#                 region_string = region[0]
#             )
#
#             try:
#                 region_id = RegionMap.objects.get(source_region_id = \
#                     source_region_id.id).master_region_id
#                 region_mapping[region[0]] = region_id
#             except ObjectDoesNotExist:
#                 pass
#
#         return region_mapping
