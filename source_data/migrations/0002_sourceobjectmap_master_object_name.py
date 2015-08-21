# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('source_data', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='sourceobjectmap',
            name='master_object_name',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
