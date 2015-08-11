# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.contrib.auth.models import User

def forwards_func(apps, schema_editor):
    User.objects.create_user\
        ('john', email='dingeej@gmail.com', password='endpolionow')


class Migration(migrations.Migration):

    dependencies = [
        ('datapoints', '0003_auto_20150805_0809'),
    ]

    operations = [

        migrations.RunPython(
            forwards_func,
        ),

        migrations.RunSQL("""

            -- INSERT INTO OFFICE --
            INSERT INTO office (name,created_at)
            SELECT 'Nigeria',NOW() UNION ALL
            SELECT 'Afghanistan',NOW() UNION ALL
            SELECT 'Pakistan',NOW();

            -- REGION TYPE --
            INSERT INTO region_type (name)
            SELECT 'Country' UNION ALL
            SELECT 'Province' UNION ALL
            SELECT 'District' UNION ALL
            SELECT 'Sub-District' UNION ALL
            SELECT 'Settlement';

            -- REGION --
            INSERT INTO region
            (name,region_code,slug,office_id,region_type_id,created_at)

            SELECT
                 x.region_name as region_name
                ,x.region_code as region_code
                ,lower(x.region_name) as slug
                ,o.id as office_id
                ,rt.id as region_type_id
                ,NOW()
            FROM (
                SELECT 'Nigeria' as region_name, 'NGA' as region_code UNION ALL
                SELECT 'Afghanistan', 'AFG' UNION ALL
                SELECT 'Pakistan', 'PAK'
            )x
            INNER JOIN office o
            ON o.name = x.region_name
            INNER JOIN region_type rt
            ON rt.name = 'Country';

            -- CACHE_JOB --
            INSERT INTO cache_job (id,date_attempted,date_completed,is_error,response_msg)
            SELECT -1, now(),now(),CAST(0 as BOOLEAN),'';

            -- PROCESS STATUS --
            INSERT INTO source_data_processstatus
            (status_text, status_description)
            SELECT 'processed_sucessfully','processed_sucessfully' UNION ALL
            SELECT 'TO_PROCESS','TO_PROCESS';

            -- CAMPAIGN_TYPE --
            INSERT INTO campaign_type
            (name)
            SELECT 'National Immunization Days (NID)' UNION ALL
            SELECT 'Sub-national Immunization Days (SNID)' UNION ALL
            SELECT 'SIAD' UNION ALL
            SELECT 'Mop-up';

            -- DOCUMENT TABLE --
            INSERT INTO source_data_document
            (created_by_id,guid,doc_text,is_processed,created_at)

            SELECT id, 'init_db','init_db', CAST(1 AS BOOLEAN),NOW()
            FROM auth_user LIMIT 1;

            -- SOURCE_DATAPOINT --
            INSERT INTO source_datapoint
            (id,campaign_string,indicator_string,region_code,cell_value,row_number,document_id,source_guid,status_id,guid,created_at)

            SELECT
                -1 as id
                ,'' as campaign_string
                ,'' as indicator_string
                ,'' as region_code
                ,'0' as cell_value
                ,'0' as row_number
                ,sdd.id as document_id
                ,'data_entry'
                ,ps.id as status_id
                ,'data_entry'
                ,NOW()
            FROM source_data_document sdd
            INNER JOIN source_data_processstatus ps
            ON 1=1
            LIMIT 1;

            """)
    ]
