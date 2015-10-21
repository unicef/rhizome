# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('datapoints', '0018_delete_campaignabstracted'),
    ]

    operations = [
        migrations.AddField(
            model_name='campaign',
            name='management_dash_pct_complete',
            field=models.FloatField(default=.001),
            preserve_default=False,
        ),
    ]
