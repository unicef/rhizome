# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('docfile', models.FileField(null=True, upload_to=b'documents/%Y/%m/%d')),
                ('doc_text', models.TextField(null=True)),
                ('guid', models.CharField(max_length=255)),
                ('source_datapoint_count', models.IntegerField(null=True)),
                ('master_datapoint_count', models.IntegerField(null=True)),
                ('is_processed', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-id',),
            },
        ),
        migrations.CreateModel(
            name='DocumentDetail',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('doc_detail_type', models.CharField(max_length=25)),
                ('doc_detail_json', jsonfield.fields.JSONField()),
                ('document', models.ForeignKey(to='source_data.Document')),
            ],
            options={
                'db_table': 'document_detail',
            },
        ),
        migrations.CreateModel(
            name='DocumentSourceObjectMap',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('document', models.ForeignKey(to='source_data.Document')),
            ],
            options={
                'db_table': 'document_to_source_object_map',
            },
        ),
        migrations.CreateModel(
            name='EtlJob',
            fields=[
                ('date_attempted', models.DateTimeField(auto_now=True)),
                ('date_completed', models.DateTimeField(null=True)),
                ('task_name', models.CharField(max_length=55)),
                ('status', models.CharField(max_length=10)),
                ('guid', models.CharField(max_length=40, serialize=False, primary_key=True)),
                ('cron_guid', models.CharField(max_length=40)),
                ('error_msg', models.TextField(null=True)),
                ('success_msg', models.CharField(max_length=255)),
            ],
            options={
                'ordering': ('-date_attempted',),
            },
        ),
        migrations.CreateModel(
            name='ODKForm',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('last_processed', models.DateTimeField(null=True)),
                ('response_msg', models.CharField(max_length=255, null=True)),
                ('source_datapoint_count', models.IntegerField(default=0)),
                ('master_datapoint_count', models.IntegerField(default=0)),
                ('form_name', models.CharField(max_length=255)),
                ('document', models.ForeignKey(to='source_data.Document', null=True)),
            ],
            options={
                'db_table': 'odk_form',
            },
        ),
        migrations.CreateModel(
            name='ProcessStatus',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('status_text', models.CharField(max_length=25)),
                ('status_description', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='SourceObjectMap',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('master_object_id', models.IntegerField()),
                ('source_object_code', models.CharField(max_length=255)),
                ('content_type', models.CharField(max_length=10)),
                ('mapped_by', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'source_object_map',
            },
        ),
        migrations.CreateModel(
            name='SourceSubmission',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('instance_guid', models.CharField(max_length=255)),
                ('row_number', models.IntegerField()),
                ('submission_json', jsonfield.fields.JSONField()),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('process_status', models.CharField(max_length=25)),
                ('document', models.ForeignKey(to='source_data.Document')),
            ],
            options={
                'db_table': 'source_submission',
            },
        ),
        migrations.AddField(
            model_name='DocumentSourceObjectMap',
            name='source_object_map',
            field=models.ForeignKey(to='source_data.SourceObjectMap'),
        ),
        migrations.AlterUniqueTogether(
            name='sourcesubmission',
            unique_together=set([('document', 'instance_guid')]),
        ),
        migrations.AlterUniqueTogether(
            name='sourceobjectmap',
            unique_together=set([('content_type', 'source_object_code')]),
        ),
        migrations.AlterUniqueTogether(
            name='DocumentSourceObjectMap',
            unique_together=set([('document', 'source_object_map')]),
        ),
        migrations.AlterUniqueTogether(
            name='documentdetail',
            unique_together=set([('document', 'doc_detail_type')]),
        ),
        migrations.AlterUniqueTogether(
            name='document',
            unique_together=set([('docfile', 'doc_text')]),
        ),
    ]
