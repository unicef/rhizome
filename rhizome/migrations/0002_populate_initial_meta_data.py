# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
import urllib2
import json

from django.db import models, migrations
from django.conf import settings
from django.db.models import get_app, get_models
import django.db.models.deletion

import jsonfield.fields
import pandas as pd

from rhizome.models import Location, LocationPolygon, LocationType, Office
from rhizome.cache_meta import minify_geo_json, LocationTreeCache

def populate_initial_data(apps, schema_editor):
    '''
    Here, we take an excel file that has the same schema as the database
    we lookup the approriate model and bulk insert.

    We need to ingest the data itself in the same order as the excel
    sheet otherwise we will have foreign key constraint issues.
    '''

    # process_meta_data()
    process_geo_json()

def process_meta_data():

    xl = pd.ExcelFile('migration_data/initial_data.xlsx')
    all_sheets = xl.sheet_names

    rhizome_app = get_app('rhizome')
    auth_app = get_app('auth')

    models_to_process = {}

    all_models = get_models(rhizome_app) + get_models(auth_app)

    for model in all_models:
        # iterate through the models in the rhizome app and create a lookup
        # for {'sheet_name': Model} .. for instance -> {'indicator': Indicator}

        if model._meta.db_table in all_sheets:
            models_to_process[model._meta.db_table] = model

    for sheet in all_sheets:
        # if the sheet has a cooresponding model, create a data frame out of
        # the sheet anf bulk insert the data using the model_df_to_data fn

        try:
            model = models_to_process[sheet]
            print 'processing sheet ' + sheet
            model_df = xl.parse(sheet)
            model_ids = model_df_to_data(model_df, model)
        except KeyError:
            pass

    ## once the locations are all created we need to ##
    ## cache them in the locaiton_tree table ##
    ltc = LocationTreeCache()
    ltc.main()

def process_geo_json():
    '''
    Depending on the values put in the COUNTRY_LIST, we pull shapes from
    The highcharts map repository.  This will give us shapes for admin level 1
    for the countries we specify.
    '''

    HOST = 'http://rhizome.work/api/v1/'
    for c in settings.COUNTRY_LIST:
        create_country_meta_data(c)

    minify_geo_json()

def create_country_meta_data(c):

    json_file_name = 'migration_data/geo/{0}.json'.format(c)

     # if this file has not already been saved, fetch it from the below url
    if not os.path.isfile(json_file_name):
        url = 'http://code.highcharts.com/mapdata/countries/{0}/{0}-all.geo.json'.format(c)
        response = urllib2.urlopen(url)
        data = json.loads(response.read())
        with open(json_file_name, 'w+') as outfile:
            json.dump(data, outfile)

    # create a dataframe where one rwo represents one shape #
    try:
        with open(json_file_name) as data_file:
            data = json.load(data_file)
            features = data['features']
            geo_json_df = pd.DataFrame(features)
    except IOError:
        return

    # create the country and province location types #
    country_lt, created = LocationType.objects.get_or_create(
        name = 'Country', admin_level = 0
    )
    province_lt, created = LocationType.objects.get_or_create(
        name = 'Province', admin_level = 1
    )

    # create an 'office' -- this model is legacy and should be removed #
    office_obj = Office.objects.create(
        name = c
    )

    # create the top level country #
    country_loc_object = Location.objects.create(
        name = c,
        location_code = c,
        office_id = office_obj.id,
        location_type_id = country_lt.id
    )

    for ix, row in geo_json_df.iterrows():

        # create the proivince location #
        row_properties, row_geo = row.properties, row.geometry
        province_loc_object = Location.objects.create(
            name = row_properties['name'],
            parent_location_id = country_loc_object.id,
            location_code = row.id,
            office_id = office_obj.id,
            location_type_id = province_lt.id
        )

        # create the proivince shapes #
        LocationPolygon.objects.create(
            geo_json = row_geo, location_id = province_loc_object.id
        )



def model_df_to_data(model_df, model):

    meta_ids = []

    non_null_df = model_df.where((pd.notnull(model_df)), None)
    list_of_dicts = non_null_df.transpose().to_dict()

    for row_ix, row_dict in list_of_dicts.iteritems():

        row_id = model.objects.create(**row_dict)
        meta_ids.append(row_id)

    return meta_ids


class Migration(migrations.Migration):

    dependencies = [
        ('rhizome', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(populate_initial_data),
    ]
