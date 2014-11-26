import pprint as pp

import xlrd
import pandas as pd

from django.db import IntegrityError
from django.core.exceptions import ValidationError
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from pandas.io.excel import read_excel

from source_data.models import *
from datapoints.models import DataPoint, Source


class DocTransform(object):

    def __init__(self,document_id,file_type):

        self.source_datapoints = []
        self.file_type = file_type
        self.document = Document.objects.get(id=document_id)
        self.file_path = settings.MEDIA_ROOT + str(self.document.docfile)
        self.df = self.create_df()

    def create_df(self):

        if self.file_path.endswith('.csv'):
            df = pd.read_csv(self.file_path)
        else:
            wb = xlrd.open_workbook(self.file_path)
            sheet = wb.sheets()[0]

            df = read_excel(self.file_path,sheet.name)

        return df

    def get_essential_columns(self):

        column_mapping = {
            'region':[],
            'Campaign':[]
        }

        header_list = [str(col) for col in self.df.columns.values]

        overrides = HeaderOverride.objects.filter(header_string__in=header_list)

        for o in overrides:
            try:
                print o.content_type.name
                column_mapping[o.content_type.name].append(o.header_string)
            except KeyError:
                pass

        return column_mapping

class RegionTransform(DocTransform):


    def validate(self):

        essential_columns = ['name','code','parent_name','region_type','country']
        df_cols = [col for col in self.df]
        intsct = list(set(essential_columns).intersection(df_cols))

        if sorted(essential_columns) == sorted(intsct):
            valid_df = self.df[essential_columns]
            return None,valid_df
        else:
            err = 'must have all of the following columns: ' + essential_columns
            return err,None


    def insert_source_regions(self,valid_df):

        valid_df['region_name'] = valid_df['name'] # unable to access name attr directly... fix this

        for row in valid_df.iterrows():
            row_data = row[1]
            # print valid_df
            print row_data.region_name

            try:
                SourceRegion.objects.create(

                    region_string = row_data.region_name,\
                    region_code = row_data.code,\
                    parent_name = row_data.parent_name,\
                    region_type = row_data.region_type,\
                    country = row_data.country,\
                    document_id = self.document.id
                )
            except IntegrityError as err:
                print 'errrrrror'
                print err
