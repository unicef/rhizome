# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import  migrations


class Migration(migrations.Migration):

    dependencies = [
        ('datapoints', '0023_customdashboard_layout'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userabstracted',
            name='user',
        ),
        migrations.DeleteModel(
            name='UserAbstracted',
        ),
    ]
