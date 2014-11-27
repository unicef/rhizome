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

        essential_columns = ['name','code','parent_name','region_type','country']
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

        for row in valid_df.iterrows():
            row_data = row[1]
            parent_regions.append(row_data.parent_name)

            try:
                SourceRegion.objects.create(

                    region_string = row_data.region_name,\
                    region_code = row_data.code,\
                    parent_name = row_data.parent_name,\
                    region_type = row_data.region_type,\
                    country = row_data.country,\
                    document_id = self.document.id,\
                    source_guid = str(row_data.region_name) + ' - '  + str(row_data.code)
                )
            except IntegrityError as err:
                print err

        distinct_parent_regions = list(set(parent_regions))

        for reg in distinct_parent_regions:

            try:
                SourceRegion.objects.create(
                    region_string = reg,\
                    region_code = reg,\
                    document_id = self.document.id
                )
            except IntegrityError as err:
                print err


    def source_regions_to_regions(self):

        src_regions = SourceRegion.objects.filter(document_id = self.document.id)
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

                print r.id

            # print p_id


        # for sr in src_regions:
        #
        #     try:
        #         parent_region = Region.objects.get(name=sr.parent_name)
        #         office = Office.objects.get(name=sr.country)
        #
        #     except ObjectDoesNotExist as err:
        #         parent_region, office = None, None
        #
        #     try:
        #         Region.objects.create(
        #             name = sr.region_string,\
        #             region_code = sr.region_code,\
        #             region_type = sr.region_type,\
        #             office = office,\
        #             latitude = sr.lat,\
        #             longitude = sr.lon,\
        #             source = source,\
        #             source_guid = sr.source_guid,\
        #             parent_region = parent_region
        #         )
        #     except IntegrityError as err:
        #         r = Region.objects.get(name=sr.region_string)
        #         r.parent_region = parent_region
        #         r.office = office
        #         r.save()
        #     except ValueError:
        #         pass
