# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('source_data', '0003_add_region_and_campaign_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='file_header',
            field=models.TextField(null=True),
        ),
    ]
