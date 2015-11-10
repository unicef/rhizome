# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('source_data', '0002_migrate_submission_campaign_and_location'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sourcesubmissiondetail',
            name='campaign',
        ),
        migrations.RemoveField(
            model_name='sourcesubmissiondetail',
            name='document',
        ),
        migrations.RemoveField(
            model_name='sourcesubmissiondetail',
            name='location',
        ),
        migrations.RemoveField(
            model_name='sourcesubmissiondetail',
            name='source_submission',
        ),
        migrations.DeleteModel(
            name='SourceSubmissionDetail',
        ),
    ]
