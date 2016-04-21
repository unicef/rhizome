# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from pprint import pprint

from django.db import models, migrations
import jsonfield.fields
import django.db.models.deletion
from django.conf import settings
from random import randint, random

import pandas as pd
from rhizome.models import *
from django.db.models import get_app, get_models
from rhizome.cache_meta import minify_geo_json, LocationTreeCache
from rhizome.etl_tasks.refresh_master import MasterRefresh
from rhizome.agg_tasks import AggRefresh
from django.db import transaction


class DataIngestor(object):

    def __init__(self):
        self.base_columns = [u'Province', u'PCODE', u'level', u'DCODE', u'geocode', u'District.Name', u'Alternative.Spell', u'LPD.group']

    def main(self):

        chart_index_columns = ['sheet_name','data_level','date_key',\
            'month_trend_count']

        self.xl = pd.ExcelFile('SituationalDashboard.xlsx')
        raw_chart_index = self.xl.parse('chart_index')
        self.chart_index_df = raw_chart_index[raw_chart_index\
            ['to_ingest'] == 1][chart_index_columns]
        for ix, row in self.chart_index_df.iterrows():
            self.process_sheet(row.to_dict())

        
        afghanistan_missed_children_qs = DataPointComputed.objects\
           .filter(
               location_id = 1,
               indicator__name = 'Number of inaccesible children'
           )

        if len(afghanistan_missed_children_qs) == 0:
           raise Exception('The data was not loaded properly')
        
        raise Exception('This aint gonna pass')

    def process_sheet(self, sheet_dict):

        # print '==sheet_dict==\n' * 2
        # pprint(sheet_dict)

        sheet_name = sheet_dict['sheet_name']
        sheet_df = self.xl.parse(sheet_name)

        ## handle indicators ##
        indicator_names = list(set(sheet_df.columns)\
            .difference(set(self.base_columns)))
        indicator_ids = self.upsert_indicator_ids(indicator_names)

        ## handle campaigns ##
        number_of_campaigns_to_process = sheet_dict['month_trend_count']
        campaign_ids = Campaign.objects.all()\
            .values_list('id',flat=True)\
            .order_by('-start_date')[:number_of_campaigns_to_process]

        ## handle locations ##
        location_ids = Location.objects.filter(
            location_type__name = sheet_dict['data_level']
        ).values_list('id', flat=True)
        document_id = Document.objects.create(doc_title = sheet_name).id
        self.create_fake_data(indicator_ids, campaign_ids, location_ids, document_id)

        # mr = MasterRefresh(1, document_id)
        
        # for c in campaign_ids:
        #     with transaction.atomic():
        #         ar = AggRefresh(c)
        #         ar.main()

    def create_fake_data(self, indicator_ids, campaign_ids, location_ids, document_id):
        indicator_list_of_lists = [[ind] for ind in indicator_ids]
        ind_df = DataFrame(indicator_list_of_lists, columns = ['indicator_id'])
        campaign_list_of_lists  = [[camp] for camp in campaign_ids]
        campaign_df = DataFrame(campaign_list_of_lists, columns = ['campaign_id'])
        location_list_of_lists  = [[loc] for loc in location_ids]
        location_df = DataFrame(location_list_of_lists, columns = ['location_id'])
        ind_df['join_col'] = 1
        campaign_df['join_col'] = 1
        location_df['join_col'] = 1

        first_merged_df = ind_df.merge(campaign_df,on='join_col')
        final_merged_df = first_merged_df.merge(location_df, on='join_col')

        source_submission = SourceSubmission.objects.create(
            document_id = document_id,
            row_number = 1
        )

        dwc_batch = []

        for ix, row in final_merged_df.iterrows():

            # if row.data_format == 'int':
            rand_val = randint(0,1000)

            dwc_obj = DataPoint(**{
                'indicator_id':row.indicator_id,
                'campaign_id':row.campaign_id,
                'location_id':row.location_id,
                'cache_job_id':-1,
                'source_submission_id': source_submission.id,
                'value':rand_val
            })

            dwc_batch.append(dwc_obj)

        DataPoint.objects.all().delete()
        DataPoint.objects.bulk_create(dwc_batch)

    def upsert_indicator_ids(self, indicator_name_list):

        indicator_id_list = []

        for ind in indicator_name_list:
            ind_object = Indicator.objects.create(
                name = ind,
                short_name = ind,
                description = ind,
                data_format = 'int'
            )
            indicator_id_list.append(ind_object.id)

        return indicator_id_list

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
