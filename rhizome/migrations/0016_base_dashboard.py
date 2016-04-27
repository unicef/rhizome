# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings

import jsonfield.fields

from rhizome.etl_tasks.transform_upload import DateDocTransform
from rhizome.etl_tasks.refresh_master import MasterRefresh
from rhizome.models import *
import pandas as pd

def ingest_base_dashboards(apps, schema_editor):

# psql rhizome -c "TRUNCATE TABLE custom_dashboard CASCADE;
# TRUNCATE TABLE custom_chart CASCADE;

# run this in bash when you need to run the migration again:
# psql rhizome -c "DELETE FROM django_migrations where name = '0016_base_dashboard';"

    CustomChart.objects.all().delete()
    CustomDashboard.objects.all().delete()

    ingest_situational()
    ingest_pre_campaign()
    ingest_intra_campaign()
    ingest_post_campaign()

def get_indicators_by_tag_name(tag_name):

    print 'get_indicators_by_tag_name' * 3
    print tag_name
    print '====\n' * 3
    tag_id = IndicatorTag.objects.get(tag_name = tag_name).id

    return Indicator.objects.filter(indicatortotag__indicator_tag_id = tag_id)\
        .values_list('id', flat=True)


def ingest_situational():

    chart_1 = CustomChart.objects.create(
        title = 'Polio Cases - 2014 to Present',
        chart_json =    {
            "end_date":"2016-03-01",
            "indicator_ids": [ Indicator.objects.get(name = 'Polio Cases').id ] ,
            "campaign_ids":[5],
            "location_ids":[1],
            "type":"BubbleMap",
            "start_date":"2015-11-01"
        },
        uuid= '7e65fbd2-6cf3-43e8-8019-17cbdcd3cf46'
    )

    chart_2 = CustomChart.objects.create(
        title = 'Annual Case Table',
        chart_json = {
            "end_date":"2016-03-01",
            "indicator_ids":[
                Indicator.objects.get(name = "Polio Cases").id,
                Indicator.objects.get(name = "Date of Latest Polio Case").id,
                Indicator.objects.get(name = "# of Infected Districts").id,
                Indicator.objects.get(name = "# of Infected Provinces").id],
            "campaign_ids":[5],
            "location_ids":[1],
            "type":"RawData",
            "start_date":"2015-11-01",
            "groupByTime":"year",
            "groupBy":"location"
        },
        uuid = '5599c516-d2be-4ed0-ab2c-d9e7e5fe33be'
    )

    chart_3 = CustomChart.objects.create(
        title = 'Immunity Profile',
        chart_json = {
            "start_date":"2016-03-01",
            "end_date":"2016-03-01",
            "indicator_ids":[
                Indicator.objects.get(short_name="Zero Dose").id,
                Indicator.objects.get(short_name="1-3 Dose").id,
                Indicator.objects.get(short_name="4-6 Dose").id,
                Indicator.objects.get(short_name="7+ Dose").id,
            ],
            "campaign_ids":[5],
            "location_ids":[1],
            "groupBy":"indicator",
            "type":"StackedPercentColumnChart"
        },
        uuid = '1874bf4a-140a-420a-a3e2-0d29430786c0'
    )

    # chart_4 = CustomChart.objects.create(
    #     title = 'Non Polio AFP Rate and Adequate Specimens',
    #     chart_json ={
    #         "end_date":"2016-03-01",
    #         "indicator_ids":[Indicator.objects.get(name="Non Polio AFP Rate").id,
    #         Indicator.objects.get(name="Percentage of Adequate Specimen ").id
    #         ],
    #         "campaign_ids":[5],
    #         "location_ids":[1],
    #         "type":"ColumnChart",
    #         "start_date":"2015-11-01"
    #     },
    #     uuid = '4499af7d-bbcc-41a6-81cf-b2071d79ce55'
    # )
    #
    #
    # chart_5 = CustomChart.objects.create(
    #     title = 'Inaccessible Children',
    #     chart_json = {
    #         "end_date":"2016-03-01",
    #         "indicator_ids":[Indicator.objects.get(short_name="Number Inaccessible Children").id],
    #         "campaign_ids":[5],
    #         "location_ids":[1],
    #         "type":"ColumnChart",
    #         "start_date":"2015-11-01"
    #     },
    #     uuid = '8fd8f0e2-327d-4cf6-ba11-0252e6580f38'
    # )
    #
    # chart_6 = CustomChart.objects.create(
    #     title = 'Environmental Results',
    #     chart_json = {
    #         "end_date":"2016-03-01",
    #         "indicator_ids":[Indicator.objects.get(short_name="Number of Environmental Samples collected").id,
    #         Indicator.objects.get(short_name="Number of Environmental Samples with Negative result").id,
    #         Indicator.objects.get(short_name="Number of Environmental Samples with Positive result").id,
    #         Indicator.objects.get(short_name="Number of Environmental Samples with result pending in Lab").id],
    #         "campaign_ids":[5],
    #         "location_ids":[1],
    #         "type":"ColumnChart",
    #         "start_date":"2015-11-01"
    #     },
    #     uuid = '6f2efd2a-dd9f-4bcc-8652-7a622ebfc047'
    # )
    #
    #
    # chart_7 = CustomChart.objects.create(
    #     title = 'Preparatory Indicators',
    #     chart_json = {
    #         "end_date":"2016-03-01"
    #         ,"indicator_ids":get_indicators_by_tag_name('Preparatory Indicators'),
    #         "campaign_ids":[5],
    #         "location_ids":[1],
    #         "type":"RawData",
    #         "start_date":"2015-11-01"
    #     },
    #     uuid = 'df3fdb84-5721-456c-8468-c4605842c7d6'
    # )
    #
    # chart_8 = CustomChart.objects.create(
    #     title = 'Campaign Analysis',
    #     chart_json = {
    #         "end_date":"2016-03-01",
    #         "indicator_ids":get_indicators_by_tag_name('Campaign Analysis'),
    #         "campaign_ids":[5],
    #         "location_ids":[1],
    #         "type":"RawData",
    #         "start_date":"2015-11-01"
    #     },
    #     uuid = '30fe1ee9-8e82-4caf-8f3b-eaf3b4cf43a9'
    # )
    #
    # chart_9 = CustomChart.objects.create(
    #     title = 'Missed Children PCA vs. Out of House',
    #     chart_json = {
    #         "end_date":"2016-03-01",
    #         "indicator_ids":[34,21],
    #         "campaign_ids":[5],
    #         "location_ids":[1],
    #         "type":"ColumnChart",
    #         "start_date":"2015-11-01"
    #     },
    #     uuid = '4f19f297-7c92-45e1-a4fe-def61e6c18e8'
    # )
    #
    # chart_10 = CustomChart.objects.create(
    #     title = 'Missed Children By Reason',
    #     chart_json = {
    #         "end_date":"2016-03-01",
    #         "indicator_ids":get_indicators_by_tag_name('Missed Chilren By Reason'),
    #         "campaign_ids":[5],
    #         "location_ids":[1],
    #         "type":"StackedColumnChart",
    #         "start_date":"2015-11-01"
    #     },
    #     uuid = '3f04d269-96db-4424-866f-8e09b5eeb9f3'
    # )
    #
    #
    # chart_11 = CustomChart.objects.create(
    #     title = 'LQAS',
    #     chart_json = {
    #         "start_date":"2016-03-01",
    #         "end_date":"2016-04-22",
    #         "indicator_ids": get_indicators_by_tag_name('LQAS'),
    #         "campaign_ids":[5]
    #         ,"groupBy":"indicator",
    #         "location_ids":[1],
    #         "type":"StackedPercentColumnChart"
    #     },
    #     uuid = 'a7f581a5-50b7-4ad1-83ec-c899b3e2948b'
    # )

    dashboard = CustomDashboard.objects.create(
        rows= [
            {"layout":4,
                "charts":[
                    "7e65fbd2-6cf3-43e8-8019-17cbdcd3cf46",
                    "5599c516-d2be-4ed0-ab2c-d9e7e5fe33be",
                    "1874bf4a-140a-420a-a3e2-0d29430786c0"
                ]},
            # {"layout":1,
            #     "charts":[
            #         "4499af7d-bbcc-41a6-81cf-b2071d79ce55"
            # ]},
            # {"layout":2,
            #     "charts":[
            #         "8fd8f0e2-327d-4cf6-ba11-0252e6580f38",
            #         "6f2efd2a-dd9f-4bcc-8652-7a622ebfc047"
            # ]},
            # {"layout":2,
            #     "charts":[
            #         "df3fdb84-5721-456c-8468-c4605842c7d6",
            #         "30fe1ee9-8e82-4caf-8f3b-eaf3b4cf43a9"
            # ]},
            # {"layout":2,
            #     "charts":[
            #         "4f19f297-7c92-45e1-a4fe-def61e6c18e8",
            #         "3f04d269-96db-4424-866f-8e09b5eeb9f3"
            # ]},
            # {"layout":1,
            #     "charts":[
            #         "a7f581a5-50b7-4ad1-83ec-c899b3e2948b"
            # ]}
        ],
        title = 'Situational Dashboard'
    )

