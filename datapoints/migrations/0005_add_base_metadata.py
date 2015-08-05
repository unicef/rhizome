# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.contrib.auth.models import User

class Migration(migrations.Migration):

    dependencies = [
        ('datapoints', '0003_auto_20150805_0809'),
    ]

    operations = [

        migrations.RunSQL("""

            -- INSERT INTO OFFICE --
            INSERT INTO office (name)
            SELECT 'Nigeria' UNION ALL
            SELECT 'Afghanistan' UNION ALL
            SELECT 'Pakistan';

            -- REGION TYPE --
            INSERT INTO region_type (name)
            SELECT 'Country' UNION ALL
            SELECT 'Province' UNION ALL
            SELECT 'District' UNION ALL
            SELECT 'Sub-District' UNpytcION ALL
            SELECT 'Settlement';

            -- REGION --
            INSERT INTO region
            (name,region_code,slug,office_id,region_type_id)

            SELECT x.region_name, lower(x.region_name),o.id,rt.id FROM (
                SELECT 'Nigeria' as region_name, 'NG' as region_code UNION ALL
                SELECT 'Afghanistan', 'AF' UNION ALL
                SELECT 'Pakistan', 'PK'
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
            SELECT 'processed_sucessfully','processed_sucessfully';

            -- CAMPAIGN_TYPE --
            INSERT INTO campaign_type
            (name)
            SELECT 'National Immunization Days (NID)' UNION ALL
            SELECT 'Sub-national Immunization Days (SNID)' UNION ALL
            SELECT 'SIAD' UNION ALL
            SELECT 'Mop-up';

            -- DOCUMENT TABLE --
            INSERT INTO source_data_document
            (created_by_id,guid,doc_text,is_processed)

            SELECT id, 'init_db','init_db', CAST(1 AS BOOLEAN)
            FROM auth_user LIMIT 1;

            -- SOURCE_DATAPOINT --
            INSERT INTO source_datapoint
            (id,campaign_string,indicator_string,region_code,cell_value,row_number,document_id,source_guid,status_id,guid)

            SELECT
                -1 as id
                ,'' as campaign_string
                ,'' as indicator_string
                ,'' as region_code
                ,'0' as cell_value
                ,'0' as row_number
                ,d.id as document_id
                ,'data_entry'
                ,ps.id as status_id
                ,'data_entry'
            FROM source_data_document sdd
            INNER JOIN source_data_processstatus ps
            ON 1=1
            LIMIT 1;

            """)
    ]
