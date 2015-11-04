# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('datapoints', '0021_chart_type_schema_update'),
    ]

    operations = [
        migrations.AddField(
            model_name='indicator',
            name='data_format',
            field=models.CharField(default='int', max_length=10),
            preserve_default=False,
        ),
        migrations.RunSQL(
            '''
            -- bool --
            UPDATE indicator
            SET data_format = 'bool'
            WHERE short_name like '%(1=yes, 0=no)%';

            -- pct --
            UPDATE indicator
            SET data_format = 'pct'
            WHERE id in (
                SELECT indicator_id
                FROM datapoint_with_computed
                WHERE value >0 and value < 1
                GROUP BY indicator_id
            );
            '''
        ),
    ]