def ingest_post_campaign():

    chart_0 = CustomChart.objects.create(
        title = 'Post Campaign Table',
        chart_json = {
            "end_date":"2016-02-29",
            "indicator_ids":[28,34,21,29,15,30,32,33],
            "campaign_ids":[5],
            "location_ids":[1],
            "type":"TableChart"
            ,"start_date":"2015-11-01"
        },
        uuid= '9b38b92e-ee11-4034-8cca-a73cece00927'
    )

    dashboard = CustomDashboard.objects.create(
        rows = [{
            "layout":1,
                "charts":["9b38b92e-ee11-4034-8cca-a73cece00927"],
        }],
        title = 'Post Campaign'
    )

def ingest_pre_campaign():
    chart_0 = CustomChart.objects.create(
        title = 'Pre Campaign Table',
        chart_json = {
            "end_date":"2016-03-01",
            "indicator_ids":[28,34,21,29,15,30,32,33],
            "campaign_ids":[5],
            "location_ids":[1],
            "type":"TableChart"
            ,"start_date":"2015-11-01"
        },
        uuid= "b1a6b067-f58d-472c-9953-18129bdad127"
    )
    dashboard = CustomDashboard.objects.create(
        rows = [{
            "layout":1,
                "charts":["b1a6b067-f58d-472c-9953-18129bdad127"]
        }],
        title = 'Pre Campaign'
    )

def ingest_intra_campaign():
    chart_0 = CustomChart.objects.create(
        title = 'Intra Campaign Table',
        chart_json = {
            "end_date":"2016-03-01",
            "indicator_ids":[28, 9, 11, 20, 8, 10, 22, 24, 6, 4],
            "campaign_ids":[5],
            "location_ids":[1],
            "type":"TableChart"
            ,"start_date":"2015-11-01"
        },
        uuid= "7f7b0a20-b73d-4bdb-a49a-c776d3442bd0"
    )

    dashboard = CustomDashboard.objects.create(
        rows = [{
            "layout":1,
                "charts":["7f7b0a20-b73d-4bdb-a49a-c776d3442bd0"]
        }],
        title = 'Intra Campaign'
    )

class Migration(migrations.Migration):

    dependencies = [
        ('rhizome', '0015_base_dashboard_data'),
    ]

    operations = [
        migrations.RunPython(ingest_base_dashboards)
    ]
