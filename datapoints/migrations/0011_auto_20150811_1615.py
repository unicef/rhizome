# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('datapoints', '0010_insert_indicator_tags'),
    ]

    operations = [
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
        migrations.AlterUniqueTogether(
            name='indicatortotag',
            unique_together=set([('indicator', 'indicator_tag')]),
        ),
    ]
