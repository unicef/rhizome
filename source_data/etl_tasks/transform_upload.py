import pprint as pp

import xlrd
import pandas as pd

from django.db import IntegrityError
from django.core.exceptions import ValidationError
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from pandas.io.excel import read_excel

from source_data.models import *
from datapoints.models import DataPoint, Source, Office, Region


class DocTransform(object):

    def __init__(self,document_id,file_type,column_mappings):

        self.source_datapoints = []
        self.file_type = file_type
        self.document = Document.objects.get(id=document_id)
        self.file_path = settings.MEDIA_ROOT + str(self.document.docfile)
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

        for i,(row) in enumerate(self.df.values):
            print 'row_number'
            print i
            sdp, created = SourceDataPoint.objects.get_or_create(
                source_guid = 'doc_id: ' + str(self.document.id) +' row_no: ' + str(i),
                defaults = {
                'indicator_string': row[df_cols.index('Indicator')],
                'region_string': row[df_cols.index('Area Name')],
                'campaign_string': row[df_cols.index('Time Period')],
                'cell_value': row[df_cols.index('Data Value')],
                'row_number': i,
                'source_id': Source.objects.get(source_name='data entry').id,
                'document_id': self.document.id,
                'status_id': ProcessStatus.objects.get(status_text='TO_PROCESS').id
            })
            source_datapoints.append(sdp)


        return source_datapoints


class RegionTransform(DocTransform):


    def validate(self):

        essential_columns = ['name','code','parent_name','region_type','country','lat','lon']
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

        parent_regions = []

        just_created, updated, errors = [],[],[]

        for row in valid_df.iterrows():
            row_data = row[1]
            parent_regions.append(row_data.parent_name)

            try:
                child_defaults = {
                    'region_code': row_data.code,\
                    'parent_name': row_data.parent_name,\
                    'region_type': row_data.region_type,\
                    'country': row_data.country,\
                    'lat': row_data.lat,\
                    'lon': row_data.lon,\
                    'document': self.document,\
                    'source_guid': str(row_data.region_name)}

                sr,created = SourceRegion.objects.get_or_create(
                    region_string = row_data.region_name,\
                    defaults= child_defaults)

            except UnicodeDecodeError as err:
                errors.append(row_data.region_name)

            if created == 1:
                just_created.append(sr)
            else: # update the row in the db with all of the new values.
                updated_sr = SourceRegion.objects.filter(id=sr.id).update(**child_defaults)
                updated.append(updated_sr)


        #############################
        ## Now process the parents ##
        #############################

        distinct_parent_regions = list(set(parent_regions))

        for reg in distinct_parent_regions:

            try:
                parent_defaults = {
                    'region_code': reg,\
                    'document': self.document,\
                    'country': row_data.country,\
                    'source_guid': 'uploaded_as_parent: ' + str(reg)}

            except UnicodeDecodeError as err:
                errors.append(row_data.region_name)

            parent_sr, created = SourceRegion.objects.get_or_create(
                region_string = reg,defaults = parent_defaults)

            if created == 1:
                just_created.append(parent_sr)
            else: # update the row in the db with all of the new values.
                updated_parent_sr = SourceRegion.objects.filter(id=parent_sr.id).\
                    update(**parent_defaults)
                updated.append(parent_sr)
