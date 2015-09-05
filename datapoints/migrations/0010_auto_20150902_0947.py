# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('datapoints', '0009_auto_20150902_0946'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='campaignabstracted',
            name='campaign_type_id',
        ),
        migrations.RemoveField(
            model_name='campaignabstracted',
            name='office_id',
        ),
    ]
