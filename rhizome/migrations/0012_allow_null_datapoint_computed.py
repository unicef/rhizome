# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rhizome', '0011_customdashboard_rows'),
    ]

    operations = [
        migrations.AlterField(
            model_name='datapointcomputed',
            name='value',
            field=models.FloatField(null=True),
        ),
    ]
