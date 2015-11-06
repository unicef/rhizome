# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os
import json

from django.db import models, migrations, IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from django.core.exceptions import ValidationError
from titlecase import titlecase

from datapoints.models import Location, LocationPolygon, LocationType
from source_data.models import SourceObjectMap


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
        process_location(feature,lvl)

def process_location(geo_json, lvl):
    '''
    Sorry this is a hack just trying to get the site working.. not proud of this
    code but the shapes on the dashboards look good :).

    This should be handled via the source data uploader app.. that is i should
    be able to upldoad new geojson / shp files.
    '''

    err = None

    # NG001034001000000000 # binji
    # NG001034001000000000 # binji
    # NG001034010000000000 # binji ( Inside Monitoring Code )

    location_code = geo_json['properties']['ADM%s_CODE' %  lvl]
    location_name = titlecase(geo_json['properties']['ADM%s_NAME' %  lvl])

    location_type = LocationType.objects.get(admin_level = lvl)

    try:
        location_id = Location.objects.get(location_code = location_code).id
    except ObjectDoesNotExist:
        location_id = None

    if not location_id:
        try:
            location_id = Location.objects.get(name = location_name,\
                location_type_id = location_type.id).id
        except ObjectDoesNotExist:
            location_id = None

    if not location_id:
        location_name_with_type = '%s (%s)' % (location_name, location_type.name)
        try:
            location_id = Location.objects.get(name = location_name_with_type,\
                location_type_id = location_type.id).id
        except ObjectDoesNotExist:
            location_id = None

    if not location_id:
        err, location_id = create_new_location(lvl, geo_json, location_name_with_type)

    if err:
        return

    try:
        rp, created = LocationPolygon.objects.get_or_create(
            location_id = location_id,
            defaults = {'geo_json': geo_json}
        )
    except ValidationError:
        print 'ValidationError!!'

    ## now create a mapping if it doesnt exists already ##
    som_obj, created = SourceObjectMap.objects.get_or_create(
        content_type = 'location',
        source_object_code = location_code,
        defaults = {'mapped_by_id':1,'master_object_id':location_id}
    )

def create_new_location(lvl, geo_json, location_name_with_type):

    if lvl == 0:
        return 'Not Creating Lvl one...', None

    parent_lvl = lvl - 1

    location_code = geo_json['properties']['ADM%s_CODE' %  parent_lvl]

    try:
        parent_location = Location.objects.get(location_code = location_code)
    except ObjectDoesNotExist:
        err_msg = 'Cant Find parent location: %s'  % location_code
        return err_msg, None

    new_location = Location.objects.create(
        location_code = geo_json['properties']['ADM%s_CODE' %  lvl],
        name = location_name_with_type,
        location_type_id = lvl + 1,
        slug =  geo_json['properties']['ADM%s_CODE' %  lvl],
        parent_location_id = parent_location.id,
        office_id = parent_location.office_id,
    )

    return None, new_location.id


class Migration(migrations.Migration):

    dependencies = [
    # DELETE FROM django_migrations WHERE name = '0013_ingest_geojson';
        ('datapoints', '0011_odk_and_seed_campaign_maps'),
    ]

    operations = [
        migrations.RunPython(ingest_geo)
    ]
