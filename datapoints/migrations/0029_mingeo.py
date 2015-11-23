# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('datapoints', '0028_delete_indicatorabstracted'),
    ]

    operations = [
        migrations.CreateModel(
            name='MinGeo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('geo_json', jsonfield.fields.JSONField()),
                ('location', models.OneToOneField(to='datapoints.Location')),
            ],
            options={
                'db_table': 'min_polygon',
            },
        ),
    ]
