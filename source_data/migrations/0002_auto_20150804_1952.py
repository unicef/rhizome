# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('source_data', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 8, 4, 19, 52, 15, 352647)),
        ),
        migrations.AlterField(
            model_name='etljob',
            name='date_attempted',
            field=models.DateTimeField(default=datetime.datetime(2015, 8, 4, 19, 52, 15, 350959)),
        ),
        migrations.AlterField(
            model_name='sourcedatapoint',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 8, 4, 19, 52, 15, 353653)),
        ),
        migrations.AlterField(
            model_name='vcmsettlement',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 8, 4, 19, 52, 15, 363341)),
        ),
    ]
