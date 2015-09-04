# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import os
import json
from pprint import pprint

# def ingest_geo(apps, schema_editor):
def ingest_geo():

    GEO_JSON_DIR = '/Users/john/data/geo'

    for root, dirs, files in os.walk(GEO_JSON_DIR, topdown=False):
        for name in files:
            if name.endswith('adm1.geojson'):
                file_results = process_geo_json_file((os.path.join(root, name)))

def process_geo_json_file(file_path):

    print '==%s==' % file_path

    with open(file_path) as data_file:
        data = json.load(data_file)

    pprint(data['features'][0]['properties']['ADM0_CODE'])
    pprint(data.keys())

def process_region(geo_json):

    print '--'


# class Migration(migrations.Migration):
#
#     dependencies = [
#         ('datapoints', '0012_afg_pak_regions'),
#     ]
#
#     operations = [
#         migrations.RunPython(ingest_geo)
#     ]


if __name__ == "__main__":
    ingest_geo()
