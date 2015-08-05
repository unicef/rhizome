# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import datetime


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('datapoints', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CampaignMap',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('mapped_by', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('master_object', models.ForeignKey(to='datapoints.Campaign')),
            ],
            options={
                'db_table': 'campaign_map',
            },
        ),
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
                ('created_at', models.DateTimeField(default=datetime.datetime(2015, 8, 4, 19, 51, 28, 360667))),
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
                ('db_model', models.CharField(max_length=255)),
                ('source_object_id', models.IntegerField()),
                ('master_object_id', models.IntegerField()),
                ('source_string', models.CharField(max_length=255)),
                ('source_dp_count', models.IntegerField()),
                ('master_dp_count', models.IntegerField()),
                ('map_id', models.IntegerField()),
                ('document', models.ForeignKey(to='source_data.Document')),
            ],
            options={
                'db_table': 'document_detail',
            },
        ),
        migrations.CreateModel(
            name='EtlJob',
            fields=[
                ('date_attempted', models.DateTimeField(default=datetime.datetime(2015, 8, 4, 19, 51, 28, 359035))),
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
            name='IndicatorMap',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('mapped_by', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('master_object', models.ForeignKey(to='datapoints.Indicator')),
            ],
            options={
                'db_table': 'indicator_map',
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
            name='RegionMap',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('mapped_by', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('master_object', models.ForeignKey(to='datapoints.Region')),
            ],
            options={
                'db_table': 'region_map',
            },
        ),
        migrations.CreateModel(
            name='SourceCampaign',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('campaign_string', models.CharField(unique=True, max_length=255)),
                ('source_guid', models.CharField(max_length=255)),
                ('document', models.ForeignKey(to='source_data.Document')),
            ],
            options={
                'db_table': 'source_campaign',
            },
        ),
        migrations.CreateModel(
            name='SourceDataPoint',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('region_code', models.CharField(max_length=255)),
                ('campaign_string', models.CharField(max_length=255)),
                ('indicator_string', models.CharField(max_length=255)),
                ('cell_value', models.CharField(max_length=255, null=True)),
                ('row_number', models.IntegerField()),
                ('source_guid', models.CharField(max_length=255)),
                ('guid', models.CharField(unique=True, max_length=255)),
                ('created_at', models.DateTimeField(default=datetime.datetime(2015, 8, 4, 19, 51, 28, 361651))),
                ('document', models.ForeignKey(to='source_data.Document')),
                ('status', models.ForeignKey(to='source_data.ProcessStatus')),
            ],
            options={
                'db_table': 'source_datapoint',
            },
        ),
        migrations.CreateModel(
            name='SourceIndicator',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('indicator_string', models.CharField(unique=True, max_length=255)),
                ('source_guid', models.CharField(max_length=255)),
                ('document', models.ForeignKey(to='source_data.Document')),
            ],
            options={
                'db_table': 'source_indicator',
            },
        ),
        migrations.CreateModel(
            name='SourceRegion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('region_code', models.CharField(unique=True, max_length=255)),
                ('lat', models.CharField(max_length=255, null=True)),
                ('lon', models.CharField(max_length=255, null=True)),
                ('parent_name', models.CharField(max_length=255, null=True)),
                ('parent_code', models.CharField(max_length=255, null=True)),
                ('region_type', models.CharField(max_length=255, null=True)),
                ('country', models.CharField(max_length=255, null=True)),
                ('source_guid', models.CharField(max_length=255)),
                ('document', models.ForeignKey(to='source_data.Document')),
            ],
            options={
                'db_table': 'source_region',
            },
        ),
        migrations.CreateModel(
            name='VCMSettlement',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('submissiondate', models.CharField(max_length=255)),
                ('deviceid', models.CharField(max_length=255)),
                ('simserial', models.CharField(max_length=255)),
                ('phonenumber', models.CharField(max_length=255)),
                ('daterecorded', models.CharField(max_length=255)),
                ('settlementcode', models.CharField(max_length=255)),
                ('settlementname', models.CharField(max_length=255)),
                ('vcmname', models.CharField(max_length=255)),
                ('vcmphone', models.CharField(max_length=255)),
                ('settlementgps_latitude', models.CharField(max_length=255)),
                ('settlementgps_longitude', models.CharField(max_length=255)),
                ('settlementgps_altitude', models.CharField(max_length=255)),
                ('settlementgps_accuracy', models.CharField(max_length=255)),
                ('meta_instanceid', models.CharField(max_length=255)),
                ('key', models.CharField(unique=True, max_length=255)),
                ('request_guid', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(default=datetime.datetime(2015, 8, 4, 19, 51, 28, 369314))),
                ('process_status', models.ForeignKey(to='source_data.ProcessStatus')),
            ],
            options={
                'db_table': 'odk_vcm_settlement',
            },
        ),
        migrations.AddField(
            model_name='regionmap',
            name='source_object',
            field=models.OneToOneField(to='source_data.SourceRegion'),
        ),
        migrations.AddField(
            model_name='indicatormap',
            name='source_object',
            field=models.OneToOneField(to='source_data.SourceIndicator'),
        ),
        migrations.AddField(
            model_name='campaignmap',
            name='source_object',
            field=models.OneToOneField(to='source_data.SourceCampaign'),
        ),
        migrations.AlterUniqueTogether(
            name='sourcedatapoint',
            unique_together=set([('source_guid', 'indicator_string')]),
        ),
        migrations.AlterUniqueTogether(
            name='document',
            unique_together=set([('docfile', 'doc_text')]),
        ),
    ]
