# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('datapoints', '0016_remove_datapoint_abstracted'),
    ]

    operations = [
        migrations.DeleteModel(
            name='CampaignAbstracted',
        ),
    ]
