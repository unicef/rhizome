import xlrd
import pandas as pd

from django.conf import settings
from pandas.io.excel import read_excel

from source_data.models import *
from source_data.etl_tasks.shared_utils import pivot_and_insert_src_datapoints
from datapoints.models import Source


class DocTransform(object):

    def __init__(self,document_id,file_type,column_mappings):

        self.source_datapoints = []
        self.file_type = file_type
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


        return df


    def dp_df_to_source_datapoints(self):

        source_datapoints = []

        df_cols = [col for col in self.df]

        indicator_col = self.column_mappings['indicator_col']
        if indicator_col == 'cols_are_indicators':
            # do stuff #
            source_datapoints = pivot_and_insert_src_datapoints(self.df,\
                self.document.id,self.column_mappings)


        else:

            for i,(row) in enumerate(self.df.values):

                sdp, created = SourceDataPoint.objects.get_or_create(
                    source_guid = 'doc_id: ' + str(self.document.id) +' row_no: ' + str(i),
                    defaults = {
                    'indicator_string': row[df_cols.index(self.column_mappings['indicator_col'])],
                    'region_code': row[df_cols.index(self.column_mappings['region_col'])],
                    'campaign_string': row[df_cols.index(self.column_mappings['campaign_col'])],
                    'cell_value': row[df_cols.index(self.column_mappings['value_col'])],
                    'row_number': i,
                    'source_id': self.source_id,
                    'document_id': self.document.id,
                    'status_id': self.to_process_status
                })
                source_datapoints.append(sdp)


        return source_datapoints


class RegionTransform(DocTransform):


    def validate(self):

        essential_columns = ['name','code','parent_name','region_type','country','lat','lon','high_risk_2014']
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
                source_guid = str(self.document.id) + '-' + row_data.code)

            just_created.append(sr)
