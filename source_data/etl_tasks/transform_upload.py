import xlrd
import pandas as pd
from pprint import pprint

from django.conf import settings
from django.db import transaction
from pandas.io.excel import read_excel

from source_data.models import *
from source_data.etl_tasks.shared_utils import pivot_and_insert_src_datapoints
from datapoints.models import Source, DataPoint


class DocTransform(object):

    def __init__(self,document_id,column_mappings):

        self.source_datapoints = []
        self.document = Document.objects.get(id=document_id)
        self.file_path = settings.MEDIA_ROOT + str(self.document.docfile)
        self.source_id = Source.objects.get(source_name='data entry').id
        self.to_process_status = ProcessStatus.objects.get(status_text='TO_PROCESS').id
        self.column_mappings = column_mappings
        self.df = self.create_df()

    def create_df(self):

        if self.file_path.endswith('.csv'):
            df = pd.read_csv(self.file_path)
        else:
            wb = xlrd.open_workbook(self.file_path)
            sheet = wb.sheets()[0]

            df = read_excel(self.file_path,sheet.name)


        df_no_nan = df.where((pd.notnull(df)), None)
        print 'THIS IS THE DATAFRAME FOR THE UPLOAD BELOW \n' * 5
        print df_no_nan
        return df_no_nan


    def dp_df_to_source_datapoints(self):

        df_cols = [col for col in self.df]

        indicator_col = self.column_mappings['indicator_col']
        if indicator_col == 'cols_are_indicators':

            source_datapoints = pivot_and_insert_src_datapoints(self.df,\
                self.document.id,self.column_mappings)

        else:

            self.df.rename(columns=
                {
                  self.column_mappings['indicator_col']: 'indicator_string',
                  self.column_mappings['region_code_col']: 'region_code',
                  self.column_mappings['campaign_col']: 'campaign_string',
                  self.column_mappings['value_col']: 'cell_value',
                }
            , inplace=True)

            source_datapoints = []
            for row_ix, row_data in self.df.iterrows():

                source_guid = 'doc_id:%s-row_no:%s' % (self.document.id,row_ix)

                sdp_dict = {
                    'source_guid': source_guid,
                    'indicator_string': row_data.indicator_string,
                    'region_code': row_data.region_code,
                    'campaign_string': row_data.campaign_string,
                    'cell_value': row_data.cell_value,
                    'row_number': row_ix,
                    'source_id': self.source_id,
                    'document_id': self.document.id,
                    'status_id': self.to_process_status
                }

                sdp = SourceDataPoint.objects.create(**sdp_dict)
                source_datapoints.append(sdp)

            return source_datapoints


class RegionTransform(DocTransform):


    def validate(self):

        essential_columns = ['name','code','parent_name','region_type','country','lat','lon','high_risk_2014','parent_code']
        df_cols = [col for col in self.df]
        intsct = list(set(essential_columns).intersection(df_cols))

        if sorted(essential_columns) == sorted(intsct):
            valid_df = self.df[essential_columns]

            return None,valid_df

        else:
            err = 'must have all of the following columns: ' + str(essential_columns)
            return err,None


    def insert_source_regions(self,valid_df):
        ''' in this method we take a datframe go through and create a source region
        for each record.  If the source region exists ( the string exists ), we
        update that record with the new values.  After this, we do the same with
        the parent regions.  One fall back currently is that the only conflict
        resolution for this is the fact that newer records take precedence.  This
        means for instance that if you upload a region with no lon/lat it could
        override the same region that currently has lon/lat'''

        valid_df['region_name'] = valid_df['name'] # unable to access name attr directly... fix this

        just_created, updated, errors = [],[],[]

        for row in valid_df.iterrows():

            row_data = row[1]

            sr = SourceRegion.objects.get_or_create(
                region_string = row_data.region_name,\
                region_type  = row_data.region_type,\
                country = row_data.country,
                region_code = row_data.code,\
                parent_name = row_data.parent_name,\
                lat = row_data.lat,\
                lon = row_data.lon,\
                document_id = self.document.id,\
                is_high_risk = row_data.high_risk_2014,\
                parent_code = row_data.parent_code,
                source_guid = str(self.document.id) + '-' + str(row_data.code))

            just_created.append(sr)
