# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('source_data', '0014_auto_20150817_0915'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sourceobjectmap',
            name='document',
        ),
    ]
