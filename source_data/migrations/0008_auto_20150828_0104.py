# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('source_data', '0007_sourcesubmissiondetail_document_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='sourcesubmissiondetail',
            old_name='document_id',
            new_name='document',
        ),
    ]
