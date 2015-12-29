# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('datapoints', '0037_data_date_date_time'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='historicaldatapointentry',
            name='campaign',
        ),
        migrations.AlterUniqueTogether(
            name='datapoint',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='datapoint',
            name='campaign',
        ),
    ]
