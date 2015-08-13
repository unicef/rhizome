# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('datapoints', '0015_update_metadata_sequences'),
    ]

    operations = [
    migrations.RunSQL("""

    INSERT INTO column_attributes
    (table_name,column_name,display_name,display_on_table_flag)

    SELECT *, CAST(0 AS BOOLEAN) FROM (
        SELECT 'table_name','column_name','display_name' UNION ALL
        SELECT 'auth_user','last_login','last login' UNION ALL
        SELECT 'auth_user','password','password' UNION ALL
        SELECT 'auth_user','is_superuser','is superuser' UNION ALL
        SELECT 'auth_user','username','username' UNION ALL
        SELECT 'auth_user','first_name','first name' UNION ALL
        SELECT 'auth_user','last_name','last name' UNION ALL
        SELECT 'auth_user','email','email' UNION ALL
        SELECT 'auth_user','is_staff','is staff' UNION ALL
        SELECT 'auth_user','is_active','is active' UNION ALL
        SELECT 'auth_user','date_joined','date joined' UNION ALL
        SELECT 'auth_user','id','id' UNION ALL
        SELECT 'campaign','office_id','office id' UNION ALL
        SELECT 'campaign','start_date','start date' UNION ALL
        SELECT 'campaign','end_date','end date' UNION ALL
        SELECT 'campaign','slug','slug' UNION ALL
        SELECT 'campaign','created_at','created at' UNION ALL
        SELECT 'campaign','campaign_type_id','campaign type id' UNION ALL
        SELECT 'campaign','id','id' UNION ALL
        SELECT 'indicator','name','name' UNION ALL
        SELECT 'indicator','description','description' UNION ALL
        SELECT 'indicator','is_reported','is reported' UNION ALL
        SELECT 'indicator','slug','slug' UNION ALL
        SELECT 'indicator','created_at','created at' UNION ALL
        SELECT 'indicator','short_name','short name' UNION ALL
        SELECT 'indicator','source_id','source id' UNION ALL
        SELECT 'region','office_id','office id' UNION ALL
        SELECT 'region','shape_file_path','shape file path' UNION ALL
        SELECT 'region','latitude','latitude' UNION ALL
        SELECT 'region','longitude','longitude' UNION ALL
        SELECT 'region','slug','slug' UNION ALL
        SELECT 'region','created_at','created at' UNION ALL
        SELECT 'region','source_id','source id' UNION ALL
        SELECT 'region','region_code','region code' UNION ALL
        SELECT 'region','is_high_risk','is high risk' UNION ALL
        SELECT 'region','name','name' UNION ALL
        SELECT 'region','parent_region_id','parent region id' UNION ALL
        SELECT 'region','region_type_id','region type id' UNION ALL
        SELECT 'indicator','id','id' UNION ALL
        SELECT 'region','id','id' UNION ALL
        SELECT 'indicator_abstracted','bound_json','bound json' UNION ALL
        SELECT 'indicator_abstracted','id','id' UNION ALL
        SELECT 'indicator_abstracted','description','description' UNION ALL
        SELECT 'indicator_abstracted','short_name','short name' UNION ALL
        SELECT 'indicator_abstracted','slug','slug' UNION ALL
        SELECT 'indicator_abstracted','name','name' UNION ALL
        SELECT 'user_abstracted','user_id','user id' UNION ALL
        SELECT 'user_abstracted','last_login','last login' UNION ALL
        SELECT 'user_abstracted','is_superuser','is superuser' UNION ALL
        SELECT 'user_abstracted','username','username' UNION ALL
        SELECT 'user_abstracted','email','email' UNION ALL
        SELECT 'user_abstracted','is_staff','is staff' UNION ALL
        SELECT 'user_abstracted','is_active','is active' UNION ALL
        SELECT 'user_abstracted','date_joined','date joined' UNION ALL
        SELECT 'user_abstracted','last_name','last name' UNION ALL
        SELECT 'user_abstracted','group_json','group json' UNION ALL
        SELECT 'user_abstracted','region_permission_json','region permission json' UNION ALL
        SELECT 'user_abstracted','id','id' UNION ALL
        SELECT 'user_abstracted','first_name','first name'
    )x
    """)
    ]
