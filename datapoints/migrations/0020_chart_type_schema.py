# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('datapoints', '0019_campaign_management_dash_pct_complete'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChartType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255)),
            ],
            options={
                'db_table': 'chart_type',
            },
        ),
        migrations.CreateModel(
            name='ChartTypeToIndicator',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('chart_type', models.ForeignKey(related_name='chart_type', to='datapoints.ChartType')),
                ('indicator', models.ForeignKey(related_name='indicator', to='datapoints.Indicator')),
            ],
            options={
                'db_table': 'chart_type_to_indicator',
            },
        ),
        migrations.AlterField(
            model_name='campaign',
            name='management_dash_pct_complete',
            field=models.FloatField(default=0.001),
        ),
        migrations.AlterUniqueTogether(
            name='charttypetoindicator',
            unique_together=set([('indicator', 'chart_type')]),
        ),
    ]
