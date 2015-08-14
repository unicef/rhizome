# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('source_data', '0006_auto_20150813_0243'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='documentdetail',
            options={},
        ),
        migrations.RemoveField(
            model_name='documentdetail',
            name='db_model',
        ),
        migrations.RemoveField(
            model_name='documentdetail',
            name='map_id',
        ),
        migrations.RemoveField(
            model_name='documentdetail',
            name='master_display_name',
        ),
        migrations.RemoveField(
            model_name='documentdetail',
            name='master_dp_count',
        ),
        migrations.RemoveField(
            model_name='documentdetail',
            name='master_object_id',
        ),
        migrations.RemoveField(
            model_name='documentdetail',
            name='source_dp_count',
        ),
        migrations.RemoveField(
            model_name='documentdetail',
            name='source_object_id',
        ),
        migrations.RemoveField(
            model_name='documentdetail',
            name='source_string',
        ),
        migrations.AddField(
            model_name='documentdetail',
            name='doc_detail_json',
            field=jsonfield.fields.JSONField(default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='documentdetail',
            name='doc_detail_type',
            field=models.CharField(default='', max_length=25),
            preserve_default=False,
        ),
    ]
