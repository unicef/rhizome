# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('datapoints', '0007_auto_20150902_0941'),
    ]

    operations = [
        migrations.AlterField(
            model_name='campaignabstracted',
            name='campaign_type',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='campaignabstracted',
            name='office',
            field=models.IntegerField(),
        ),
    ]
