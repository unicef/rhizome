# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('source_data', '0006_auto_20150827_2253'),
    ]

    operations = [
        migrations.AddField(
            model_name='sourcesubmissiondetail',
            name='document_id',
            field=models.ForeignKey(default=20, to='source_data.Document'),
            preserve_default=False,
        ),
    ]
