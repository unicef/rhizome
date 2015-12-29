# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from source_data.models import DocDetailType

def forwards_func(apps, schema_editor):

    dtt = DocDetailType.objects.get(name='campaign_column')
    dtt.name = 'date_column'
    dtt.save()


class Migration(migrations.Migration):

    dependencies = [
        ('datapoints', '0038_top_lvl_indicator_tag'),
    ]

    operations = [
        migrations.RunPython(
            forwards_func
        ),
    ]
