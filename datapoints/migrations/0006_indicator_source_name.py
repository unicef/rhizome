# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('datapoints', '0005_indicator_low_and_high_bound'),
    ]

    operations = [
        migrations.AddField(
            model_name='indicator',
            name='source_name',
            field=models.CharField(default='NEEDS SOURCE', max_length=25),
            preserve_default=False,
        ),
    ]
