# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('datapoints', '0009_indicator_map'),
        ('source_data', '0002_build_functions'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='odkform',
            name='document',
        ),
        migrations.AddField(
            model_name='sourcesubmissiondetail',
            name='campaign_id',
            field=models.ForeignKey(to='datapoints.Campaign', null=True),
        ),
        migrations.AddField(
            model_name='sourcesubmissiondetail',
            name='region_id',
            field=models.ForeignKey(to='datapoints.Region', null=True),
        ),
        migrations.DeleteModel(
            name='ODKForm',
        ),
    ]
