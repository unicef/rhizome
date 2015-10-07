# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('datapoints', '0014_indicator_bound'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomChart',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('chart_title', models.CharField(max_length=100)),
                ('chart_json', jsonfield.fields.JSONField()),
            ],
            options={
                'db_table': 'custom_chart',
            },
        ),
        migrations.RemoveField(
            model_name='customdashboard',
            name='dashboard_json',
        ),
        migrations.AddField(
            model_name='customchart',
            name='dashboard',
            field=models.ForeignKey(to='datapoints.CustomDashboard'),
        ),
    ]
