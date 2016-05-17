# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from rhizome.models import DataPoint, Campaign
from pandas import DataFrame
import math
import pandas as pd

def ingest_vcm_data(apps, schema_editor):
	pass

class Migration(migrations.Migration):

    dependencies = [
        ('rhizome', '0013_datapoint_unique_index'),
    ]

    operations = [
        migrations.RunPython(ingest_vcm_data),
    ]
