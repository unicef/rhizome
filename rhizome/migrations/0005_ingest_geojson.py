# -*- coding: utf-8 -*-
# from __future__ import unicode_literals
import os

import jsonfield.fields
import django.db.models.deletion
from django.db import models, migrations
from django.conf import settings
from django.db.models import get_app, get_models
from django.core.exceptions import ImproperlyConfigured

from django.core.management import call_command
from django.conf import settings
from django.db import connection
from django.db.models.loading import get_app
from StringIO import StringIO
from datetime import datetime

from rhizome.models import CacheJob
import pandas as pd
from rhizome.models import *

def process_geo_json(apps, schema_editor):

    pass
    # try:
    #     geo_json_df = pd.read_csv('geo_json.txt',delimiter = ",")
    # except IOError:
    #     return
    #
    # location_df = pd.DataFrame(list(Location.objects.all()\
    #     .values_list('id','location_code')),columns=['location_id','location_code'])
    #
    # # print 'geo_json_df'
    # # print geo_json_df[:2]
    #
    # # print '===\n' * 10
    #
    # # print 'location_df'
    # # print location_df[:2]
    #
    # merged_df = location_df.merge(geo_json_df)[['location_id','geo_json']]
    # model_df_to_data(merged_df, LocationPolygon)
    #
    # minify_geo_json()


class Migration(migrations.Migration):

    dependencies = [
        ('rhizome', '0004_populate_initial_source_data'),
    ]

    operations = [
        migrations.RunPython(process_geo_json),
    ]
