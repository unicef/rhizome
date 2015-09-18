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
            name='source_submission',
            field=models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False, blank=True, to='source_data.SourceSubmission', null=True),
        ),
        migrations.AddField(
            model_name='docdatapoint',
            name='changed_by',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='docdatapoint',
            name='document',
            field=models.ForeignKey(to='source_data.Document'),
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
            name='campaign',
            field=models.ForeignKey(to='datapoints.Campaign'),
        ),
        migrations.AddField(
            model_name='docdatapoint',
            name='source_submission',
            field=models.ForeignKey(to='source_data.SourceSubmission'),
        ),
        migrations.AddField(
            model_name='datapointcomputed',
            name='cache_job',
            field=models.ForeignKey(default=-1, to='datapoints.CacheJob'),
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
            model_name='datapointcomputed',
            name='campaign',
            field=models.ForeignKey(to='datapoints.Campaign'),
        ),
        migrations.AddField(
            model_name='datapointabstracted',
            name='cache_job',
            field=models.ForeignKey(default=-1, to='datapoints.CacheJob'),
        ),
        migrations.AddField(
            model_name='datapointabstracted',
            name='location',
            field=models.ForeignKey(to='datapoints.Location'),
        ),
        migrations.AddField(
            model_name='datapointabstracted',
            name='campaign',
            field=models.ForeignKey(to='datapoints.Campaign'),
        ),
        migrations.AddField(
            model_name='datapoint',
            name='cache_job',
            field=models.ForeignKey(default=-1, to='datapoints.CacheJob'),
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
            name='location',
            field=models.ForeignKey(to='datapoints.Location'),
        ),
        migrations.AddField(
            model_name='datapoint',
            name='campaign',
            field=models.ForeignKey(to='datapoints.Campaign'),
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
            name='indicator',
            field=models.ForeignKey(to='datapoints.Indicator'),
        ),
        migrations.AddField(
            model_name='aggdatapoint',
            name='location',
            field=models.ForeignKey(to='datapoints.Location'),
        ),
        migrations.AddField(
            model_name='aggdatapoint',
            name='campaign',
            field=models.ForeignKey(to='datapoints.Campaign'),
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
            name='Campaign',
            unique_together=set([('office', 'start_date')]),
        ),
        migrations.AlterUniqueTogether(
            name='locationtree',
            unique_together=set([('parent_location', 'location')]),
        ),
        migrations.AlterUniqueTogether(
            name='locationpermission',
            unique_together=set([('user', 'location', 'read_write')]),
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
            unique_together=set([('location', 'campaign', 'indicator')]),
        ),
        migrations.AlterUniqueTogether(
            name='datapointabstracted',
            unique_together=set([('location', 'campaign')]),
        ),
        migrations.AlterUniqueTogether(
            name='datapoint',
            unique_together=set([('indicator', 'location', 'campaign')]),
        ),
        migrations.AlterUniqueTogether(
            name='aggdatapoint',
            unique_together=set([('location', 'campaign', 'indicator')]),
        ),
    ]
