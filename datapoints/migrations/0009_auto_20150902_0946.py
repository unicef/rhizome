# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('datapoints', '0008_auto_20150902_0944'),
    ]

    operations = [
        migrations.RenameField(
            model_name='campaignabstracted',
            old_name='campaign_type',
            new_name='campaign_type_id',
        ),
        migrations.RenameField(
            model_name='campaignabstracted',
            old_name='office',
            new_name='office_id',
        ),
        migrations.AlterUniqueTogether(
            name='campaignabstracted',
            unique_together=set([]),
        ),
    ]
