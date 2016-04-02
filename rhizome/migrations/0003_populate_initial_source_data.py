# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import jsonfield.fields
import django.db.models.deletion
from django.db import models, migrations
from django.conf import settings
from django.db.models import get_app, get_models

import pandas as pd

from rhizome.cache_meta import minify_geo_json, LocationTreeCache
from rhizome.models import Location, LocationPolygon, Indicator, Campaign,\
    LocationType
from rhizome.models import Document, DocumentDetail, DocDetailType
from rhizome.etl_tasks.transform_upload import DocTransform
from rhizome.etl_tasks.refresh_master import MasterRefresh
from rhizome.agg_tasks import AggRefresh


def populate_source_data(apps, schema_editor):
    '''
    Here, we take an excel file that has the same schema as the database
    we lookup the approriate model and bulk insert.

    We need to ingest the data itself in the same order as the excel
    sheet otherwise we will have foreign key constraint issues.
    '''
    odk_form_sheet_name = 'source-data_idp_odk_form'
    xl = pd.ExcelFile('initial_data.xlsx')

    source_sheet_df = xl.parse(odk_form_sheet_name)

    mdf = MetaDataGenerator(source_sheet_df)
    mdf.main()


class MetaDataGenerator:

    def __init__(self, source_sheet_df):

        self.source_sheet_df = source_sheet_df
        self.odk_file_map = {
            'date_column': 'RRM_Distribution/date_assessdistro',
            'lat_column': '',
            'lon_column': '',
            'province_column': '',
            'district_column': '',
            'city_column': ''
        }

    def main(self):

        self.build_meta_data_from_source()
        self.process_source_sheet()

    def build_meta_data_from_source(self):

        indicator_ids = self.build_indicator_meta()
        # campaign_ids = self.build_campaign_meta()
        # location_ids = self.build_location_meta()

    def build_indicator_meta(self):

        batch = []

        df_columns = self.source_sheet_df.columns
        config_columns = self.odk_file_map.values()
        indicators = df_columns #set(df_columns).intersection(set(config_columns))

        for ind in indicators:

            print '=ind='
            print ind

            batch.append(Indicator(**{
                'name':ind,
                'short_name':ind,
                'description':ind
            }))

        Indicator.objects.all().delete()
        Indicator.objects.bulk_create(batch)

        print '=made indicators=\n' * 5
        print Indicator.objects.all().values()

    def build_campaign_meta(self):

        date_column = self.odk_file_map['date_column']

        all_date_df = pd.DataFrame(self.source_sheet_df[date_column], columns = [date_column])

        all_date_df['week_of_month'] = all_date_df[date_column]\
            .apply(lambda x: x.weekofyear)


    def build_location_meta(self):

        country_name = 'Iraq'

        province_df = pd.DataFrame(self.odk_file_map['province_column']\
            .unique())

        self.process_location_df(province_df, 'Province')

        district_df = pd.DataFrame(self.odk_file_map['district_column']\
            .unique())
        city_df = pd.DataFrame(self.odk_file_map['city_column'])


        all_date_df = pd.DataFrame(self.source_sheet_df[date_column], columns = [date_column])

        all_date_df['week_of_month'] = all_date_df[date_column]\
            .apply(lambda x: x.weekofyear)

    def process_location_df(self, province_df, admin_level):

        batch = []
        for ix, loc in province_df.iterrows():
            batch.append(Location(**{
                'name': loc.location_name,
                'code': loc.location_code,
                # 'parent_location_type_id'
            }))

        Location.objects.filter(location_type__name=admin_level).delete()
        Location.objecst.bulk_create(batch)

    def model_df_to_data(model_df,model):

        meta_ids = []

        non_null_df = model_df.where((pd.notnull(model_df)), None)
        list_of_dicts = non_null_df.transpose().to_dict()

        for row_ix, row_dict in list_of_dicts.iteritems():

            row_id = model.objects.create(**row_dict)
            meta_ids.append(row_id)

        return meta_ids


    def process_source_sheet(self):

        user_id = -1

        sheet_name = 'initial_source_data'
        # file_loc = settings.MEDIA_ROOT + sheet_name
        saved_csv_file_location = settings.MEDIA_ROOT + sheet_name + '.csv'
        self.source_sheet_df.to_csv(saved_csv_file_location)
        doc_file_text = sheet_name + '.csv'

        new_doc = Document.objects.create(
            doc_title = doc_file_text,
            guid = 'test',
            docfile=doc_file_text
        )

        create_doc_details(new_doc.id)

        ## document -> source_submissions ##
        dt = DocTransform(user_id, new_doc.id)
        dt.main()

        ## source_submissions -> datapoints ##
        mr = MasterRefresh(user_id, new_doc.id)
        mr.main()

        ## datapoints -> computed datapoints ##
        ar = AggRefresh()

def create_doc_details(doc_id):

    doc_detail_types = ['uq_id_column', 'date_column', 'location_column']

    for dd_type in doc_detail_types:
        DocumentDetail.objects.create(
            document_id = doc_id,
            doc_detail_type_id = DocDetailType.objects.get(name = dd_type).id,
            doc_detail_value = dd_type ## this implies that the source columns
                                        ## are named with the above convention
        )

class Migration(migrations.Migration):

    dependencies = [
        ('rhizome', '0002_populate_initial_meta_data'),
    ]

    operations = [
        migrations.RunPython(populate_source_data),
    ]
