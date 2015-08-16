# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('source_data', '0013_auto_20150816_0942'),
        ('datapoints', '0017_delete_columnattributes'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='datapoint',
            name='source_datapoint',
        ),
        migrations.RemoveField(
            model_name='historicaldatapointentry',
            name='source_datapoint',
        ),
        migrations.AddField(
            model_name='datapoint',
            name='source_submission',
            field=models.ForeignKey(default=1, to='source_data.SourceSubmission'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='historicaldatapointentry',
            name='source_submission',
            field=models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False, blank=True, to='source_data.SourceSubmission', null=True),
        ),
    ]
