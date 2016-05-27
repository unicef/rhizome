# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rhizome', '0006_add_campaign_column'),
    ]

    operations = [
        migrations.RunSQL('''TRUNCATE TABLE custom_chart'''),
        migrations.CreateModel(
            name='ChartToDashboard',
            fields=[
                ('id', models.AutoField(verbose_name='ID',
                                        serialize=False, auto_created=True, primary_key=True)),
                ('sort_order', models.IntegerField(default=0)),
            ],
            options={
                'db_table': 'chart_to_dashboard',
            },
        ),
        migrations.RemoveField(
            model_name='customdashboard',
            name='default_office',
        ),
        migrations.AddField(
            model_name='customchart',
            name='uuid',
            field=models.CharField(default=1, unique=True, max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='charttodashboard',
            name='chart',
            field=models.ForeignKey(to='rhizome.CustomChart'),
        ),
        migrations.AddField(
            model_name='charttodashboard',
            name='dashboard',
            field=models.ForeignKey(to='rhizome.CustomDashboard'),
        ),
        migrations.AlterUniqueTogether(
            name='charttodashboard',
            unique_together=set([('chart', 'dashboard')]),
        ),
    ]
