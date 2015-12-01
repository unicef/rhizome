# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('datapoints', '0032_useradminlevelpermissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='IndicatorToOffice',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('indicator', models.ForeignKey(to='datapoints.Indicator')),
                ('office', models.ForeignKey(to='datapoints.Office')),
            ],
            options={
                'db_table': 'indicator_to_office',
            },
        ),
    ]
