# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jsonfield.fields
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID',
                                        serialize=False, auto_created=True, primary_key=True)),
            ],
            options={
                'db_table': 'auth_user_groups',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AggDataPoint',
            fields=[
                ('id', models.AutoField(verbose_name='ID',
                                        serialize=False, auto_created=True, primary_key=True)),
                ('value', models.FloatField()),
            ],
            options={
                'db_table': 'agg_datapoint',
            },
        ),
        migrations.CreateModel(
            name='CalculatedIndicatorComponent',
            fields=[
                ('id', models.AutoField(verbose_name='ID',
                                        serialize=False, auto_created=True, primary_key=True)),
                ('calculation', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'calculated_indicator_component',
            },
        ),
        migrations.CreateModel(
            name='Campaign',
            fields=[
                ('id', models.AutoField(verbose_name='ID',
                                        serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('pct_complete', models.FloatField(default=0.001)),
                ('created_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ('-start_date',),
                'db_table': 'campaign',
            },
        ),
        migrations.CreateModel(
            name='CampaignToIndicator',
            fields=[
                ('id', models.AutoField(verbose_name='ID',
                                        serialize=False, auto_created=True, primary_key=True)),
                ('campaign', models.ForeignKey(to='rhizome.Campaign')),
            ],
            options={
                'db_table': 'campaign_to_indicator',
            },
        ),
        migrations.CreateModel(
            name='CampaignType',
            fields=[
                ('id', models.AutoField(verbose_name='ID',
                                        serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=55)),
            ],
            options={
                'db_table': 'campaign_type',
            },
        ),
        migrations.CreateModel(
            name='CustomChart',
            fields=[
                ('id', models.AutoField(verbose_name='ID',
                                        serialize=False, auto_created=True, primary_key=True)),
                ('uuid', models.CharField(unique=True, max_length=255)),
                ('title', models.CharField(unique=True, max_length=255)),
                ('chart_json', jsonfield.fields.JSONField()),
            ],
            options={
                'db_table': 'custom_chart',
            },
        ),
        migrations.CreateModel(
            name='CustomDashboard',
            fields=[
                ('id', models.AutoField(verbose_name='ID',
                                        serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(unique=True, max_length=255)),
                ('description', models.CharField(max_length=1000)),
                ('layout', models.IntegerField(default=0, null=True)),
                ('rows', jsonfield.fields.JSONField(null=True, blank=True)),
            ],
            options={
                'db_table': 'custom_dashboard',
            },
        ),
        migrations.CreateModel(
            name='DataPoint',
            fields=[
                ('id', models.AutoField(verbose_name='ID',
                                        serialize=False, auto_created=True, primary_key=True)),
                ('data_date', models.DateTimeField()),
                ('value', models.FloatField(null=True)),
                ('created_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'datapoint',
            },
        ),
        migrations.CreateModel(
            name='DataPointComputed',
            fields=[
                ('id', models.AutoField(verbose_name='ID',
                                        serialize=False, auto_created=True, primary_key=True)),
                ('value', models.FloatField()),
                ('campaign', models.ForeignKey(to='rhizome.Campaign')),
            ],
            options={
                'db_table': 'datapoint_with_computed',
            },
        ),
        migrations.CreateModel(
            name='DocDataPoint',
            fields=[
                ('id', models.AutoField(verbose_name='ID',
                                        serialize=False, auto_created=True, primary_key=True)),
                ('data_date', models.DateTimeField()),
                ('campaign', models.ForeignKey(to='rhizome.Campaign', null=True)),
                ('value', models.FloatField(null=True)),
                ('agg_on_location', models.BooleanField()),
            ],
            options={
                'db_table': 'doc_datapoint',
            },
        ),
        migrations.CreateModel(
            name='DocDetailType',
            fields=[
                ('id', models.AutoField(verbose_name='ID',
                                        serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255)),
            ],
            options={
                'db_table': 'doc_detail_type',
            },
        ),
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.AutoField(verbose_name='ID',
                                        serialize=False, auto_created=True, primary_key=True)),
                ('docfile', models.FileField(
                    null=True, upload_to=b'documents/%Y/%m/%d')),
                ('doc_title', models.TextField(unique=True)),
                ('file_header', jsonfield.fields.JSONField(null=True)),
                ('guid', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(
                    to=settings.AUTH_USER_MODEL, null=True)),
                ('file_type', models.CharField(default='campaign', max_length=10)),
                ],
            options={
                'ordering': ('-created_at',),
                'db_table': 'source_doc',
            },
        ),
        migrations.CreateModel(
            name='DocumentDetail',
            fields=[
                ('id', models.AutoField(verbose_name='ID',
                                        serialize=False, auto_created=True, primary_key=True)),
                ('doc_detail_value', models.CharField(max_length=255)),
                ('doc_detail_type', models.ForeignKey(to='rhizome.DocDetailType')),
                ('document', models.ForeignKey(to='rhizome.Document')),
            ],
            options={
                'db_table': 'doc_detail',
            },
        ),
        migrations.CreateModel(
            name='DocumentSourceObjectMap',
            fields=[
                ('id', models.AutoField(verbose_name='ID',
                                        serialize=False, auto_created=True, primary_key=True)),
                ('document', models.ForeignKey(to='rhizome.Document')),
            ],
            options={
                'db_table': 'doc_object_map',
            },
        ),
        migrations.CreateModel(
            name='Indicator',
            fields=[
                ('id', models.AutoField(verbose_name='ID',
                                        serialize=False, auto_created=True, primary_key=True)),
                ('short_name', models.CharField(unique=True, max_length=255)),
                ('name', models.CharField(unique=True, max_length=255)),
                ('description', models.CharField(max_length=255)),
                ('is_reported', models.BooleanField(default=True)),
                ('data_format', models.CharField(max_length=10)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('bound_json', jsonfield.fields.JSONField(default=[])),
                ('tag_json', jsonfield.fields.JSONField(default=[])),
                ('office_id', jsonfield.fields.JSONField(default=[])),
                ('good_bound', models.FloatField(null=True)),
                ('bad_bound', models.FloatField(null=True)),
                ('source_name', models.CharField(max_length=55)),
                ('resource_name', models.CharField(default=1, max_length=10)),
            ],
            options={
                'ordering': ('name',),
                'db_table': 'indicator',
            },
        ),
        migrations.CreateModel(
            name='IndicatorBound',
            fields=[
                ('id', models.AutoField(verbose_name='ID',
                                        serialize=False, auto_created=True, primary_key=True)),
                ('mn_val', models.FloatField(null=True)),
                ('mx_val', models.FloatField(null=True)),
                ('bound_name', models.CharField(max_length=255)),
                ('direction', models.IntegerField(default=1)),
                ('indicator', models.ForeignKey(to='rhizome.Indicator')),
            ],
            options={
                'db_table': 'indicator_bound',
            },
        ),
        migrations.CreateModel(
            name='IndicatorTag',
            fields=[
                ('id', models.AutoField(verbose_name='ID',
                                        serialize=False, auto_created=True, primary_key=True)),
                ('tag_name', models.CharField(max_length=255)),
                ('parent_tag', models.ForeignKey(
                    to='rhizome.IndicatorTag', null=True)),
            ],
            options={
                'db_table': 'indicator_tag',
            },
        ),
        migrations.CreateModel(
            name='IndicatorToTag',
            fields=[
                ('id', models.AutoField(verbose_name='ID',
                                        serialize=False, auto_created=True, primary_key=True)),
                ('indicator', models.ForeignKey(to='rhizome.Indicator')),
                ('indicator_tag', models.ForeignKey(to='rhizome.IndicatorTag')),
            ],
            options={
                'ordering': ('-id',),
                'db_table': 'indicator_to_tag',
            },
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(verbose_name='ID',
                                        serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255)),
                ('location_code', models.CharField(unique=True, max_length=255)),
                ('latitude', models.FloatField(null=True, blank=True)),
                ('longitude', models.FloatField(null=True, blank=True)),
                ('lpd_status', models.IntegerField(null=True, blank=True)),
                ('created_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'location',
            },
        ),
        migrations.CreateModel(
            name='LocationPermission',
            fields=[
                ('id', models.AutoField(verbose_name='ID',
                                        serialize=False, auto_created=True, primary_key=True)),
                ('top_lvl_location', models.ForeignKey(to='rhizome.Location')),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'location_permission',
            },
        ),
        migrations.CreateModel(
            name='LocationPolygon',
            fields=[
                ('id', models.AutoField(verbose_name='ID',
                                        serialize=False, auto_created=True, primary_key=True)),
                ('geo_json', jsonfield.fields.JSONField()),
                ('location', models.OneToOneField(to='rhizome.Location')),
            ],
            options={
                'db_table': 'location_polygon',
            },
        ),
        migrations.CreateModel(
            name='LocationTree',
            fields=[
                ('id', models.AutoField(verbose_name='ID',
                                        serialize=False, auto_created=True, primary_key=True)),
                ('lvl', models.IntegerField()),
                ('location', models.ForeignKey(to='rhizome.Location')),
                ('parent_location', models.ForeignKey(
                    related_name='ultimate_parent', to='rhizome.Location')),
            ],
            options={
                'db_table': 'location_tree',
            },
        ),
        migrations.CreateModel(
            name='LocationType',
            fields=[
                ('id', models.AutoField(verbose_name='ID',
                                        serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=55)),
                ('admin_level', models.IntegerField(unique=True)),
            ],
            options={
                'db_table': 'location_type',
            },
        ),
        migrations.CreateModel(
            name='MinGeo',
            fields=[
                ('id', models.AutoField(verbose_name='ID',
                                        serialize=False, auto_created=True, primary_key=True)),
                ('geo_json', jsonfield.fields.JSONField()),
                ('location', models.OneToOneField(to='rhizome.Location')),
            ],
            options={
                'db_table': 'min_polygon',
            },
        ),
        migrations.CreateModel(
            name='Office',
            fields=[
                ('id', models.AutoField(verbose_name='ID',
                                        serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=55)),
                ('created_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'office',
                'permissions': (('view_office', 'View office'),),
            },
        ),
        migrations.CreateModel(
            name='SourceObjectMap',
            fields=[
                ('id', models.AutoField(verbose_name='ID',
                                        serialize=False, auto_created=True, primary_key=True)),
                ('master_object_id', models.IntegerField()),
                ('master_object_name', models.CharField(max_length=255, null=True)),
                ('source_object_code', models.CharField(max_length=255)),
                ('content_type', models.CharField(max_length=20)),
                ('mapped_by', models.ForeignKey(
                    to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'db_table': 'source_object_map',
            },
        ),
        migrations.CreateModel(
            name='SourceSubmission',
            fields=[
                ('id', models.AutoField(verbose_name='ID',
                                        serialize=False, auto_created=True, primary_key=True)),
                ('instance_guid', models.CharField(max_length=255)),
                ('row_number', models.IntegerField()),
                ('data_date', models.DateTimeField(null=True)),
                ('location_code', models.CharField(max_length=1000)),
                ('campaign_code', models.CharField(max_length=1000)),
                ('location_display', models.CharField(max_length=1000)),
                ('submission_json', jsonfield.fields.JSONField()),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('process_status', models.CharField(max_length=25)),
                ('document', models.ForeignKey(to='rhizome.Document')),
            ],
            options={
                'db_table': 'source_submission',
            },
        ),
        migrations.AddField(
            model_name='location',
            name='location_type',
            field=models.ForeignKey(to='rhizome.LocationType'),
        ),
        migrations.AddField(
            model_name='location',
            name='office',
            field=models.ForeignKey(to='rhizome.Office'),
        ),
        migrations.AddField(
            model_name='location',
            name='parent_location',
            field=models.ForeignKey(to='rhizome.Location', null=True),
        ),
        migrations.AddField(
            model_name='documentsourceobjectmap',
            name='source_object_map',
            field=models.ForeignKey(to='rhizome.SourceObjectMap'),
        ),
        migrations.AddField(
            model_name='docdatapoint',
            name='document',
            field=models.ForeignKey(to='rhizome.Document'),
        ),
        migrations.AddField(
            model_name='docdatapoint',
            name='indicator',
            field=models.ForeignKey(to='rhizome.Indicator'),
        ),
        migrations.AddField(
            model_name='docdatapoint',
            name='location',
            field=models.ForeignKey(to='rhizome.Location'),
        ),
        migrations.AddField(
            model_name='docdatapoint',
            name='source_submission',
            field=models.ForeignKey(to='rhizome.SourceSubmission'),
        ),
        migrations.AddField(
            model_name='datapointcomputed',
            name='indicator',
            field=models.ForeignKey(to='rhizome.Indicator'),
        ),
        migrations.AddField(
            model_name='datapointcomputed',
            name='location',
            field=models.ForeignKey(to='rhizome.Location'),
        ),
        migrations.AddField(
            model_name='datapointcomputed',
            name='document',
            field=models.ForeignKey(to='rhizome.Document'),
        ),
        migrations.AddField(
            model_name='datapoint',
            name='indicator',
            field=models.ForeignKey(to='rhizome.Indicator'),
        ),
        migrations.AddField(
            model_name='datapoint',
            name='location',
            field=models.ForeignKey(to='rhizome.Location'),
        ),
        migrations.AddField(
            model_name='datapoint',
            name='campaign',
            field=models.ForeignKey(to='rhizome.Campaign', null=True),
        ),
        migrations.AddField(
            model_name='datapoint',
            name='source_submission',
            field=models.ForeignKey(to='rhizome.SourceSubmission'),
        ),
        migrations.AddField(
            model_name='datapoint',
            name='unique_index',
            field=models.CharField(default=-1, unique=True, max_length=255),
        ),
        migrations.AddField(
            model_name='campaigntoindicator',
            name='indicator',
            field=models.ForeignKey(to='rhizome.Indicator'),
        ),
        migrations.AddField(
            model_name='campaign',
            name='campaign_type',
            field=models.ForeignKey(to='rhizome.CampaignType'),
        ),
        migrations.AddField(
            model_name='campaign',
            name='office',
            field=models.ForeignKey(to='rhizome.Office'),
        ),
        migrations.AddField(
            model_name='campaign',
            name='top_lvl_indicator_tag',
            field=models.ForeignKey(to='rhizome.IndicatorTag'),
        ),
        migrations.AddField(
            model_name='campaign',
            name='top_lvl_location',
            field=models.ForeignKey(to='rhizome.Location'),
        ),
        migrations.AddField(
            model_name='calculatedindicatorcomponent',
            name='indicator',
            field=models.ForeignKey(
                related_name='indicator_master', to='rhizome.Indicator'),
        ),
        migrations.AddField(
            model_name='calculatedindicatorcomponent',
            name='indicator_component',
            field=models.ForeignKey(
                related_name='indicator_component', to='rhizome.Indicator'),
        ),
        migrations.AddField(
            model_name='aggdatapoint',
            name='campaign',
            field=models.ForeignKey(to='rhizome.Campaign'),
        ),
        migrations.AddField(
            model_name='aggdatapoint',
            name='indicator',
            field=models.ForeignKey(to='rhizome.Indicator'),
        ),
        migrations.AddField(
            model_name='aggdatapoint',
            name='location',
            field=models.ForeignKey(to='rhizome.Location'),
        ),
        migrations.CreateModel(
            name='DataPointEntry',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('rhizome.datapoint',),
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
            name='locationtree',
            unique_together=set([('parent_location', 'location')]),
        ),
        migrations.AlterUniqueTogether(
            name='indicatortotag',
            unique_together=set([('indicator', 'indicator_tag')]),
        ),
        migrations.AlterUniqueTogether(
            name='documentsourceobjectmap',
            unique_together=set([('document', 'source_object_map')]),
        ),
        migrations.AlterUniqueTogether(
            name='documentdetail',
            unique_together=set([('document', 'doc_detail_type')]),
        ),
        migrations.AlterUniqueTogether(
            name='datapointcomputed',
            unique_together=set([('location', 'campaign', 'indicator')]),
        ),
        migrations.AlterUniqueTogether(
            name='campaigntoindicator',
            unique_together=set([('indicator', 'campaign')]),
        ),
        migrations.AlterUniqueTogether(
            name='campaign',
            unique_together=set([('office', 'start_date')]),
        ),
        migrations.AlterUniqueTogether(
            name='aggdatapoint',
            unique_together=set([('location', 'campaign', 'indicator')]),
        ),
    ]
