# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('datapoints', '0022_indicator_data_format'),
    ]

    operations = [
        migrations.AddField(
            model_name='customdashboard',
            name='layout',
            field=models.IntegerField(default=0, null=True),
        ),
    ]
