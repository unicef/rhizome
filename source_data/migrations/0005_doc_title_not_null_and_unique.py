# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('source_data', '0004_document_file_header'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='doc_title',
            field=models.TextField(unique=True),
        ),
        migrations.AlterField(
            model_name='document',
            name='file_header',
            field=jsonfield.fields.JSONField(null=True),
        ),
    ]
