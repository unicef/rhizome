# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

class Migration(migrations.Migration):
    dependencies = [
        ('source_data', '0004_remove_submission_detail'),
    ]

    operations = [
        migrations.AddField(
            model_name='sourcesubmission',
            name='campaign_code',
            field=models.CharField(default='', max_length=1000),
            preserve_default=False,
        ),
    ]
