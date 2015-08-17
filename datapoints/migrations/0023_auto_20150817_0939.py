# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('datapoints', '0022_docdatapoint_agg_on_region'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='baddata',
            name='cache_job',
        ),
        migrations.RemoveField(
            model_name='baddata',
            name='datapoint',
        ),
        migrations.RemoveField(
            model_name='baddata',
            name='document',
        ),
        migrations.DeleteModel(
            name='BadData',
        ),
    ]
