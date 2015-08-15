# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('source_data', '0011_sourceobjectmap_lastest_related_doc'),
    ]

    operations = [
        migrations.RenameField(
            model_name='sourceobjectmap',
            old_name='lastest_related_doc',
            new_name='document',
        ),
    ]
