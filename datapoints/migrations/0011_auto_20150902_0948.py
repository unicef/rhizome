# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('datapoints', '0010_auto_20150902_0947'),
    ]

    operations = [
        migrations.AddField(
            model_name='campaignabstracted',
            name='campaign_type_id',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='campaignabstracted',
            name='office_id',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
