# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('datapoints', '0020_chart_type_schema'),
        ('source_data', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='sourcesubmission',
            name='campaign',
            field=models.ForeignKey(to='datapoints.Campaign', null=True),
        ),
        migrations.AddField(
            model_name='sourcesubmission',
            name='campaign_code',
            field=models.CharField(default='', max_length=1000),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='sourcesubmission',
            name='location',
            field=models.ForeignKey(to='datapoints.Location', null=True),
        ),
        migrations.AddField(
            model_name='sourcesubmission',
            name='location_code',
            field=models.CharField(default='', max_length=1000),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='sourcesubmission',
            name='location_display',
            field=models.CharField(default='', max_length=1000),
            preserve_default=False,
        ),
    ]
