# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('datapoints', '0015_dashboard_json_to_charts'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='datapointabstracted',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='datapointabstracted',
            name='cache_job',
        ),
        migrations.RemoveField(
            model_name='datapointabstracted',
            name='campaign',
        ),
        migrations.RemoveField(
            model_name='datapointabstracted',
            name='location',
        ),
        migrations.DeleteModel(
            name='DataPointAbstracted',
        ),
    ]
