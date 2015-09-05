# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import autoslug.fields
import jsonfield.fields
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('auth', '0006_require_contenttypes_0002'),
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
                ('region_id', models.IntegerField()),
                ('campaign_id', models.IntegerField()),
                ('indicator_id', models.IntegerField()),
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
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('slug', autoslug.fields.AutoSlugField(populate_from=b'get_full_name', unique=True, editable=False)),
                ('created_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ('-start_date',),
                'db_table': 'campaign',
            },
        ),
        migrations.CreateModel(
            name='CampaignAbstracted',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('slug', autoslug.fields.AutoSlugField(populate_from=b'get_full_name', unique=True, editable=False)),
                ('pct_complete', models.FloatField()),
                ('created_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ('-start_date',),
                'db_table': 'campaign_abstracted',
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
            name='CustomDashboard',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(unique=True, max_length=255)),
                ('description', models.CharField(max_length=1000)),
                ('dashboard_json', jsonfield.fields.JSONField(null=True)),
            ],
            options={
                'db_table': 'custom_dashboard',
            },
        ),
        migrations.CreateModel(
            name='DataPoint',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('value', models.FloatField(null=True)),
                ('note', models.CharField(max_length=255, null=True, blank=True)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('cache_job', models.ForeignKey(default=-1, to='datapoints.CacheJob')),
                ('campaign', models.ForeignKey(to='datapoints.Campaign')),
                ('changed_by', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['region', 'campaign'],
                'db_table': 'datapoint',
                'permissions': (('view_datapoint', 'View datapoint'),),
            },
        ),
        migrations.CreateModel(
            name='DataPointAbstracted',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('indicator_json', jsonfield.fields.JSONField()),
                ('cache_job', models.ForeignKey(default=-1, to='datapoints.CacheJob')),
                ('campaign', models.ForeignKey(to='datapoints.Campaign')),
            ],
            options={
                'db_table': 'datapoint_abstracted',
            },
        ),
        migrations.CreateModel(
            name='DataPointComputed',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('region_id', models.IntegerField()),
                ('campaign_id', models.IntegerField()),
                ('indicator_id', models.IntegerField()),
                ('value', models.FloatField()),
                ('cache_job', models.ForeignKey(default=-1, to='datapoints.CacheJob')),
            ],
            options={
                'db_table': 'datapoint_with_computed',
            },
        ),
        migrations.CreateModel(
            name='DocDataPoint',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('value', models.FloatField(null=True)),
                ('is_valid', models.BooleanField()),
                ('agg_on_region', models.BooleanField()),
                ('campaign', models.ForeignKey(to='datapoints.Campaign')),
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
                ('value', models.FloatField(null=True)),
                ('note', models.CharField(max_length=255, null=True, blank=True)),
                ('created_at', models.DateTimeField(editable=False, blank=True)),
                ('history_id', models.AutoField(serialize=False, primary_key=True)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(max_length=1, choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')])),
                ('cache_job', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False, blank=True, to='datapoints.CacheJob', null=True)),
                ('campaign', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False, blank=True, to='datapoints.Campaign', null=True)),
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
                ('slug', autoslug.fields.AutoSlugField(populate_from=b'name', unique=True, editable=False)),
                ('created_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ('name',),
                'db_table': 'indicator',
            },
        ),
        migrations.CreateModel(
            name='IndicatorAbstracted',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', models.CharField(max_length=255)),
                ('short_name', models.CharField(max_length=255)),
                ('slug', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('bound_json', jsonfield.fields.JSONField()),
                ('tag_json', jsonfield.fields.JSONField()),
            ],
            options={
                'db_table': 'indicator_abstracted',
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
            name='IndicatorPermission',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('group', models.ForeignKey(to='auth.Group')),
                ('indicator', models.ForeignKey(to='datapoints.Indicator')),
            ],
            options={
                'db_table': 'indicator_permission',
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
            name='IndicatorToTag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('indicator', models.ForeignKey(to='datapoints.Indicator')),
                ('indicator_tag', models.ForeignKey(to='datapoints.IndicatorTag')),
            ],
            options={
                'ordering': ['-id'],
                'db_table': 'indicator_to_tag',
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
        migrations.CreateModel(
            name='ReconData',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('target_value', models.FloatField()),
                ('campaign', models.ForeignKey(to='datapoints.Campaign')),
                ('indicator', models.ForeignKey(to='datapoints.Indicator')),
            ],
            options={
                'db_table': 'recon_data',
            },
        ),
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255)),
                ('region_code', models.CharField(unique=True, max_length=255)),
                ('latitude', models.FloatField(null=True, blank=True)),
                ('longitude', models.FloatField(null=True, blank=True)),
                ('slug', autoslug.fields.AutoSlugField(populate_from=b'name', unique=True, editable=False)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('office', models.ForeignKey(to='datapoints.Office')),
                ('parent_region', models.ForeignKey(to='datapoints.Region', null=True)),
            ],
            options={
                'db_table': 'region',
            },
        ),
        migrations.CreateModel(
            name='RegionPermission',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('read_write', models.CharField(max_length=1)),
                ('region', models.ForeignKey(to='datapoints.Region')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'region_permission',
            },
        ),
        migrations.CreateModel(
            name='RegionPolygon',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('geo_json', jsonfield.fields.JSONField()),
                ('region', models.OneToOneField(to='datapoints.Region')),
            ],
            options={
                'db_table': 'region_polygon',
            },
        ),
        migrations.CreateModel(
            name='RegionTree',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('lvl', models.IntegerField()),
                ('immediate_parent', models.ForeignKey(related_name='immediate_parent', to='datapoints.Region')),
                ('parent_region', models.ForeignKey(related_name='ultimate_parent', to='datapoints.Region')),
                ('region', models.ForeignKey(to='datapoints.Region')),
            ],
            options={
                'db_table': 'region_tree',
            },
        ),
        migrations.CreateModel(
            name='RegionType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=55)),
            ],
            options={
                'db_table': 'region_type',
            },
        ),
        migrations.CreateModel(
            name='Responsibility',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('indicator', models.ForeignKey(to='datapoints.Indicator')),
                ('region', models.ForeignKey(to='datapoints.Region')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('indicator',),
                'db_table': 'responsibility',
            },
        ),
        migrations.CreateModel(
            name='UserAbstracted',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('last_login', models.DateTimeField()),
                ('is_superuser', models.BooleanField()),
                ('username', models.CharField(max_length=255)),
                ('first_name', models.CharField(max_length=255)),
                ('last_name', models.BooleanField()),
                ('email', models.CharField(max_length=255)),
                ('is_staff', models.BooleanField()),
                ('is_active', models.BooleanField()),
                ('date_joined', models.DateTimeField()),
                ('group_json', jsonfield.fields.JSONField()),
                ('region_permission_json', jsonfield.fields.JSONField()),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'user_abstracted',
            },
        ),
        migrations.AddField(
            model_name='region',
            name='region_type',
            field=models.ForeignKey(to='datapoints.RegionType'),
        ),
        migrations.AddField(
            model_name='recondata',
            name='region',
            field=models.ForeignKey(to='datapoints.Region'),
        ),
        migrations.AddField(
            model_name='historicaldatapointentry',
            name='indicator',
            field=models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False, blank=True, to='datapoints.Indicator', null=True),
        ),
        migrations.AddField(
            model_name='historicaldatapointentry',
            name='region',
            field=models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False, blank=True, to='datapoints.Region', null=True),
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
            name='region',
            field=models.ForeignKey(to='datapoints.Region'),
        ),
        migrations.AddField(
            model_name='docdatapoint',
            name='source_submission',
            field=models.ForeignKey(to='source_data.SourceSubmission'),
        ),
        migrations.AddField(
            model_name='datapointabstracted',
            name='region',
            field=models.ForeignKey(to='datapoints.Region'),
        ),
        migrations.AddField(
            model_name='datapoint',
            name='indicator',
            field=models.ForeignKey(to='datapoints.Indicator'),
        ),
        migrations.AddField(
            model_name='datapoint',
            name='region',
            field=models.ForeignKey(to='datapoints.Region'),
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
            model_name='campaignabstracted',
            name='campaign_type',
            field=models.ForeignKey(to='datapoints.CampaignType'),
        ),
        migrations.AddField(
            model_name='campaignabstracted',
            name='office',
            field=models.ForeignKey(to='datapoints.Office'),
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
            name='responsibility',
            unique_together=set([('user', 'indicator', 'region')]),
        ),
        migrations.AlterUniqueTogether(
            name='regiontree',
            unique_together=set([('parent_region', 'region')]),
        ),
        migrations.AlterUniqueTogether(
            name='regionpermission',
            unique_together=set([('user', 'region', 'read_write')]),
        ),
        migrations.AlterUniqueTogether(
            name='region',
            unique_together=set([('name', 'region_type', 'office')]),
        ),
        migrations.AlterUniqueTogether(
            name='recondata',
            unique_together=set([('region', 'campaign', 'indicator')]),
        ),
        migrations.AlterUniqueTogether(
            name='indicatortotag',
            unique_together=set([('indicator', 'indicator_tag')]),
        ),
        migrations.AlterUniqueTogether(
            name='indicatorpermission',
            unique_together=set([('group', 'indicator')]),
        ),
        migrations.AlterUniqueTogether(
            name='datapointcomputed',
            unique_together=set([('region_id', 'campaign_id', 'indicator_id')]),
        ),
        migrations.AlterUniqueTogether(
            name='datapointabstracted',
            unique_together=set([('region', 'campaign')]),
        ),
        migrations.AlterUniqueTogether(
            name='datapoint',
            unique_together=set([('indicator', 'region', 'campaign')]),
        ),
        migrations.AlterUniqueTogether(
            name='campaignabstracted',
            unique_together=set([('office', 'start_date')]),
        ),
        migrations.AlterUniqueTogether(
            name='campaign',
            unique_together=set([('office', 'start_date')]),
        ),
        migrations.AlterUniqueTogether(
            name='aggdatapoint',
            unique_together=set([('region_id', 'campaign_id', 'indicator_id')]),
        ),
    ]
