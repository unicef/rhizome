# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('source_data', '0010_auto_20150815_1746'),
    ]

    operations = [
        migrations.AddField(
            model_name='sourceobjectmap',
            name='lastest_related_doc',
            field=models.ForeignKey(default=6, to='source_data.Document'),
            preserve_default=False,
        ),
    ]
