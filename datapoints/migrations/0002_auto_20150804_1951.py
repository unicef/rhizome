# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('datapoints', '0001_initial'),
        ('source_data', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicaldatapointentry',
            name='source_datapoint',
            field=models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False, blank=True, to='source_data.SourceDataPoint', null=True),
        ),
        migrations.AddField(
            model_name='expecteddata',
            name='campaign',
            field=models.ForeignKey(to='datapoints.Campaign'),
        ),
        migrations.AddField(
            model_name='expecteddata',
            name='parent_region',
            field=models.ForeignKey(related_name='ex_parent_region', to='datapoints.Region'),
        ),
        migrations.AddField(
            model_name='expecteddata',
            name='region',
            field=models.ForeignKey(related_name='ex_child_region', to='datapoints.Region'),
        ),
        migrations.AddField(
            model_name='datapointcomputed',
            name='cache_job',
            field=models.ForeignKey(default=-1, to='datapoints.CacheJob'),
        ),
        migrations.AddField(
            model_name='datapointabstracted',
            name='cache_job',
            field=models.ForeignKey(default=-1, to='datapoints.CacheJob'),
        ),
        migrations.AddField(
            model_name='datapointabstracted',
            name='campaign',
            field=models.ForeignKey(to='datapoints.Campaign'),
        ),
        migrations.AddField(
            model_name='datapointabstracted',
            name='region',
            field=models.ForeignKey(to='datapoints.Region'),
        ),
        migrations.AddField(
            model_name='datapoint',
            name='cache_job',
            field=models.ForeignKey(default=-1, to='datapoints.CacheJob'),
        ),
        migrations.AddField(
            model_name='datapoint',
            name='campaign',
            field=models.ForeignKey(to='datapoints.Campaign'),
        ),
        migrations.AddField(
            model_name='datapoint',
            name='changed_by',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
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
            name='source_datapoint',
            field=models.ForeignKey(to='source_data.SourceDataPoint'),
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
            model_name='baddata',
            name='cache_job',
            field=models.ForeignKey(to='datapoints.CacheJob'),
        ),
        migrations.AddField(
            model_name='baddata',
            name='datapoint',
            field=models.ForeignKey(to='datapoints.DataPoint'),
        ),
        migrations.AddField(
            model_name='baddata',
            name='document',
            field=models.ForeignKey(to='source_data.Document'),
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
            name='indicatorpermission',
            unique_together=set([('group', 'indicator')]),
        ),
        migrations.AlterUniqueTogether(
            name='expecteddata',
            unique_together=set([('region', 'campaign')]),
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
