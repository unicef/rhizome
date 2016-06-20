# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rhizome', '0015_update_unique_index'),
    ]

    operations = [
        migrations.AddField(
            model_name='indicator',
            name='resource_name',
            field=models.CharField(default=1, max_length=10),
            preserve_default=False,
        ),
        migrations.RunSQL('''

            -- This says, anything that is the result of another
            -- calculation is a campaign indicator.

            UPDATE indicator ind
            SET resource_name = x.resource_name
            FROM (

                SELECT id, 'campaign' as resource_name
                FROM indicator ind
                WHERE NOT EXISTS (
                    SELECT 1 FROM calculated_indicator_component cic
                    WHERE ind.id = cic.indicator_id
                )

                UNION ALL

                SELECT id, 'data_date'
                FROM indicator ind
                WHERE NOT EXISTS (
                    SELECT 1 FROM calculated_indicator_component cic
                    WHERE ind.id = cic.indicator_id
                )
            ) x
            WHERE ind.id = x.id;

        '''),
    ]
