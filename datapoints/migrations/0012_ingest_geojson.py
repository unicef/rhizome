# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os
import json

from django.db import models, migrations, IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from django.core.exceptions import ValidationError

from datapoints.models import Location, LocationPolygon

def ingest_geo(apps, schema_editor):

    GEO_JSON_DIR = '/Users/john/data/geo'

    for x in range(0,3):
        process_geo_level(x,GEO_JSON_DIR)

def process_geo_level(lvl,data_dir):

    for root, dirs, files in os.walk(data_dir, topdown=False):
        for name in files:

            if name.endswith('adm%s.geojson' % lvl):
                file_results = process_geo_json_file(\
                    (os.path.join(root, name)),lvl)

def process_geo_json_file(file_path,lvl):

    print '\n PROCESSING: %s'  % file_path

    with open(file_path) as data_file:
        data = json.load(data_file)

    features = data['features']
    for feature in features:
        process_location(feature,lvl)

def process_location(geo_json, lvl):

    # NG001034001000000000 # binji
    # NG001034001000000000 # binji
    # NG001034010000000000 # binji ( Inside Monitoring Code )

    location_code = geo_json['properties']['ADM%s_CODE' %  lvl]
    location_name = geo_json['properties']['ADM%s_NAME' %  lvl]


    try:
        location_id = Location.objects.get(location_code = location_code).id
        print 'FOUND IT: %s ' %  Location.objects.get(location_code = location_code).name
    except ObjectDoesNotExist:
        print ' ===== CAN NOT FIND %s' % location_name
        return

    try:
        rp, created = LocationPolygon.objects.get_or_create(
            location_id = location_id,
            defaults = {'geo_json': geo_json}
        )
    except ValidationError:
        print 'ValidationError!!'

class Migration(migrations.Migration):

    dependencies = [
    # DELETE FROM django_migrations WHERE name = '0013_ingest_geojson';
        ('datapoints', '0011_odk_and_seed_campaign_maps'),
    ]

    operations = [
        migrations.RunPython(ingest_geo)
    ]
