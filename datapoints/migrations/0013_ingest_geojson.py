# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os
import json
from pprint import pprint

from django.db import models, migrations, IntegrityError
from django.core.exceptions import ObjectDoesNotExist

from datapoints.models import Region, RegionPolygon

def ingest_geo(apps, schema_editor):

    GEO_JSON_DIR = '/Users/john/data/geo'

    for x in range(0,3):
        print '===== PROCESSING LEVEL %s ===  ' % x
        process_geo_level(x,GEO_JSON_DIR)

def process_geo_level(lvl,data_dir):

    for root, dirs, files in os.walk(data_dir, topdown=False):
        for name in files:

            if name.endswith('adm%s.geojson' % lvl):
                file_results = process_geo_json_file(\
                    (os.path.join(root, name)),lvl)

def process_geo_json_file(file_path,lvl):

    print '===== PROCESSING FILE %s ===  ' % file_path

    with open(file_path) as data_file:
        data = json.load(data_file)

    features = data['features']
    for feature in features:
        process_region(feature,lvl)

def process_region(geo_json, lvl):

    full_region_code = geo_json['properties']['ADM%s_CODE' %  lvl]

    NG_PREFIX = 'NG0010'
    RHIZOME_REGION_CODE_LEN = lvl * 2

    if full_region_code.startswith(NG_PREFIX):
        trimmed = full_region_code.replace(NG_PREFIX,'')
        region_code = trimmed[:RHIZOME_REGION_CODE_LEN]

    else:
        region_code = full_region_code

    try:
        region_id = Region.objects.get(region_code = region_code).id
    except ObjectDoesNotExist:
        print 'region_code %s DOES NOT EXISTS ' % region_code
        return

    rp, created = RegionPolygon.objects.get_or_create(
        region_id = region_id,
        defaults = {'geo_json': geo_json}
    )

    if not created:

        print  geo_json['properties']['ADM%s_CODE' %  lvl]
        print RHIZOME_REGION_CODE_LEN
        print region_code
        print ' is a dupe '


class Migration(migrations.Migration):

    dependencies = [
    # DELETE FROM django_migrations WHERE name = '0013_ingest_geojson';
        ('datapoints', '0012_afg_pak_regions'),
    ]

    operations = [
        migrations.RunPython(ingest_geo)
    ]
