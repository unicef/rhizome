# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('source_data', '0005_auto_20150827_1459'),
    ]

    operations = [
        migrations.CreateModel(
            name='SourceSubmissionDetail',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('submission_username', models.CharField(max_length=1000)),
                ('img_location', models.CharField(max_length=1000)),
                ('source_submission', models.OneToOneField(to='source_data.SourceSubmission')),
            ],
            options={
                'db_table': 'source_submission_detail',
            },
        ),
        migrations.AlterField(
            model_name='documentdetail',
            name='doc_detail_type',
            field=models.ForeignKey(to='source_data.DocDetailType'),
        ),
    ]
