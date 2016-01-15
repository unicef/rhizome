# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('datapoints', '0004_remove_docdatapoint_is_valid'),
    ]

    operations = [
        migrations.AddField(
            model_name='cachejob',
            name='full_error_response',
            field=models.TextField(null=True),
        ),
    ]
