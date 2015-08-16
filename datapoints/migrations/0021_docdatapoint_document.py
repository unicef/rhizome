# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('source_data', '0013_auto_20150816_0942'),
        ('datapoints', '0020_auto_20150816_1253'),
    ]

    operations = [
        migrations.AddField(
            model_name='docdatapoint',
            name='document',
            field=models.ForeignKey(default=66, to='source_data.Document'),
            preserve_default=False,
        ),
    ]
