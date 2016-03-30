# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rhizome', '0005_reset_sql_sequence'),
    ]

    operations = [
        migrations.AddField(
            model_name='datapoint',
            name='campaign',
            field=models.ForeignKey(default=1, to='rhizome.Campaign'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='docdatapoint',
            name='campaign',
            field=models.ForeignKey(default=1, to='rhizome.Campaign'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='historicaldatapointentry',
            name='campaign',
            field=models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False, blank=True, to='rhizome.Campaign', null=True),
        ),
        migrations.AlterField(
            model_name='datapoint',
            name='data_date',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='docdatapoint',
            name='data_date',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='historicaldatapointentry',
            name='data_date',
            field=models.DateTimeField(null=True),
        ),
    ]
