# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('datapoints', '0008_load_base_permissions'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='regionpolygon',
            name='region',
        ),
        migrations.DeleteModel(
            name='RegionPolygon',
        ),
    ]
