# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('datapoints', '0024_remove_user_abstracted'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='locationtree',
            name='immediate_parent',
        ),
    ]
