# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from rhizome.models import DataPoint, Campaign
from pandas import DataFrame
import math
import pandas as pd


class Migration(migrations.Migration):

    dependencies = [
        ('rhizome', '0012_datapoint_campaign_nullable'),
    ]

    operations = [
        migrations.AddField(
            model_name='datapoint',
            name='unique_index',
            field=models.CharField(default=-1, max_length=255),
        ),
        migrations.AddField(
            model_name='historicaldatapointentry',
            name='unique_index',
            field=models.CharField(default=-1, max_length=255, db_index=True),
        ),
    ]
