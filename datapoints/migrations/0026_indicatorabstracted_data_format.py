# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

class Migration(migrations.Migration):
    dependencies = [
        ('datapoints', '0025_remove_locationtree_immediate_parent'),
    ]

    operations = [
        migrations.AddField(
            model_name='indicatorabstracted',
            name='data_format',
            field=models.CharField(default='int', max_length=10),
            preserve_default=False,
        ),
    ]
