# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('datapoints', '0002_indicator_json_fields'),
    ]

    operations = [
        migrations.RunSQL('''

        INSERT INTO location_type
        (name, admin_level)
        SELECT 'Planet', -1
        WHERE NOT EXISTS (
            SELECT 1 FROM location_type where name = 'Planet'
        );
        INSERT INTO location
        (name,location_code,slug,location_type_id,office_id,parent_location_id,created_at)

        SELECT 'Earth', 'Earth', 'earth', lt.id, 1, null, now()
        FROM location_type lt
        WHERE lt.name = 'Planet'
        AND NOT EXISTS (
            SELECT 1 FROM location where name = 'Earth'
        );

        UPDATE location l
        SET parent_location_id = earth.id
        FROM location earth
        WHERE earth.name = 'Earth'
        AND l.parent_location_id IS NULL
        AND l.name != 'Earth';

        UPDATE location_permission lp
        SET top_lvl_location_id = earth.id
        FROM location earth
        WHERE earth.name = 'Earth'
        AND lp.user_id = 1;
        ''')
    ]
