# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('datapoints', '0019_docdatapoint'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='docdatapoint',
            unique_together=set([('source_submission', 'indicator')]),
        ),
    ]
