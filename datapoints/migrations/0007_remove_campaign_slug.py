# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('datapoints', '0006_indicator_source_name'),
    ]

    operations = [
        migrations.RunSQL('''
        alter table campaign drop column if exists slug;
        ''')
    ]
