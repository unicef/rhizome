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

    transformed_df = transform_raw_file()
    transformed_file_to_datapoint(transformed_df)

def transformed_file_to_datapoint(df):

    user_id = User.objects.all()[0].id
    new_doc = Document.objects.create(
        doc_title = 'AFP_CASES',
        guid = 'AFP_CASES'
    )

    df['unique_key'] = df['index_0']
    dt = DateDocTransform(user_id, new_doc.id, df)
    dt.process_file()

    ss_id_list = SourceSubmission.objects.filter(document_id = new_doc.id)\
        .values_list('id', flat=True)

    ## source_submissions -> datapoints ##
    mr = MasterRefresh(user_id, new_doc.id)
    mr.main()

    dps = DataPoint.objects.filter(
        source_submission_id__in = ss_id_list
    )

    if len(ss_id_list) != len(df):

        print 'ss_id_list LEN \n' * 5
        print len(ss_id_list)
        print '==\n * 3'

        raise Exception('source Submissions got messed up')

    if len(dps != len(df)):

        print 'df LEN \n' * 5
        print len(df)
        print '==\n * 3'

        raise Exception('source Submissions got messed up')


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
        ('rhizome', '0015_base_dashboards'),
    ]

    operations = [
        migrations.RunPython(ingest_afp_cases)
    ]
