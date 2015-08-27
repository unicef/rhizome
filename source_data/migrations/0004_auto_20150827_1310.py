# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('source_data', '0003_auto_20150826_1148'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='documentdetail',
            name='doc_detail_json',
        ),
        migrations.AddField(
            model_name='documentdetail',
            name='doc_detail_value',
            field=models.CharField(default=1, max_length=255),
            preserve_default=False,
        ),
    ]
