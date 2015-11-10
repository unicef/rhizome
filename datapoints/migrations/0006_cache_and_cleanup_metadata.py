# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from datapoints import agg_tasks

def cache_metadata(apps, schema_editor):


    indicator_cache_data = agg_tasks.cache_indicator_abstracted()
    campaign_cache_data = agg_tasks.calculate_campaign_percentage_complete()



class Migration(migrations.Migration):

    dependencies = [
        ('datapoints', '0005_load_indicator_result_permission'),
    ]

    operations = [
        migrations.RunSQL("""
        SELECT setval('indicator_id_seq', (SELECT MAX(id) FROM indicator));
        SELECT setval('campaign_id_seq', (SELECT MAX(id) FROM campaign));
        SELECT setval('location_id_seq', (SELECT MAX(id) FROM location));
        SELECT setval('indicator_tag_id_seq', (SELECT MAX(id) FROM indicator_tag));
        """),

        migrations.RunPython(cache_metadata),

    ]
