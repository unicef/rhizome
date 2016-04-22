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
from django.core.exceptions import ObjectDoesNotExist

class DataIngestor(object):

    def __init__(self):
        pass

    # psql rhizome -c "DELETE FROM django_migrations where name like '%base_dashboard%';"

    def main(self):

        chart_index_columns = ['sheet_name','data_level','date_key',\
            'month_trend_count','chart_key']

        self.xl = pd.ExcelFile('SituationalDashboard.xlsx')

        raw_chart_index = self.xl.parse('chart_index')
        self.chart_index_df = raw_chart_index[raw_chart_index\
            ['to_ingest'] == 1]

        self.indicator_sheet_df = self.xl.parse('indicators')

        eoc_tag_id = IndicatorTag.objects.get(tag_name =\
            'Kabul EOC Indicators').id
        self.situational_dashboard_tag_id = IndicatorTag.objects.create(
            tag_name = 'Situational Dashboard',
            parent_tag_id = eoc_tag_id
        ).id

        for ix, row in self.chart_index_df.iterrows():
            self.process_sheet(row.to_dict())

        self.validate_ingest()

    def validate_ingest(self):

        afghanistan_missed_children_qs = DataPointComputed.objects\
           .filter(
               location_id = 1,
               indicator__short_name = 'Number Inaccessible Children'
           )
        if len(afghanistan_missed_children_qs) == 0:
           raise Exception('The data was not loaded properly for t5')

        infected_dist_dwcs= DataPointComputed.objects\
            .filter(
                location_id = 1,
                indicator__short_name = 'Infected district (Yes/No)'
            )

        if len(infected_dist_dwcs) == 0:
           raise Exception('The data was not loaded properly for t3')

        non_polio_afp_dwc = DataPointComputed.objects\
            .filter(
                location_id = 1,
                indicator__short_name = 'Number of reported Non Polio AFP cases'
            )
        if len(non_polio_afp_dwc) == 0:
            raise Exception('The data was not loaded properly for t4')

        afp_rate = DataPointComputed.objects\
            .filter(
                location_id=1,
                indicator__short_name = 'Non Polio AFP Rate'
            )

        if len(afp_rate) == 0:
            raise Exception('The data was not loaded properly t4')

        env_samples = DataPointComputed.objects.filter(
            location_id = 1,
            indicator__short_name = "Number of Environmental Samples with result pending in Lab"
        )

        if len(env_samples) == 0:
            raise Exception('The data was not loaded properly for t6')

        polio_cases = DataPointComputed.objects.filter(
            location_id = 1,
            indicator__short_name = "polio cases"
        )

        if len(polio_cases) == 0:
            raise Exception('The data was not loaded properly for m__1')

        district_meeting = DataPointComputed.objects.filter(
            location_id = 1,
            indicator__short_name = 'District review and planning meeting'
        )

        if len(district_meeting) == 0:
            raise Exception('The data was not loaded properly for t7')

        num_vaccinated = DataPointComputed.objects.filter(
            location_id = 1,
            indicator__short_name = 'Number.Vaccinated.Recorded.3days'
        )

        if len(num_vaccinated) == 0:
            raise Exception('The data was not loaded properly for t8')

        # num_seen = DataPointComputed.objects.filter(
        #     location_id = 1,
        #     indicator__short_name = 'Number.Children.Seen.Market.Survey'
        # )

        # if len(num_seen) == 0:
        #     raise Exception('The data was not loaded properly for t9')

        num_seen_pca = DataPointComputed.objects.filter(
            location_id = 1,
            indicator__short_name = '# children seen - PCA'
        )

        if len(num_seen_pca) == 0:
            raise Exception('The data was not properly loaded for t11')

        
    def process_sheet(self, sheet_dict):

        # print '==sheet_dict==\n' * 2
        # pprint(sheet_dict)

        chart_name = sheet_dict['chart']
        chart_key = sheet_dict['chart_key']

        ## handle indicators ##
        chart_indicator_df = self.indicator_sheet_df[self.indicator_sheet_df\
            ['chart_key'] == chart_key]
        indicator_ids = self.upsert_indicator_ids(chart_name, chart_indicator_df)

        ## handle campaigns ##
        number_of_campaigns_to_process = sheet_dict['month_trend_count']
        campaign_ids = Campaign.objects.all()\
            .values_list('id',flat=True)\
            .order_by('-start_date')[:number_of_campaigns_to_process]

        ## handle locations ##
        location_ids = Location.objects.filter(
            location_type__name = sheet_dict['data_level']
        ).values_list('id', flat=True)

        document, created = Document.objects\
            .get_or_create(doc_title = 'fake situational -- ' + chart_name)

        self.create_fake_data(indicator_ids, campaign_ids, location_ids, document.id)

        for c in campaign_ids:
            ar = AggRefresh(c)

    def create_fake_data(self, indicator_ids, campaign_ids, location_ids, document_id):

        indicator_df_cols =['id', 'data_format']
        ind_df = DataFrame(list(Indicator.objects.filter(id__in= indicator_ids).values('id', 'data_format')), columns = indicator_df_cols)
        ind_df.columns = ['indicator_id', 'data_format']

        campaign_list_of_lists  = [[camp] for camp in campaign_ids]
        campaign_df = DataFrame(campaign_list_of_lists, columns = ['campaign_id'])


        location_list_of_lists  = [[loc] for loc in location_ids]
        location_df = DataFrame(location_list_of_lists, columns = ['location_id'])

        ind_df['join_col'] = 1
        campaign_df['join_col'] = 1
        location_df['join_col'] = 1

        first_merged_df = ind_df.merge(campaign_df,on='join_col')
        final_merged_df = first_merged_df.merge(location_df, on='join_col')
        source_submission, created = SourceSubmission.objects.get_or_create(
            document_id = document_id,
            row_number = 1,
            defaults = { 'instance_guid': document_id }
        )

        dwc_batch = []

        for ix, row in final_merged_df.iterrows():
            if row.data_format == 'int':
                rand_val = randint(0,1000)
            if row.data_format =='bool':
                rand_val = randint(0,1)
            if row.data_format == 'pct':
                rand_val = float(randint(0, 100))/100

            dwc_obj = DataPoint(**{
                'indicator_id':row.indicator_id,
                'campaign_id':row.campaign_id,
                'location_id':row.location_id,
                'cache_job_id':-1,
                'source_submission_id': source_submission.id,
                'value':rand_val
            })
            dwc_batch.append(dwc_obj)

        print'\n---dps before----\n'
        print len(DataPoint.objects.all())
        DataPoint.objects.bulk_create(dwc_batch)
        print'\n---dps after----\n'
        print len(DataPoint.objects.all())

    def upsert_indicator_ids(self, chart_name, chart_indicator_df):

        chart_tag, created = IndicatorTag.objects.get_or_create(
            tag_name = chart_name,
            defaults = {'parent_tag_id': self.situational_dashboard_tag_id}
        )

        indicator_id_list = []

        IndicatorToTag.objects.filter(indicator_tag_id = chart_tag.id).delete()

        for ix, row in chart_indicator_df.iterrows():
            row_dict = row.to_dict()
            row_dict.pop('chart_key')

            indicator_name = row_dict['name']
            indicator_short_name = row_dict['short_name']
            row_dict.pop('name')
            row_dict.pop('short_name')

            ind_object, created = Indicator.objects\
                .get_or_create(name = indicator_name,\
                    short_name = indicator_short_name,\
                 defaults = row_dict)

            indicator_id_list.append(ind_object.id)

            IndicatorToTag.objects.create(
                indicator_tag_id = chart_tag.id,
                indicator_id = ind_object.id
            )

        return indicator_id_list

def populate_base_dashboard_data(apps, schema_editor):

    d = DataIngestor()
    d.main()


class Migration(migrations.Migration):

    dependencies = [
        ('rhizome', '0013_ingest_polio_cases'),
    ]

    operations = [
        migrations.RunPython(populate_base_dashboard_data),
    ]
