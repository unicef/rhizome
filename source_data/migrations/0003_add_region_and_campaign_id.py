# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('datapoints', '0009_indicator_map'),
        ('source_data', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='odkform',
            name='document',
        ),
        migrations.AddField(
            model_name='sourcesubmissiondetail',
            name='campaign',
            field=models.ForeignKey(to='datapoints.Campaign', null=True),
        ),
        migrations.AddField(
            model_name='sourcesubmissiondetail',
            name='region',
            field=models.ForeignKey(to='datapoints.Region', null=True),
        ),
        migrations.DeleteModel(
            name='ODKForm',
        ),
    ]
