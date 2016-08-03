# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.db.utils import ProgrammingError

import django.db.models.deletion

class Migration(migrations.Migration):

    dependencies = [
        ('rhizome', '0005_reset_sql_sequence'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='file_type',
            field=models.CharField(default='campaign', max_length=10),
            preserve_default=False,
        )
    ]
