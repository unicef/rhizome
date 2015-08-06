# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('datapoints', '0007_load_indicator_map'),
    ]

    operations = [

        migrations.RunSQL("""

        INSERT INTO auth_group
        (name)
        SELECT 'can_edit_all_indicators';

        INSERT INTO auth_user_groups
        (user_id,group_id)
        SELECT au.id,ag.id FROM auth_user au
        INNER JOIN auth_group ag
        ON ag.name = 'can_edit_all_indicators';

    	INSERT INTO indicator_permission
    	(group_id, indicator_id)

    	SELECT ag.id, i.id FROM indicator i
    	INNER JOIN auth_group ag
    	ON ag.name = 'can_edit_all_indicators';

    	INSERT INTO region_permission
    	(read_write, region_id, user_id)

    	SELECT 'r', r.id, au.id
    	FROM region r
    	INNER JOIN auth_user au
    	ON 1=1;

    	INSERT INTO region_permission
    	(read_write, region_id, user_id)

    	SELECT 'w' , region_id, user_id FROM region_permission;

        """)
    ]
