# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('datapoints', '0016_add_column_attributes'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ColumnAttributes',
        ),
    ]
