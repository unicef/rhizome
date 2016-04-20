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

    ingest_post_campaign()

def ingest_post_campaign():
    #
    # TRUNCATE TABLE custom_dashboard CASCADE;
    # TRUNCATE TABLE custom_chart CASCADE;
    # DELETE FROM django_migrations where name like '%base_dashboar%';

    CustomChart.objects.all().delete()
    CustomDashboard.objects.all().delete()

    chart_0 = CustomChart.objects.create(
        title = 'Post Campaign Table',
        chart_json = {
            "end_date":"2016-02-29",
            "indicator_ids":[28,34,21,29,15,30,32,33],
            "campaign_ids":[5],
            "location_ids":[33],
            "type":"TableChart"
            ,"start_date":"2016-02-01"
        },
        uuid= '9b38b92e-ee11-4034-8cca-a73cece00927'
    )

    chart_1 = CustomChart.objects.create(
        title = 'LQAS Assesment',
        chart_json = {
            "end_date":"2016-03-01",
            "indicator_ids":[29],
            "campaign_ids":[5],
            "location_ids":[33],
            "type":"MapChart",
            "start_date":"2016-02-01"
        },
        uuid= '000fef60-61de-4104-9ad9-69c3c9fd6634'
    )

    chart_2 = CustomChart.objects.create(
        title = 'Missed Children Trend ( PCA / Out of House Survey )',
        chart_json = {
            "end_date":"2016-03-01",
            "indicator_ids":[34,21],
            "campaign_ids":[5],
            "location_ids":[157],
            "type":"LineChart",
            "start_date":"2015-02-01"
        },
        uuid = 'e2a6e9ac-78be-4def-bfe1-b978f726f447'
    )

    chart_3 = CustomChart.objects.create(
        title = 'PCA Percent Missed Children',
        chart_json = {
            "end_date":"2016-03-01",
            "indicator_ids":[34],
            "campaign_ids":[5],
            "location_ids":[33],
            "type":"MapChart",
            "start_date":"2016-02-01"
        },
        uuid = '5582a06b-fa1a-4c91-bf72-ffca6e30cf57'
    )

    dashboard_dict = [{
        "layout":1,
        "charts":["9b38b92e-ee11-4034-8cca-a73cece00927"]},{"layout":2,"charts":["5582a06b-fa1a-4c91-bf72-ffca6e30cf57","000fef60-61de-4104-9ad9-69c3c9fd6634"]},{"layout":1,"charts":["e2a6e9ac-78be-4def-bfe1-b978f726f447"]
    }]

    dashboard = CustomDashboard.objects.create(
        rows = dashboard_dict,
        title = 'Post Campaign'
    )

class Migration(migrations.Migration):

    dependencies = [
        ('rhizome', '0013_ingest_polio_cases'),
    ]

    operations = [
        migrations.RunPython(ingest_base_dashboards)
    ]
