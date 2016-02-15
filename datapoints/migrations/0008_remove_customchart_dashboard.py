# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('datapoints', '0007_remove_campaign_slug'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customchart',
            name='dashboard',
        ),
    ]
