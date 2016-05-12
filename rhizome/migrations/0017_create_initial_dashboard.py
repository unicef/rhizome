# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import jsonfield.fields
import django.db.models.deletion
from django.db import models, migrations
from django.conf import settings
from django.db.models import get_app, get_models
from django.db.utils import IntegrityError
import pandas as pd

from rhizome.cache_meta import minify_geo_json, LocationTreeCache
from rhizome.models import Location, LocationPolygon, Indicator, Campaign,\
    LocationType, Office, CampaignType, IndicatorTag, SourceObjectMap,\
    DataPointComputed

from rhizome.models import *
from rhizome.etl_tasks.transform_upload import DateDocTransform
from rhizome.etl_tasks.refresh_master import MasterRefresh
from rhizome.agg_tasks import AggRefresh

from pprint import pprint


def initial_visualization(apps, schema_editor):
    '''
    '''

    # psql iraq -c "TRUNCATE TABLE custom_chart; DELETE from django_migrations where name like '%initial_dashboard%';"

    chart_1 = CustomChart.objects.create(
        title = 'RRM Kits Distrbuted',
        chart_json = {
            "groupByTime":"all_time",
            "end_date":"2016-05-12",
            "indicator_ids":[4],
            "type_params":{},
            "campaign_ids":[1],
            "groupBy":"indicator",
            "location_ids":[1],
            "type":"BubbleMap",
            "start_date":"2015-05-12",
            "indicator_colors":{"4":"ffffb3"}
        },
        uuid= '7e65fbd2-6cf3-43e8-8019-17cbdcd3cf46'
    )

    chart_2 = CustomChart.objects.create(
        title = 'Families Seen',
        chart_json = {
            "groupByTime":"all_time",
            "end_date":"2016-05-12",
            "indicator_ids":[3],
            "type_params":{},
            "campaign_ids":[1],
            "groupBy":"indicator",
            "location_ids":[1],
            "type":"BubbleMap",
            "start_date":"2015-05-12",
            "indicator_colors":{"3":"#ffb3e6"}
        },
        uuid= '7e65fbd2-6cf3-43e8-8019-17cbdcd3cf4z'
    )

    chart_3 = CustomChart.objects.create(
        title = 'Singles Seen',
        chart_json = {
            "groupByTime":"all_time",
            "end_date":"2016-05-12",
            "indicator_ids":[2],
            "type_params":{},
            "campaign_ids":[1],
            "groupBy":"indicator",
            "location_ids":[1],
            "type":"BubbleMap",
            "start_date":"2015-05-12",
            "indicator_colors":{"2":"#6699ff"}
        },
        uuid= '7e65fbd2-6cf3-43e8-8019-17cbdcd3cf4y'
    )

    chart_4 = CustomChart.objects.create(
        title = 'Plumpy Bars Distributed',
        chart_json = {
            "groupByTime":"all_time",
            "end_date":"2016-05-12",
            "indicator_ids":[2],
            "type_params":{},
            "campaign_ids":[1],
            "groupBy":"indicator",
            "location_ids":[1],
            "type":"BubbleMap",
            "start_date":"2015-05-12",
            "indicator_colors":{"1":"#ff9999"}
        },
        uuid= '7e65fbd2-6cf3-43e8-8019-17cbdcd3cf4x'
    )

    # dashboard = CustomDashboard.objects.create(
    #     rows= [
    #         {"layout":1,
    #             "charts":[
    #                 "7e65fbd2-6cf3-43e8-8019-17cbdcd3cf46"
    #         ]},
    #     ],
    #     title = 'IDP Dashboard'
    # )

class Migration(migrations.Migration):

    dependencies = [
        ('rhizome', '0016_populate_initial_source_data'),
    ]

    operations = [
        migrations.RunPython(initial_visualization),
        ]
