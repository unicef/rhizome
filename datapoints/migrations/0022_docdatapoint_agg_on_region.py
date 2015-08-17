# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('datapoints', '0021_docdatapoint_document'),
    ]

    operations = [
        migrations.AddField(
            model_name='docdatapoint',
            name='agg_on_region',
            field=models.BooleanField(default=True),
            preserve_default=False,
        ),
    ]
