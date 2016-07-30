# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.db.utils import ProgrammingError

import django.db.models.deletion

def add_file_type_if_not_exists(apps, schema_editor):
    '''
    THis should run on production, but not when spinning up a new database
    '''

    try:
        migrations.AddField(
            model_name='document',
            name='file_type',
            field=models.CharField(default='campaign', max_length=10),
            preserve_default=False,
        )
    except ProgrammingError:
        pass


class Migration(migrations.Migration):

    dependencies = [
        ('rhizome', '0005_reset_sql_sequence'),
    ]

    operations = [
        migrations.RunPython(add_file_type_if_not_exists)
    ]
