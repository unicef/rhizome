# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jsonfield.fields
import django.db.models.deletion
from django.conf import settings

import pandas as pd
from rhizome.models import Location, LocationPolygon
from django.db.models import get_app, get_models
from rhizome.cache_meta import minify_geo_json, LocationTreeCache


class DataIngestor(object):

    def __init__(self):
        pass

    def main(self):

        chart_index_columns = ['sheet_name','data_level','date_key',\
            'month_trend_count']

        self.xl = pd.ExcelFile('SituationalDashboard.xlsx')
        raw_chart_index = self.xl.parse('chart_index')
        self.chart_index_df = raw_chart_index[raw_chart_index\
            ['to_ingest'] == 1][chart_index_columns]

        for ix, row in self.chart_index_df.iterrows():
            self.process_sheet(row.to_dict())

        raise('this aint gonna pass')

    def process_sheet(self, sheet_dict):

        print '==='
        print sheet_dict
        sheet_df = self.xl.parse(sheet_dict['sheet_name'])
        number_of_campaigns_to_process = sheet_dict['month_trend_count']
        campaigns_to_ingest = Campaign.objects.all().order_by('-start_date')\
            [:number_of_campaigns_to_process]

        print sheet_df
        print '==='




def populate_base_dashboard_data(apps, schema_editor):

    d = DataIngestor()
    d.main()


class Migration(migrations.Migration):

    dependencies = [
        ('rhizome', '0014_base_dashboards'),
    ]

    operations = [
        migrations.RunPython(populate_base_dashboard_data),
    ]
