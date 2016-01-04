# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jsonfield.fields
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('source_data', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
            options={
                'db_table': 'auth_user_groups',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AggDataPoint',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('value', models.FloatField()),
            ],
            options={
                'db_table': 'agg_datapoint',
            },
        ),
        migrations.CreateModel(
            name='CacheJob',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_attempted', models.DateTimeField(auto_now=True)),
                ('date_completed', models.DateTimeField(null=True)),
                ('is_error', models.BooleanField()),
                ('response_msg', models.CharField(max_length=255)),
            ],
            options={
                'ordering': ('-date_attempted',),
                'db_table': 'cache_job',
            },
        ),
        migrations.CreateModel(
            name='CalculatedIndicatorComponent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
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
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
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
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('campaign', models.ForeignKey(to='datapoints.Campaign')),
            ],
            options={
                'db_table': 'campaign_to_indicator',
            },
        ),
        migrations.CreateModel(
            name='CampaignType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=55)),
            ],
            options={
                'db_table': 'campaign_type',
            },
        ),
        migrations.CreateModel(
            name='CustomChart',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('chart_json', jsonfield.fields.JSONField()),
            ],
            options={
                'db_table': 'custom_chart',
            },
        ),
        migrations.CreateModel(
            name='CustomDashboard',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(unique=True, max_length=255)),
                ('description', models.CharField(max_length=1000)),
                ('layout', models.IntegerField(default=0, null=True)),
            ],
            options={
                'db_table': 'custom_dashboard',
            },
        ),
        migrations.CreateModel(
            name='DataPoint',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('data_date', models.DateTimeField()),
                ('value', models.FloatField(null=True)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('cache_job', models.ForeignKey(default=-1, to='datapoints.CacheJob')),
                ('changed_by', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'datapoint',
            },
        ),
        migrations.CreateModel(
            name='DataPointComputed',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('value', models.FloatField()),
                ('cache_job', models.ForeignKey(default=-1, to='datapoints.CacheJob')),
                ('campaign', models.ForeignKey(to='datapoints.Campaign')),
            ],
            options={
                'db_table': 'datapoint_with_computed',
            },
        ),
        migrations.CreateModel(
            name='DocDataPoint',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('data_date', models.DateTimeField()),
                ('value', models.FloatField(null=True)),
                ('is_valid', models.BooleanField()),
                ('agg_on_location', models.BooleanField()),
                ('changed_by', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('document', models.ForeignKey(to='source_data.Document')),
            ],
            options={
                'db_table': 'doc_datapoint',
            },
        ),
        migrations.CreateModel(
            name='HistoricalDataPointEntry',
            fields=[
                ('id', models.IntegerField(verbose_name='ID', db_index=True, auto_created=True, blank=True)),
                ('data_date', models.DateTimeField()),
                ('value', models.FloatField(null=True)),
                ('created_at', models.DateTimeField(editable=False, blank=True)),
                ('history_id', models.AutoField(serialize=False, primary_key=True)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(max_length=1, choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')])),
                ('cache_job', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False, blank=True, to='datapoints.CacheJob', null=True)),
                ('changed_by', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False, blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('history_user', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
                'verbose_name': 'historical data point entry',
            },
        ),
        migrations.CreateModel(
            name='Indicator',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('short_name', models.CharField(unique=True, max_length=255)),
                ('name', models.CharField(unique=True, max_length=255)),
                ('description', models.CharField(max_length=255)),
                ('is_reported', models.BooleanField(default=True)),
                ('data_format', models.CharField(max_length=10)),
                ('created_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ('name',),
                'db_table': 'indicator',
            },
        ),
        migrations.CreateModel(
            name='IndicatorBound',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('mn_val', models.FloatField(null=True)),
                ('mx_val', models.FloatField(null=True)),
                ('bound_name', models.CharField(max_length=255)),
                ('direction', models.IntegerField(default=1)),
                ('indicator', models.ForeignKey(to='datapoints.Indicator')),
            ],
            options={
                'db_table': 'indicator_bound',
            },
        ),
        migrations.CreateModel(
            name='IndicatorTag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tag_name', models.CharField(max_length=255)),
                ('parent_tag', models.ForeignKey(to='datapoints.IndicatorTag', null=True)),
            ],
            options={
                'db_table': 'indicator_tag',
            },
        ),
        migrations.CreateModel(
            name='IndicatorToOffice',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('indicator', models.ForeignKey(to='datapoints.Indicator')),
            ],
            options={
                'db_table': 'indicator_to_office',
            },
        ),
        migrations.CreateModel(
            name='IndicatorToTag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('indicator', models.ForeignKey(to='datapoints.Indicator')),
                ('indicator_tag', models.ForeignKey(to='datapoints.IndicatorTag')),
            ],
            options={
                'ordering': ('-id',),
                'db_table': 'indicator_to_tag',
            },
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255)),
                ('location_code', models.CharField(unique=True, max_length=255)),
                ('latitude', models.FloatField(null=True, blank=True)),
                ('longitude', models.FloatField(null=True, blank=True)),
                ('created_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'location',
            },
        ),
        migrations.CreateModel(
            name='LocationPermission',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('top_lvl_location', models.ForeignKey(to='datapoints.Location')),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'location_permission',
            },
        ),
        migrations.CreateModel(
            name='LocationPolygon',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('geo_json', jsonfield.fields.JSONField()),
                ('location', models.OneToOneField(to='datapoints.Location')),
            ],
            options={
                'db_table': 'location_polygon',
            },
        ),
        migrations.CreateModel(
            name='LocationTree',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('lvl', models.IntegerField()),
                ('location', models.ForeignKey(to='datapoints.Location')),
                ('parent_location', models.ForeignKey(related_name='ultimate_parent', to='datapoints.Location')),
            ],
            options={
                'db_table': 'location_tree',
            },
        ),
        migrations.CreateModel(
            name='LocationType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
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
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('geo_json', jsonfield.fields.JSONField()),
                ('location', models.OneToOneField(to='datapoints.Location')),
            ],
            options={
                'db_table': 'min_polygon',
            },
        ),
        migrations.CreateModel(
            name='Office',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=55)),
                ('created_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'office',
                'permissions': (('view_office', 'View office'),),
            },
        ),
        migrations.AddField(
            model_name='location',
            name='location_type',
            field=models.ForeignKey(to='datapoints.LocationType'),
        ),
        migrations.AddField(
            model_name='location',
            name='office',
            field=models.ForeignKey(to='datapoints.Office'),
        ),
        migrations.AddField(
            model_name='location',
            name='parent_location',
            field=models.ForeignKey(to='datapoints.Location', null=True),
        ),
        migrations.AddField(
            model_name='indicatortooffice',
            name='office',
            field=models.ForeignKey(to='datapoints.Office'),
        ),
        migrations.AddField(
            model_name='historicaldatapointentry',
            name='indicator',
            field=models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False, blank=True, to='datapoints.Indicator', null=True),
        ),
        migrations.AddField(
            model_name='historicaldatapointentry',
            name='location',
            field=models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False, blank=True, to='datapoints.Location', null=True),
        ),
        migrations.AddField(
            model_name='historicaldatapointentry',
            name='source_submission',
            field=models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False, blank=True, to='source_data.SourceSubmission', null=True),
        ),
        migrations.AddField(
            model_name='docdatapoint',
            name='indicator',
            field=models.ForeignKey(to='datapoints.Indicator'),
        ),
        migrations.AddField(
            model_name='docdatapoint',
            name='location',
            field=models.ForeignKey(to='datapoints.Location'),
        ),
        migrations.AddField(
            model_name='docdatapoint',
            name='source_submission',
            field=models.ForeignKey(to='source_data.SourceSubmission'),
        ),
        migrations.AddField(
            model_name='datapointcomputed',
            name='indicator',
            field=models.ForeignKey(to='datapoints.Indicator'),
        ),
        migrations.AddField(
            model_name='datapointcomputed',
            name='location',
            field=models.ForeignKey(to='datapoints.Location'),
        ),
        migrations.AddField(
            model_name='datapoint',
            name='indicator',
            field=models.ForeignKey(to='datapoints.Indicator'),
        ),
        migrations.AddField(
            model_name='datapoint',
            name='location',
            field=models.ForeignKey(to='datapoints.Location'),
        ),
        migrations.AddField(
            model_name='datapoint',
            name='source_submission',
            field=models.ForeignKey(to='source_data.SourceSubmission'),
        ),
        migrations.AddField(
            model_name='customdashboard',
            name='default_office',
            field=models.ForeignKey(to='datapoints.Office', null=True),
        ),
        migrations.AddField(
            model_name='customdashboard',
            name='owner',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='customchart',
            name='dashboard',
            field=models.ForeignKey(to='datapoints.CustomDashboard'),
        ),
        migrations.AddField(
            model_name='campaigntoindicator',
            name='indicator',
            field=models.ForeignKey(to='datapoints.Indicator'),
        ),
        migrations.AddField(
            model_name='campaign',
            name='campaign_type',
            field=models.ForeignKey(to='datapoints.CampaignType'),
        ),
        migrations.AddField(
            model_name='campaign',
            name='office',
            field=models.ForeignKey(to='datapoints.Office'),
        ),
        migrations.AddField(
            model_name='campaign',
            name='top_lvl_indicator_tag',
            field=models.ForeignKey(to='datapoints.IndicatorTag'),
        ),
        migrations.AddField(
            model_name='campaign',
            name='top_lvl_location',
            field=models.ForeignKey(to='datapoints.Location'),
        ),
        migrations.AddField(
            model_name='calculatedindicatorcomponent',
            name='indicator',
            field=models.ForeignKey(related_name='indicator_master', to='datapoints.Indicator'),
        ),
        migrations.AddField(
            model_name='calculatedindicatorcomponent',
            name='indicator_component',
            field=models.ForeignKey(related_name='indicator_component', to='datapoints.Indicator'),
        ),
        migrations.AddField(
            model_name='aggdatapoint',
            name='cache_job',
            field=models.ForeignKey(default=-1, to='datapoints.CacheJob'),
        ),
        migrations.AddField(
            model_name='aggdatapoint',
            name='campaign',
            field=models.ForeignKey(to='datapoints.Campaign'),
        ),
        migrations.AddField(
            model_name='aggdatapoint',
            name='indicator',
            field=models.ForeignKey(to='datapoints.Indicator'),
        ),
        migrations.AddField(
            model_name='aggdatapoint',
            name='location',
            field=models.ForeignKey(to='datapoints.Location'),
        ),
        migrations.CreateModel(
            name='DataPointEntry',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('datapoints.datapoint',),
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
