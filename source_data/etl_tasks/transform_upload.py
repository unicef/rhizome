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
        # http://localhost:8000/datapoints/regions
        # http://localhost:8000/source_data/pre_process_file/595/Region/

        valid_df['region_name'] = valid_df['name'] # unable to access name attr directly... fix this

        parent_regions = []

        just_created, updated, errors = [],[],[]

        for row in valid_df.iterrows():
            row_data = row[1]
            parent_regions.append(row_data.parent_name)

            child_defaults = {
                'region_code': row_data.code,\
                'parent_name': row_data.parent_name,\
                'region_type': row_data.region_type,\
                'country': row_data.country,\
                'lat': row_data.lat,\
                'lon': row_data.lon,\
                'document': self.document,\
                'source_guid': row_data.region_name.encode('utf-8') \
                    + ' - ' + str(row_data.code)}

            try:
                sr,created = SourceRegion.objects.get_or_create(
                    region_string = row_data.region_name,\
                    defaults= child_defaults)

                if created == 1:
                    just_created.append(sr)
                else: # update the row in the db with all of the new values.
                    updated_sr = SourceRegion.objects.filter(id=sr.id).update(**child_defaults)
                    updated.append(updated_sr)

            except UnicodeDecodeError as err:
                errors.append(row_data.region_name)

        ## Now process the parents
        distinct_parent_regions = list(set(parent_regions))

        for reg in distinct_parent_regions:
            parent_defaults = {
                'region_code': reg,\
                'document': self.document,\
                'source_guid': 'parent_reg :' + reg + ' from doc_id: ' + \
                    str(self.document.id)}

            parent_sr, created = SourceRegion.objects.get_or_create(
                region_string = reg,defaults = parent_defaults)

            if created == 1:
                just_created.append(parent_sr)
            else: # update the row in the db with all of the new values.
                updated_parent_sr = SourceRegion.objects.filter(id=parent_sr.id).\
                    update(**parent_defaults)
                updated.append(parent_sr)



    def add_source_parent_regions(self):

        source = Source.objects.get(source_name='region_upload')

        ## INSERT PARENT REGIONS
        parent_region_lookup = {}
        parents = SourceRegion.objects.values('country','parent_name','id').distinct()

        for p in parents:

            if p['country'] != None and p['parent_name'] != None:

                office = Office.objects.get(name=p['country'])
                region_name,sr_id = p['parent_name'],p['id']

                r,created = Region.objects.get_or_create(name=region_name,defaults = \
                    {'region_code':region_name,'office':office,'source':source,
                        'source_region_id':sr_id})

                parent_region_lookup[region_name] = r.id

        return parent_region_lookup

    def source_regions_to_regions(self,parent_region_lookup):

        source = Source.objects.get(source_name='region_upload')

        src_regions = SourceRegion.objects.filter(document_id = self.document.id)

        for sr in src_regions:
            #     try:

            if sr.country is not None:
                office = Office.objects.get(name=sr.country)

                r,created = Region.objects.get_or_create(
                    name = sr.region_string,defaults = {
                    'region_code':sr.region_code,\
                    'region_type':sr.region_type,\
                    'office':office,\
                    'latitude':sr.lat,\
                    'longitude':sr.lon,\
                    'source':source,\
                    'source_region_id':sr.id,\
                    'parent_region_id':parent_region_lookup[sr.parent_name]})

                if created == 0:
                    r.parent_region_id = parent_region_lookup[sr.parent_name]
                    r.office = office
                    r.save()
