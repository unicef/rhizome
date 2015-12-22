# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations, transaction

from datapoints.models import Campaign, Location, DataPointComputed, \
    CampaignToIndicator, DataPoint

class Migration(migrations.Migration):

    dependencies = [
        ('datapoints', '0033_indicatortooffice'),
    ]

    operations = [
        migrations.CreateModel(
            name='CampaignToIndicator',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
            options={
                'db_table': 'campaign_to_indicator',
            },
        ),
        migrations.AddField(
            model_name='campaign',
            name='name',
            field=models.CharField(default='tmp_campaign_name', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='campaign',
            name='top_lvl_location',
            field=models.ForeignKey(default=1, to='datapoints.Location'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='datapoint',
            name='data_date',
            field=models.DateField(default='2015-01-01'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='historicaldatapointentry',
            name='data_date',
            field=models.DateField(default='2015-01-01'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='campaigntoindicator',
            name='campaign',
            field=models.ForeignKey(to='datapoints.Campaign'),
        ),
        migrations.AddField(
            model_name='campaigntoindicator',
            name='indicator',
            field=models.ForeignKey(to='datapoints.Indicator'),
        ),
        migrations.RenameField(
            model_name='campaign',
            old_name='management_dash_pct_complete',
            new_name='pct_complete',
        ),
        migrations.AlterUniqueTogether(
            name='campaigntoindicator',
            unique_together=set([('indicator', 'campaign')]),
        ),
    ]
