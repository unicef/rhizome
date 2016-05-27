# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rhizome', '0007_chart_to_dashboard'),
    ]

    operations = [
        migrations.CreateModel(
            name='IndicatorClassMap',
            fields=[
                ('id', models.AutoField(verbose_name='ID',
                                        serialize=False, auto_created=True, primary_key=True)),
                ('string_value', models.CharField(max_length=100)),
                ('enum_value', models.IntegerField()),
                ('is_display', models.BooleanField()),
                ('indicator', models.ForeignKey(to='rhizome.Indicator')),
            ],
            options={
                'db_table': 'indicator_class_map',
            },
        ),
        migrations.AlterUniqueTogether(
            name='indicatorclassmap',
            unique_together=set([('indicator', 'string_value', 'enum_value')]),
        ),
    ]
