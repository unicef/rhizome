# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('datapoints', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='indicator',
            name='bound_json',
            field=jsonfield.fields.JSONField(default=[]),
        ),
        migrations.AddField(
            model_name='indicator',
            name='office_id',
            field=jsonfield.fields.JSONField(default=[]),
        ),
        migrations.AddField(
            model_name='indicator',
            name='tag_json',
            field=jsonfield.fields.JSONField(default=[]),
        ),
    ]
