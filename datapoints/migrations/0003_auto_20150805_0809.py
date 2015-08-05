# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('datapoints', '0002_auto_20150804_1951'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cachejob',
            name='date_attempted',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
