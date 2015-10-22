# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('datapoints', '0017_fix_campaign_dates'),
    ]

    operations = [
        migrations.DeleteModel(
            name='CampaignAbstracted',
        ),
    ]
