# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('datapoints', '0009_indicator_map'),
    ]

    operations = [
        migrations.RunSQL('''

        DELETE FROM campaign CASCADE
        WHERE start_date < '2014-01-01';

        DROP TABLE IF EXISTS _all_campaigns;
        CREATE TABLE _all_campaigns
        AS
        SELECT
        	o.id as office_id
        	,REPLACE(o.name || '-' || CAST(first_of_the_month as varchar),' 00:00:00','') as slug
        	,first_of_the_month as start_date
        	,first_of_the_month as end_date
        	,1 as campaign_type_id
        FROM office o

        INNER JOIN (
        SELECT DATE '2014-01-01' + m*INTERVAL'1mon' as first_of_the_month
            FROM generate_series(0,20) m
        )x
        ON 1=1;

        INSERT INTO campaign
        (office_id, slug, start_date, end_date, campaign_type_id, created_at)
        SELECT
        	office_id, slug, start_date, end_date, campaign_type_id, now()
        FROM _all_campaigns ac
        WHERE NOT EXISTS (
        	SELECT 1 FROM campaign c
        	WHERE c.office_id = ac.office_id
        	AND c.start_date = ac.start_date

        );

        ''')

    ]
