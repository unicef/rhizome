# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('datapoints', '0037_rm_campaign_from_datapoint'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='docdatapoint',
            name='campaign',
        ),
        migrations.AddField(
            model_name='campaign',
            name='top_lvl_indicator_tag',
            field=models.ForeignKey(default=1, to='datapoints.IndicatorTag'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='docdatapoint',
            name='data_date',
            field=models.DateTimeField(default='2016-01-01'),
            preserve_default=False,
        ),
    ]
