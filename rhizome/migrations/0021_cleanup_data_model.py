# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rhizome', '0020_add_file_type_to_document'),
    ]

    operations = [
        migrations.RunSQL('''
            DROP TABLE rhizome_historicaldatapointentry
        '''),
        migrations.RunSQL('''
            ALTER TABLE campaign
            DROP top_lvl_location_id;

            ALTER TABLE campaign
            DROP top_lvl_indicator_tag_id;

        '''),

        ## remove old cache_job_id references ##
        migrations.RunSQL('''
            ALTER TABLE datapoint
            DROP cache_job_id;

            ALTER TABLE agg_datapoint
            DROP cache_job_id;

            ALTER TABLE datapoint_with_computed
            DROP cache_job_id;

            DROP TABLE cache_job;
        '''),

        ## remove old document references from datapoint with computed ##
        migrations.RunSQL('''
            ALTER TABLE datapoint_with_computed
            DROP document_id;
        '''),

        ## remove old office table and FKs ##
        migrations.RunSQL('''
            ALTER TABLE indicator
            DROP office_id;

            ALTER TABLE campaign
            DROP office_id;

            ALTER TABLE location
            DROP office_id;

            DROP TABLE indicator_to_office;

            -- change unique index for campaign
            -- was start_date / office -> start_date / campaign_type 
            DROP TABLE office;
        '''),

        migrations.RunSQL('''
            DROP TABLE indicator_class_map;
        ''')
    ]
