# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('source_data', '0004_remove_submission_detail'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sourcesubmission',
            name='campaign',
        ),
        migrations.RemoveField(
            model_name='sourcesubmission',
            name='campaign_code',
        ),
        migrations.RemoveField(
            model_name='sourcesubmission',
            name='location',
        ),
        migrations.AddField(
            model_name='sourcesubmission',
            name='data_date',
            field=models.DateTimeField(default='2016-01-01'),
            preserve_default=False,
        ),
    ]
