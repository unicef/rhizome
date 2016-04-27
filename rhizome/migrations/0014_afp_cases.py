# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings

import jsonfield.fields

from rhizome.etl_tasks.transform_upload import DateDocTransform
from rhizome.etl_tasks.refresh_master import MasterRefresh
from rhizome.models import *
import pandas as pd

def ingest_afp_cases(apps, schema_editor):

    ingest_afp_case_meta()
    transformed_df = transform_raw_file()
    transformed_file_to_datapoint(transformed_df)

def ingest_afp_case_meta():

    indicator_names = ['Zero Dose','1-3 Dose','4-6 Dose','7+ Dose']
    for ind in indicator_names:
        ind_id = Indicator.objects.create(
            name = 'AFP Case - ' + ind,
            short_name = ind,
            description = ind,
            data_format = 'int'
        ).id
        som_obj = SourceObjectMap.objects.create(
            master_object_id = ind_id,
            content_type = 'indicator',
            source_object_code = ind
        )

def transformed_file_to_datapoint(df):

    user_id = User.objects.all()[0].id
    new_doc, created = Document.objects.get_or_create(
        doc_title = 'AFP_CASES',
        guid = 'AFP_CASES'
    )

    df['unique_key'] = df['geocode'] + df['data_date'].map(str)
    dt = DateDocTransform(user_id, new_doc.id, df)
    dt.process_file()
    dt.upsert_source_object_map()

    ss_id_list = SourceSubmission.objects.filter(document_id = new_doc.id)\
        .values_list('id', flat=True)

    ## source_submissions -> datapoints ##
    mr = MasterRefresh(user_id, new_doc.id)
    mr.main()

    dps = DataPoint.objects.filter(
        source_submission_id__in = ss_id_list
    )

    # if len(ss_id_list) != len(df):
    #     raise Exception('source Submissions not ingested properly')

    # if len(dps != len(df)):
    #     raise Exception('datapoitns not ingested properly')

def transform_raw_file():

    input_df = pd.read_csv('AFP.afg.2014_2016.csv')
    input_df['data_date'] = input_df["Day"].map(str) + '-' + input_df["Month"]\
        .map(str) + '-' + input_df['Year'].map(str)
    input_df = input_df[['geocode','data_date','Doses']]

    zero_dose_df = input_df[input_df['Doses'] == 0]
    one_to_three_dose_df = input_df[input_df['Doses'].isin([1,2,3])]
    four_to_six_dose_df = input_df[input_df['Doses'].isin([4,5,6])]
    seven_plus_dose_df = input_df[input_df['Doses'] > 6]


    first_df = zero_dose_df.merge(one_to_three_dose_df, \
        how='right',on=['geocode','data_date']).reset_index()
    first_df.columns = ['index','geocode','data_date','Zero Dose','1-3 Dose']

    second_df = first_df.merge(four_to_six_dose_df, \
        how='right',on=['geocode','data_date']).reset_index()
    second_df.columns = ['index_0','index_1','geocode','data_date',\
        'Zero Dose','1-3 Dose','4-6 Dose']

    final_df = second_df.merge(seven_plus_dose_df,\
        how='right',on=['geocode','data_date'])

    final_df.columns = ['index_0','index_1','geocode','data_date',\
        'Zero Dose','1-3 Dose','4-6 Dose','7+ Dose']

    return final_df
    # disitct_geo_code_date_df = input_df[['geocode','data_date']].drop_duplicates()
    #
    # if len(final_df) != len(disitct_geo_code_date_df):
    #     raise Exception('this did not work')

class Migration(migrations.Migration):

    dependencies = [
        ('rhizome', '0013_ingest_polio_cases'),
    ]

    operations = [
        migrations.RunPython(ingest_afp_cases)
    ]
