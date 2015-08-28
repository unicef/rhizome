# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('source_data', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='sourcesubmissiondetail',
            old_name='submission_username',
            new_name='campaign_code',
        ),
        migrations.AddField(
            model_name='sourcesubmissiondetail',
            name='raw_data_proxy',
            field=models.CharField(default='', max_length=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='sourcesubmissiondetail',
            name='region_code',
            field=models.CharField(default='', max_length=1000),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='sourcesubmissiondetail',
            name='region_display',
            field=models.CharField(default='', max_length=1000),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='sourcesubmissiondetail',
            name='username_code',
            field=models.CharField(default='', max_length=1000),
            preserve_default=False,
        ),
    ]
