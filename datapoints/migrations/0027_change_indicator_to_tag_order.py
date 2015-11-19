# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('datapoints', '0026_indicatorabstracted_data_format'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='indicatortotag',
            options={'ordering': ('-id',)},
        ),
    ]
