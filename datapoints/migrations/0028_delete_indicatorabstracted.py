# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('datapoints', '0027_change_indicator_to_tag_order'),
    ]

    operations = [
        migrations.DeleteModel(
            name='IndicatorAbstracted',
        ),
    ]
