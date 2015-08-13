# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('source_data', '0005_auto_20150813_0223'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='documentdetail',
            options={'ordering': ['-master_dp_count']},
        ),
    ]
