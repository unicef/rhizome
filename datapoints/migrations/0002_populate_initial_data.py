# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jsonfield.fields
import django.db.models.deletion
from django.conf import settings

import pandas as pd
from datapoints.models import IndicatorTag
from django.db.models import get_app, get_models

def populate_initial_data(apps, schema_editor):

    xl = pd.ExcelFile('initial_data.xlsx')
    all_sheets = xl.sheet_names

    datapoints_app = get_app('datapoints')

    for model in get_models(datapoints_app):

        print model._meta.db_table
        print all_sheets

        if model._meta.db_table in all_sheets:

            model_df = xl.parse(model._meta.db_table)
            model_ids = model_df_to_data(model_df,model)


def model_df_to_data(model_df,model):

    meta_ids = []

    non_null_df = model_df.where((pd.notnull(model_df)), None)
    list_of_dicts = non_null_df.transpose().to_dict()

    for row_ix, row_dict in list_of_dicts.iteritems():

        row_id = model.objects.create(**row_dict)
        meta_ids.append(row_id)

    return meta_ids


class Migration(migrations.Migration):

    dependencies = [
        ('datapoints', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(populate_initial_data),
    ]
