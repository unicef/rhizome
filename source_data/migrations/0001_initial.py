# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jsonfield.fields
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='DocDetailType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255)),
            ],
            options={
                'db_table': 'doc_detail_type',
            },
        ),
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('docfile', models.FileField(null=True, upload_to=b'documents/%Y/%m/%d')),
                ('doc_title', models.TextField(unique=True)),
                ('file_header', jsonfield.fields.JSONField(null=True)),
                ('guid', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-created_at',),
                'db_table': 'source_doc',
            },
        ),
        migrations.CreateModel(
            name='DocumentDetail',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('doc_detail_value', models.CharField(max_length=255)),
                ('doc_detail_type', models.ForeignKey(to='source_data.DocDetailType')),
                ('document', models.ForeignKey(to='source_data.Document')),
            ],
            options={
                'db_table': 'doc_detail',
            },
        ),
        migrations.CreateModel(
            name='DocumentSourceObjectMap',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('document', models.ForeignKey(to='source_data.Document')),
            ],
            options={
                'db_table': 'doc_object_map',
            },
        ),
        migrations.CreateModel(
            name='SourceObjectMap',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('master_object_id', models.IntegerField()),
                ('master_object_name', models.CharField(max_length=255, null=True)),
                ('source_object_code', models.CharField(max_length=255)),
                ('content_type', models.CharField(max_length=20)),
                ('mapped_by', models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True)),
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
                ('data_date', models.DateTimeField()),
                ('location_code', models.CharField(max_length=1000)),
                ('location_display', models.CharField(max_length=1000)),
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
            model_name='documentsourceobjectmap',
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
            name='documentsourceobjectmap',
            unique_together=set([('document', 'source_object_map')]),
        ),
        migrations.AlterUniqueTogether(
            name='documentdetail',
            unique_together=set([('document', 'doc_detail_type')]),
        ),
    ]
