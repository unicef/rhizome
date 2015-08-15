# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('source_data', '0008_auto_20150814_1248'),
    ]

    operations = [
        migrations.CreateModel(
            name='SourceSubmission',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('instance_guid', models.CharField(max_length=255)),
                ('row_number', models.IntegerField()),
                ('submission_json', jsonfield.fields.JSONField()),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('document', models.ForeignKey(to='source_data.Document')),
            ],
            options={
                'db_table': 'source_submission',
            },
        ),
    ]
