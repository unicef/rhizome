# -*- coding: utf-8 -*-
# from __future__ import unicode_literals
import os
import json

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
from rhizome.cache_meta import minify_geo_json

def process_geo_json(apps, schema_editor):

    ## IRAQ ##
    ## http://code.highcharts.com/mapdata/countries/iq/iq-all.geo.json ##

    office = Office.objects.create(name = 'Iraq')
    province_location_type_id = LocationType.objects.get(name = 'Province').id
    iraq_location_id = Location.objects.create(\
        name = 'Iraq',
        location_code = 'Iraq',
        location_type_id = LocationType.objects.get(name = 'Country').id,
        office = office
        ).id


    with open('geo_json.txt') as data_file:
        data = json.load(data_file)
        features = data['features']
        # location_name =
    for location in features:
        location_name = location['properties']['woe-name']
        location_shape = location['geometry']

        location_object = Location.objects.create(
            name = location_name,
            location_code = location_name,
            location_type_id = province_location_type_id,
            parent_location_id = iraq_location_id,
            office = office
        )

        location_shape_object = MinGeo.objects.create(
            location_id = location_object.id,
            geo_json = location_shape,
        )


    # minify_geo_json()


class Migration(migrations.Migration):

    dependencies = [
        ('rhizome', '0002_populate_initial_meta_data'),
    ]

    operations = [
        migrations.RunPython(process_geo_json),
    ]
