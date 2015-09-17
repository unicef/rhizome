from __future__ import unicode_literals

from django.db import models, migrations
from django.contrib.auth.models import User

def forwards_func(apps, schema_editor):
    User.objects.create_superuser\
        ('demo_user', email='demo@user.com', password='demo_password')


class Migration(migrations.Migration):

    dependencies = [
        ('datapoints', '0002_all_unique_ix'),
    ]

    operations = [

     migrations.RunPython(
            forwards_func,
        ),

    migrations.RunSQL("""
        -- INITIAL DOCUMENT --
        INSERT INTO source_data_document
        (created_by_id,docfile,guid,doc_title,created_at)
        SELECT id,'initialize-db','initialize-db','initialize-db',NOW()
        FROM auth_user
        WHERE NOT EXISTS (
            SELECT 1 FROM source_data_document sdd
            WHERE guid = 'initialize-db'
        )
        LIMIT 1;
        --  DOCUMENT DETAIL  --
        INSERT INTO document_detail_type
        (name)
        SELECT 'odk_host' UNION ALL
        SELECT 'odk_form_name' UNION ALL
        SELECT 'region_column' UNION ALL
        SELECT 'campaign_column' UNION ALL
        SELECT 'username_column' UNION ALL
        SELECT 'uq_id_column' UNION ALL
        SELECT 'agg_on_region' UNION ALL
        SELECT 'image_col' UNION ALL
        SELECT 'delimiter' UNION ALL
        SELECT 'submission_count' UNION ALL
        SELECT 'submission_processed_count' UNION ALL
        SELECT 'submission_to_process_count' UNION ALL
        SELECT 'doc_datapoint_count' UNION ALL
        SELECT 'datapoint_count' UNION ALL
        SELECT 'agg_datapoint_count' UNION ALL
        SELECT 'calc_datapoint_count' UNION ALL
        SELECT 'lat_col' UNION ALL
        SELECT 'lon_col' UNION ALL
        SELECT 'region_display_name';
        --  OFFICE --
        INSERT INTO office (name,created_at)
        SELECT 'Nigeria',NOW() UNION ALL
        SELECT 'Afghanistan',NOW() UNION ALL
        SELECT 'Pakistan',NOW();
        -- REGION TYPE --
        INSERT INTO location_type (name,admin_level)
        SELECT 'Country',0 UNION ALL
        SELECT 'Province',1 UNION ALL
        SELECT 'District',2 UNION ALL
        SELECT 'Sub-District',3 UNION ALL
        SELECT 'Settlement',4;
        -- REGION --

        INSERT INTO location
        (name,location_code,slug,office_id,location_type_id,created_at)
        SELECT
             x.region_name as region_name
            ,x.region_code as region_code
            ,lower(x.region_name) as slug
            ,o.id as office_id
            ,rt.id as region_type_id
            ,NOW()
        FROM (
            SELECT 'Nigeria' as region_name, 'NG001000000000000000' as region_code UNION ALL
            SELECT 'Afghanistan', 'AF001000000000000000' UNION ALL
            SELECT 'Pakistan', 'PK001000000000000000'
        )x
        INNER JOIN office o
        ON o.name = x.region_name
        INNER JOIN location_type rt
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
        INSERT INTO result_structure_type
        (name)
        SELECT 'National Immunization Days (NID)' UNION ALL
        SELECT 'Sub-national Immunization Days (SNID)' UNION ALL
        SELECT 'SIAD' UNION ALL
        SELECT 'Mop-up';
    """)
    ]
