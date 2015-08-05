# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('source_data', '0002_auto_20150804_1952'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='created_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='etljob',
            name='date_attempted',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='sourcedatapoint',
            name='created_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='vcmsettlement',
            name='created_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
