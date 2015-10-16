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
        SELECT 'nigeria-september-2013','2013-09-01';

        UPDATE campaign c
        SET start_date = CAST(f.new_date AS DATE)
        FROM _campaign_fix_naija f
        WHERE c.slug = f.slug;

        DROP TABLE IF EXISTS _campaign_fix_naija;
        '''),
    ]
