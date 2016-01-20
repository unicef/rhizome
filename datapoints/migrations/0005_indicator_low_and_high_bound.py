# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('datapoints', '0004_remove_docdatapoint_is_valid'),
    ]

    operations = [
        migrations.AddField(
            model_name='indicator',
            name='high_bound',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='indicator',
            name='low_bound',
            field=models.FloatField(null=True),
        ),
    ]
