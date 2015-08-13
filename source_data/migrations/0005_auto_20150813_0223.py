# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('source_data', '0004_documentdetail_master_display_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='documentdetail',
            name='master_display_name',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
