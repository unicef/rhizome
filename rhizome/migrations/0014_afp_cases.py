# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings

import jsonfield.fields

from rhizome.etl_tasks.transform_upload import DateDocTransform
from rhizome.etl_tasks.refresh_master import MasterRefresh
from rhizome.models import *
import pandas as pd
import datetime
import numpy as np

# psql rhizome -c "DELETE FROM django_migrations where name = '0016_afp_cases';"
def ingest_afp_cases(apps, schema_editor):

    indicator_ids = update_indicators_and_dps()
    transformed_df = transform_raw_file()
    transformed_file_to_datapoint(transformed_df, indicator_ids)

def transformed_file_to_datapoint(df, indicator_ids):
    user_id = 1
    new_doc, created = Document.objects.get_or_create(
        doc_title = 'AFP_CASES',
        guid = 'AFP_CASES'
    )

    df['unique_key'] = df['geocode'] + df['data_date'].map(str)
    dt = DateDocTransform(user_id, new_doc.id, df)
    sss = dt.process_file()
    dt.upsert_source_object_map()

    ss_id_list = SourceSubmission.objects.filter(document_id = new_doc.id)\
    #     .values_list('id', flat=True)
    # print 'ss_id_list'
    # print ss_id_list
    ## source_submissions -> datapoints ##
    # mr = MasterRefresh(user_id, new_doc.id)
    # mr.main()

    # MAJOR HACK: We're just going to create the datapoints on the fly for now. No SourceSubmissions
    indicator_name_to_id ={}
    for indicator_id in indicator_ids:
        ind = Indicator.objects.get(id=indicator_id)
        indicator_name_to_id[ind.name] = indicator_id

    dp_batch = []
    total_num_non_zeros = 0
    for ix, row in df.iterrows():
        for indicator_name, indicator_id in indicator_name_to_id.iteritems():
            val = row[indicator_name]
            location_id = Location.objects.get(location_code = row.geocode).id
            data_date = datetime.datetime.strptime(row['data_date'], '%d-%m-%Y').strftime('%Y-%m-%d')

            if val > 0:
                dp_obj = DataPoint(**{
                    'indicator_id':indicator_id,
                    'data_date':data_date,
                    'location_id':location_id,
                    'cache_job_id':-1,
                    # MAJOR HACK:::
                    'source_submission_id': ss_id_list[0].id,
                    'value': val
                })
                dp_batch.append(dp_obj)
                total_num_non_zeros += 1

    DataPoint.objects.bulk_create(dp_batch)

    dps = DataPoint.objects.filter(
        indicator_id__in = indicator_ids
    )
    # if len(ss_id_list) != len(df):
    #     raise Exception('source Submissions not ingested properly')

    # count the number of dps

    if len(dps) != total_num_non_zeros:
        raise Exception('datapoitns not ingested properly')

def transform_raw_file():

    input_df = pd.read_csv('migration_data/AFP.afg.2014_2016.csv')
    input_df['data_date'] = input_df["Day"].map(str) + '-' + input_df["Month"]\
        .map(str) + '-' + input_df['Year'].map(str)
    input_df = input_df[['geocode','data_date','Doses']]

    zero_dose_df = input_df[input_df['Doses'] == 0]
    zero_dose_df['Doses'] = 1
    one_to_three_dose_df = input_df[input_df['Doses'].isin([1,2,3])]
    one_to_three_dose_df['Doses'] = 1
    four_to_six_dose_df = input_df[input_df['Doses'].isin([4,5,6])]
    four_to_six_dose_df['Doses'] = 1
    seven_plus_dose_df = input_df[input_df['Doses'] > 6]
    seven_plus_dose_df['Doses'] = 1

    first_df = zero_dose_df.merge(one_to_three_dose_df, \
        how='outer',on=['geocode','data_date']).reset_index()
    first_df.columns = ['index','geocode','data_date','Zero Dose','1-3 Dose']

    second_df = first_df.merge(four_to_six_dose_df, \
        how='outer',on=['geocode','data_date']).reset_index()
    second_df.columns = ['index_0','index_1','geocode','data_date',\
        'Zero Dose','1-3 Dose','4-6 Dose']

    final_df = second_df.merge(seven_plus_dose_df,\
        how='outer',on=['geocode','data_date'])

    final_df.columns = ['index_0','index_1','geocode','data_date',\
        'Number of Unvaccinated Non Polio AFP Cases',\
        'Number of Non Polio AFP cases vaccinated 1-3 doses',\
        'Number of Non Polio AFP cases vaccinated 4-6 doses',\
        'Number of Non Polio AFP cases vaccinated 7+ doses']
    
    final_df = final_df.replace(np.nan, 0)
    final_df = final_df.groupby(['geocode', 'data_date'], as_index = False).sum()
    totals_column = final_df.apply(add_total_cases, axis=1)
    final_df['Number of reported Non Polio AFP cases'] = totals_column
    return final_df

def add_total_cases(x):
    total = x['Number of Unvaccinated Non Polio AFP Cases']+\
    x['Number of Non Polio AFP cases vaccinated 1-3 doses']+\
    x['Number of Non Polio AFP cases vaccinated 4-6 doses']+\
    x['Number of Non Polio AFP cases vaccinated 7+ doses']
    return total

def update_indicators_and_dps():

    # get or create indicators
    indicator_names = ['Number of reported Non Polio AFP cases',\
        'Number of Unvaccinated Non Polio AFP Cases',\
        'Number of Non Polio AFP cases vaccinated 1-3 doses',\
        'Number of Non Polio AFP cases vaccinated 4-6 doses',\
        'Number of Non Polio AFP cases vaccinated 7+ doses']

    indicator_ids =[]
    for indicator_name in indicator_names:
        indicator = Indicator.objects.get_or_create(name=indicator_name,\
            short_name = indicator_name,
            description = indicator_name,
            data_format = 'int')
        indicator_ids.append(indicator[0].id)
    # print 'indicator_ids'
    # print indicator_ids
    # delete any existing dps for those indicators
    for indicator_id in indicator_ids:
        DataPoint.objects.filter(indicator=indicator_id).delete()
        DataPointComputed.objects.filter(indicator=indicator_id).delete()
        DocDataPoint.objects.filter(indicator=indicator_id).delete()
    return indicator_ids

class Migration(migrations.Migration):

    dependencies = [
        ('rhizome', '0013_ingest_polio_cases'),
    ]

    operations = [
        migrations.RunPython(ingest_afp_cases)
    ]
