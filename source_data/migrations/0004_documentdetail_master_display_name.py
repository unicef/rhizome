# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('source_data', '0003_auto_20150805_0809'),
    ]

    operations = [
        migrations.AddField(
            model_name='documentdetail',
            name='master_display_name',
            field=models.CharField(default=1, max_length=255),
            preserve_default=False,
        ),
    ]
