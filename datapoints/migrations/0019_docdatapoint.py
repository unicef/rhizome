# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('source_data', '0013_auto_20150816_0942'),
        ('datapoints', '0018_auto_20150816_1235'),
    ]

    operations = [
        migrations.CreateModel(
            name='DocDataPoint',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('value', models.FloatField(null=True)),
                ('is_valid', models.BooleanField()),
                ('campaign', models.ForeignKey(to='datapoints.Campaign')),
                ('changed_by', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('indicator', models.ForeignKey(to='datapoints.Indicator')),
                ('region', models.ForeignKey(to='datapoints.Region')),
                ('source_submission', models.ForeignKey(to='source_data.SourceSubmission')),
            ],
            options={
                'db_table': 'doc_datapoint',
            },
        ),
    ]
