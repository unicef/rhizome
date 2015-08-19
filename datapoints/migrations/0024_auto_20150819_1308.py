# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('datapoints', '0023_auto_20150817_0939'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='expecteddata',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='expecteddata',
            name='campaign',
        ),
        migrations.RemoveField(
            model_name='expecteddata',
            name='parent_region',
        ),
        migrations.RemoveField(
            model_name='expecteddata',
            name='region',
        ),
        migrations.DeleteModel(
            name='ExpectedData',
        ),
    ]
