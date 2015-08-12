# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('datapoints', '0013_auto_20150812_0821'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='indicatortotag',
            options={'ordering': ['-id']},
        ),
    ]
