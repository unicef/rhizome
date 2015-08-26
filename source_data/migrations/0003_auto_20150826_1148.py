# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('source_data', '0002_sourceobjectmap_master_object_name'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='document',
            options={'ordering': ('-created_at',)},
        ),
        migrations.RenameField(
            model_name='document',
            old_name='doc_text',
            new_name='doc_title',
        ),
        migrations.AlterUniqueTogether(
            name='document',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='document',
            name='is_processed',
        ),
        migrations.RemoveField(
            model_name='document',
            name='master_datapoint_count',
        ),
        migrations.RemoveField(
            model_name='document',
            name='source_datapoint_count',
        ),
    ]
