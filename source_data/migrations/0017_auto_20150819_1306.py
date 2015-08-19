# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('source_data', '0016_sourcesubmission_process_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='campaignmap',
            name='mapped_by',
        ),
        migrations.RemoveField(
            model_name='campaignmap',
            name='master_object',
        ),
        migrations.RemoveField(
            model_name='campaignmap',
            name='source_object',
        ),
        migrations.RemoveField(
            model_name='indicatormap',
            name='mapped_by',
        ),
        migrations.RemoveField(
            model_name='indicatormap',
            name='master_object',
        ),
        migrations.RemoveField(
            model_name='indicatormap',
            name='source_object',
        ),
        migrations.RemoveField(
            model_name='regionmap',
            name='mapped_by',
        ),
        migrations.RemoveField(
            model_name='regionmap',
            name='master_object',
        ),
        migrations.RemoveField(
            model_name='regionmap',
            name='source_object',
        ),
        migrations.RemoveField(
            model_name='sourcecampaign',
            name='document',
        ),
        migrations.AlterUniqueTogether(
            name='sourcedatapoint',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='sourcedatapoint',
            name='document',
        ),
        migrations.RemoveField(
            model_name='sourcedatapoint',
            name='status',
        ),
        migrations.RemoveField(
            model_name='sourceindicator',
            name='document',
        ),
        migrations.RemoveField(
            model_name='sourceregion',
            name='document',
        ),
        migrations.RemoveField(
            model_name='vcmsettlement',
            name='process_status',
        ),
        migrations.DeleteModel(
            name='CampaignMap',
        ),
        migrations.DeleteModel(
            name='IndicatorMap',
        ),
        migrations.DeleteModel(
            name='RegionMap',
        ),
        migrations.DeleteModel(
            name='SourceCampaign',
        ),
        migrations.DeleteModel(
            name='SourceDataPoint',
        ),
        migrations.DeleteModel(
            name='SourceIndicator',
        ),
        migrations.DeleteModel(
            name='SourceRegion',
        ),
        migrations.DeleteModel(
            name='VCMSettlement',
        ),
    ]
