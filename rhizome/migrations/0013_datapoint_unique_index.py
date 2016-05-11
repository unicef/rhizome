# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from rhizome.models import DataPoint, Campaign
from pandas import DataFrame
import math
import pandas as pd

# helper function for upsert_unique_indices
def add_unique_index(x):
    if x['campaign_id'] and not math.isnan(x['campaign_id']):
        x['unique_index'] = str(x['location_id']) + '_' + str(x['indicator_id']) + '_' + str(int(x['campaign_id']))
    else:
        x['unique_index'] = str(x['location_id']) + '_' + str(x['indicator_id']) + '_' + str(pd.to_datetime(x['data_date'], utc=True))
    return x

def upsert_unique_indices(apps, schema_editor):
    datapoint_values_list = ['id','created_at','indicator_id','location_id','campaign_id','data_date']
    historical_dps = DataFrame(list(DataPoint.objects.filter(unique_index = -1)\
        .values_list('id','created_at','indicator_id','location_id','campaign_id','data_date')), columns=datapoint_values_list)
    # create the unique index
    historical_dps = historical_dps.apply(add_unique_index, axis=1)

    # group by and max on created at, get the most recent upload
    historical_dps = historical_dps.sort("created_at", ascending=False).groupby("unique_index", as_index=False).first()

    # get the ids into a list and select them
    dps_to_update = DataPoint.objects.filter(id__in=list(historical_dps['id']))
    print 'dps to update'
    print len(dps_to_update)
    # then run a query and update each
    for dp in dps_to_update:
        unique_index = historical_dps[historical_dps['id'] == dp.id].iloc[0]['unique_index']
        dp.unique_index = unique_index
        dp.save()

    # delete all the other duplicates
    dps_to_delete = DataPoint.objects.filter(unique_index=-1)
    print 'dps_to_delete'
    print len(dps_to_delete)
    dps_to_delete.delete()



class Migration(migrations.Migration):

    dependencies = [
        ('rhizome', '0012_reset_sql_sequence'),
    ]

    operations = [
        migrations.AddField(
            model_name='datapoint',
            name='unique_index',
            field=models.CharField(default=-1, max_length=255),
        ),
        migrations.AddField(
            model_name='historicaldatapointentry',
            name='unique_index',
            field=models.CharField(default=-1, max_length=255, db_index=True),
        ),
        migrations.RunPython(upsert_unique_indices),

    ]
