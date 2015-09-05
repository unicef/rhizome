# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datapoints.models


class Migration(migrations.Migration):

    dependencies = [
        ('datapoints', '0006_build_functions'),
    ]

    operations = [
        migrations.AlterField(
            model_name='campaignabstracted',
            name='office',
            field=models.IntegerField(verbose_name=datapoints.models.Office),
        ),
    ]
