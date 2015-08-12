# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('datapoints', '0014_auto_20150812_0842'),
    ]

    operations = [
    migrations.RunSQL("""
    SELECT setval('indicator_id_seq', (SELECT MAX(id) FROM indicator));
    SELECT setval('campaign_id_seq', (SELECT MAX(id) FROM campaign));
    SELECT setval('region_id_seq', (SELECT MAX(id) FROM region));
    SELECT setval('indicator_tag_id_seq', (SELECT MAX(id) FROM indicator_tag));
    """)
    ]
