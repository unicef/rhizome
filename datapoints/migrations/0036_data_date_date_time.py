# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('datapoints', '0035_migrate_datadate_data'),
    ]

    operations = [
        migrations.AlterField(
            model_name='datapoint',
            name='data_date',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='historicaldatapointentry',
            name='data_date',
            field=models.DateTimeField(),
        ),
    ]
