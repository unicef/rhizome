# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models, migrations
from os import path

SQL_DIR = path.join(path.dirname(path.dirname(path.abspath(__file__))), 'sql')


def readSQLFromFile(filename):
    return open(path.join(SQL_DIR, filename), 'r').read()


class Migration(migrations.Migration):
    dependencies = [
        ('datapoints', '0001_initial'),
        ('datapoints', '0002_load_base_metadata'),
        ('datapoints', '0003_load_ng_regions'),
        ('datapoints', '0004_load_indicators_campaigns_permissions'),
        ('datapoints', '0005_cache_and_cleanup_metadata'),
    ]

    operations = [
        migrations.RunSQL(readSQLFromFile('functions/fn_agg_datapoint.sql')),
        migrations.RunSQL(readSQLFromFile('functions/fn_test_data_accuracy.sql')),

        migrations.RunSQL(readSQLFromFile('functions/fn_calc_prep.sql')),
        migrations.RunSQL(readSQLFromFile('functions/fn_calc_sum_of_parts.sql')),
        migrations.RunSQL(readSQLFromFile('functions/fn_calc_part_over_whole.sql')),
        migrations.RunSQL(readSQLFromFile('functions/fn_calc_part_of_difference.sql')),
        migrations.RunSQL(readSQLFromFile('functions/fn_calc_upsert_computed.sql')),
        migrations.RunSQL(readSQLFromFile('functions/fn_calc_datapoint.sql')),
        migrations.RunSQL(readSQLFromFile('functions/fn_get_authorized_regions_by_user.sql'))
    ]
