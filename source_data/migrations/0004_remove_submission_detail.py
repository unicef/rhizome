# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('source_data', '0003_update_source_submission_details'),
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
