# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('source_data', '0015_remove_sourceobjectmap_document'),
    ]

    operations = [
        migrations.AddField(
            model_name='sourcesubmission',
            name='process_status',
            field=models.CharField(default=1, max_length=25),
            preserve_default=False,
        ),
    ]
