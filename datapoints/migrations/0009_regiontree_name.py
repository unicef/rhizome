# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('datapoints', '0008_ingest_geojson'),
    ]

    operations = [
        migrations.AddField(
            model_name='regiontree',
            name='name',
            field=models.CharField(default='test', max_length=255),
            preserve_default=False,
        ),
    ]
