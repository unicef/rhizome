# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('rhizome', '0010_add_data_entry_document'),
    ]

    operations = [
        migrations.AddField(
            model_name='customdashboard',
            name='rows',
            field=jsonfield.fields.JSONField(null=True, blank=True),
        ),
    ]
