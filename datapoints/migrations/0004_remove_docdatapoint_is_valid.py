# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('datapoints', '0003_add_earth_location'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='docdatapoint',
            name='is_valid',
        ),
    ]
