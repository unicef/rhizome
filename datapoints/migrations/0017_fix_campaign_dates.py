# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json

from django.db import models, migrations
from datapoints.models import CustomDashboard, CustomChart
import jsonfield.fields


class Migration(migrations.Migration):


    dependencies = [
        ('datapoints', '0016_remove_datapoint_abstracted'),
    ]

    operations = [
        migrations.RunSQL('''
            DROP TABLE IF EXISTS _campaign_fix_naija;
            CREATE TABLE _campaign_fix_naija (
                slug VARCHAR,
                new_date VARCHAR
            );

            INSERT INTO _campaign_fix_naija
            (slug, new_date)

            SELECT 'nigeria-april-2013','2013-04-01' UNION ALL
            SELECT 'nigeria-august-2013','2013-08-01' UNION ALL
            SELECT 'nigeria-december-2013','2013-12-01' UNION ALL
            SELECT 'nigeria-february-2013','2013-02-01' UNION ALL
            SELECT 'nigeria-january-2013','2013-01-01' UNION ALL
            SELECT 'nigeria-july-2013','2013-07-01' UNION ALL
            SELECT 'nigeria-june-2013','2013-06-01' UNION ALL
            SELECT 'nigeria-march-2013','2013-03-01' UNION ALL
            SELECT 'nigeria-may-2013','2013-05-01' UNION ALL
            SELECT 'nigeria-november-2013','2013-11-01' UNION ALL
            SELECT 'nigeria-october-2013','2013-10-01' UNION ALL
            SELECT 'nigeria-september-2013','2013-09-01' UNION ALL

            SELECT 'afghanistan-april-2013','2013-04-01' UNION ALL
            SELECT 'afghanistan-august-2013','2013-08-01' UNION ALL
            SELECT 'afghanistan-december-2013','2013-12-01' UNION ALL
            SELECT 'afghanistan-february-2013','2013-02-01' UNION ALL
            SELECT 'afghanistan-january-2013','2013-01-01' UNION ALL
            SELECT 'afghanistan-july-2013','2013-07-01' UNION ALL
            SELECT 'afghanistan-june-2013','2013-06-01' UNION ALL
            SELECT 'afghanistan-march-2013','2013-03-01' UNION ALL
            SELECT 'afghanistan-may-2013','2013-05-01' UNION ALL
            SELECT 'afghanistan-november-2013','2013-11-01' UNION ALL
            SELECT 'afghanistan-october-2013','2013-10-01' UNION ALL
            SELECT 'afghanistan-september-2013','2013-09-01' UNION ALL

            SELECT 'pakistan-april-2013','2013-04-01' UNION ALL
            SELECT 'pakistan-august-2013','2013-08-01' UNION ALL
            SELECT 'pakistan-december-2013','2013-12-01' UNION ALL
            SELECT 'pakistan-2013-02-01','2013-02-01' UNION ALL
            SELECT 'pakistan-2013-01-01','2013-01-01' UNION ALL
            SELECT 'pakistan-july-2013','2013-07-01' UNION ALL
            SELECT 'pakistan-june-2013','2013-06-01' UNION ALL
            SELECT 'pakistan-2013-03-01','2013-03-01' UNION ALL
            SELECT 'pakistan-may-2013','2013-05-01' UNION ALL
            SELECT 'pakistan-november-2013','2013-11-01' UNION ALL
            SELECT 'pakistan-october-2013','2013-10-01' UNION ALL
            SELECT 'pakistan-september-2013','2013-09-01';

            UPDATE campaign c
            SET start_date = CAST(f.new_date AS DATE)
            FROM _campaign_fix_naija f
            WHERE c.slug = f.slug;

            UPDATE campaign c
            SET start_date = CAST(f.new_date AS DATE)
            FROM _campaign_fix_naija f
            WHERE c.slug = f.slug;

            update campaign c
            SET end_date = start_date;

            DROP TABLE IF EXISTS _campaign_fix_naija;
        '''),
    ]
