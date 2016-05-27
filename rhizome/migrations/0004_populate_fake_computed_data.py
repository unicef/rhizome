# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import jsonfield.fields
import django.db.models.deletion
from django.db import models, migrations
from django.conf import settings
from django.db.models import get_app, get_models

from pandas import DataFrame
from random import randint, random

from rhizome.cache_meta import minify_geo_json, LocationTreeCache
from rhizome.models import Location, Indicator, Campaign, DataPointComputed
from rhizome.models import Document, DocumentDetail, DocDetailType
from rhizome.etl_tasks.transform_upload import DocTransform
from rhizome.etl_tasks.refresh_master import MasterRefresh
from rhizome.agg_tasks import AggRefresh


def pass_fn(apps, schema_editor):
    pass


def populate_fake_dwc_data(apps, schema_editor):
    '''
    This migration will be removed, and we will prefer the "initial_meta_data"
    ingetion and rely on DocTransform, RefreshMaster and AggRefresh in order
    to populate the datapoint_with_computed table.. however, so that we can have
    ample data to show on the dashboards, i will take the cartesion product
    of campaigns, indicators and selected locations ( provinces and LPDS )
    and dump that data in to datapoint_with_computed.

    It would be nice to somehow set this up so that when a new developer spins
    up the app locally.. they can populate this 'fake' data.

    Maybe somethign like.. if SETTINGS.debug = True, then ingest fake data.
    '''

    document = Document.objects.create(doc_title='Initial FAKE Data Load')

    ind_df = DataFrame(list(Indicator.objects.all()
                            .values_list('id', 'short_name', 'data_format')), columns=['indicator_id', 'short_name', 'data_format'])

    campaign_df = DataFrame(list(Campaign.objects.all()
                                 .values_list('id', 'name')), columns=['campaign_id', 'campaign_name'])

    country_id_list = list(Location.objects
                           .filter(location_type_id=1)
                           .values_list('id', flat=True))

    location_df = DataFrame(list(Location.objects
                                 .filter(location_type_id__lte=3)
                                 .values_list('id', 'name')), columns=['location_id', 'name'])

    ind_df['join_col'] = 1
    campaign_df['join_col'] = 1
    location_df['join_col'] = 1

    first_merged_df = ind_df.merge(campaign_df, on='join_col')
    final_merged_df = first_merged_df.merge(location_df, on='join_col')

    upsert_df_data(final_merged_df, document.id)


def upsert_df_data(df, document_id):

    dwc_batch = []
    for ix, row in df.iterrows():

        if row.data_format == 'pct':
            rand_val = random()

        if row.data_format == 'bool':
            rand_val = randint(0, 1)

        if row.data_format == 'int':
            rand_val = randint(0, 1000)

        dwc_obj = DataPointComputed(**{
            'indicator_id': row.indicator_id,
            'campaign_id': row.campaign_id,
            'location_id': row.location_id,
            'cache_job_id': -1,
            'document_id': document_id,
            'value': rand_val
        })

        dwc_batch.append(dwc_obj)

    DataPointComputed.objects.all().delete()
    DataPointComputed.objects.bulk_create(dwc_batch)


class Migration(migrations.Migration):

    dependencies = [
        ('rhizome', '0003_populate_initial_source_data'),
    ]

    operations = [
        migrations.RunPython(populate_fake_dwc_data),
    ]
