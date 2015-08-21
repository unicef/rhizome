# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from datapoints import cache_tasks

def cache_metadata(apps, schema_editor):


    indicator_cache_data = cache_tasks.cache_indicator_abstracted()
    campaign_cache_data = cache_tasks.cache_campaign_abstracted()



class Migration(migrations.Migration):

    dependencies = [
        ('datapoints', '0004_load_indicators_campaigns_permissions'),
    ]

    operations = [
        migrations.RunSQL("""
        SELECT setval('indicator_id_seq', (SELECT MAX(id) FROM indicator));
        SELECT setval('campaign_id_seq', (SELECT MAX(id) FROM campaign));
        SELECT setval('region_id_seq', (SELECT MAX(id) FROM region));
        SELECT setval('indicator_tag_id_seq', (SELECT MAX(id) FROM indicator_tag));
        """),

        migrations.RunPython(cache_metadata),

    ]
