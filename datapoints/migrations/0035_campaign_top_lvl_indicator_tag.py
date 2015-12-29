# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations, transaction

from datapoints.models import Campaign, Location, DataPointComputed, \
    CampaignToIndicator, DataPoint


class Migration(migrations.Migration):

    dependencies = [
        ('datapoints', '0034_datadate_to_datapoint'),
    ]
    operations = [
        migrations.AddField(
            model_name='campaign',
            name='top_lvl_indicator_tag',
            field=models.ForeignKey(default=1, to='datapoints.IndicatorTag'),
            preserve_default=False,
        )
    ]
