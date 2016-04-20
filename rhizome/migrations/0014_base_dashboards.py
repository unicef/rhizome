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


    CustomChart.objects.all().delete()
    CustomDashboard.objects.all().delete()

    chart_dict_0 = {
        "end_date":"2016-02-29",
        "indicator_ids":[28,34,21,29,15,30,32,33],
        "campaign_ids":[1],
        "location_ids":[1],
        "type":"TableChart"
        ,"start_date":"2016-02-01"
    }

    chart_0 = CustomChart.objects.create(
        title = 'Post Campaign Table',
        chart_json = chart_dict_0,
        uuid= '9b38b92e-ee11-4034-8cca-a73cece00927'
    )

    dashboard_row_dict_0 = [{
        "layout":1,
        "charts":["9b38b92e-ee11-4034-8cca-a73cece00927"]
        }
    ]
    dashboard_0 = CustomDashboard.objects.create(
        rows = dashboard_row_dict_0,
        title = 'Post Campaign'
    )

class Migration(migrations.Migration):

    dependencies = [
        ('rhizome', '0013_ingest_polio_cases'),
    ]

    operations = [
        migrations.RunPython(ingest_base_dashboards)
    ]
