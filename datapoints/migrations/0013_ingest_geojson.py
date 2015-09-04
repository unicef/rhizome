# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os
import json
from pprint import pprint

from django.db import models, migrations
from django.core.exceptions import ObjectDoesNotExist

from datapoints.models import Region, RegionPolygon

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

    with open(file_path) as data_file:
        data = json.load(data_file)

    features = data['features']
    for feature in features:
        process_region(feature,lvl)

def process_region(geo_json, lvl):

    region_code = geo_json['properties']['ADM%s_CODE' %  lvl]

    try:
        region_id = Region.objects.get(region_code = region_code).id
    except ObjectDoesNotExist:
        return

    rp = RegionPolygon.objects.create(
        region_id = region_id,
        geo_json = geo_json
    )

class Migration(migrations.Migration):

    dependencies = [
    # DELETE FROM django_migrations WHERE name = '0013_ingest_geojson';
        ('datapoints', '0012_afg_pak_regions'),
    ]

    operations = [
        migrations.RunPython(ingest_geo)
    ]
