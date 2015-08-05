# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('datapoints', '0004_add_base_metadata'),
    ]

    operations = [

        migrations.RunSQL("""


            INSERT INTO source_data_document
            (created_by_id,guid,doc_text,is_processed,created_at)

            SELECT id, 'init_ng_regions','init_ng_regions', CAST(1 AS BOOLEAN),NOW()
            FROM auth_user
            WHERE NOT EXISTS (
                SELECT 1 FROM source_data_document sdd
                WHERE guid = 'init_ng_regions'
            )
            LIMIT 1;

	    DROP TABLE IF EXISTS _tmp_ng_regions;
	    CREATE TABLE _tmp_ng_regions
	    (
		    region_code VARCHAR
		    ,region_name VARCHAR
		    ,region_type VARCHAR
		    ,country VARCHAR
	    );

	    INSERT INTO _tmp_ng_regions
	    (region_code, region_name, region_type, country)

            SELECT 42, 'Bauchi (Province)','Province','Nigeria' UNION ALL
            SELECT 43, 'Borno','Province','Nigeria' UNION ALL
            SELECT 18, 'Jigawa (Province)','Province','Nigeria' UNION ALL
            SELECT 19, 'Kaduna','Province','Nigeria' UNION ALL
            SELECT 20, 'Kano','Province','Nigeria' UNION ALL
            SELECT 22, 'Kebbi','Province','Nigeria' UNION ALL
            SELECT 34, 'Sokoto','Province','Nigeria' UNION ALL
            SELECT 36, 'Yobe','Province','Nigeria' UNION ALL
            SELECT 37, 'Zamfara','Province','Nigeria' UNION ALL
            SELECT 21, 'Katsina','Province','Nigeria' UNION ALL
            SELECT 4301, 'Abadam','District','Nigeria' UNION ALL
            SELECT 2001, 'Ajingi (Kano)','District','Nigeria' UNION ALL
            SELECT 2002, 'Albasu (Kano)','District','Nigeria' UNION ALL
            SELECT 2201, 'Aleiro','District','Nigeria' UNION ALL
            SELECT 4201, 'Alkaleri','District','Nigeria' UNION ALL
            SELECT 3701, 'Anka','District','Nigeria' UNION ALL
            SELECT 2202, 'Arewa Dandi','District','Nigeria' UNION ALL
            SELECT 2203, 'Argungu','District','Nigeria' UNION ALL
            SELECT 4302, 'Askira/Uba','District','Nigeria';


            INSERT INTO source_region
            (region_code,parent_code,region_type,country,source_guid,document_id)

            SELECT DISTINCT
                region_code
                ,LEFT(CAST(region_code AS VARCHAR),LENGTH(CAST(region_code AS VARCHAR))-2)
                ,region_type
                ,country
                ,region_code
                ,sdd.id
            FROM _tmp_ng_regions tng
            INNER JOIN source_data_document sdd
                ON sdd.doc_text = 'init_ng_regions'
            WHERE region_code is NOT NULL;

            INSERT INTO region
            (name,region_code,slug,office_id,region_type_id,parent_region_id,created_at)

            SELECT
                 tng.region_name
                ,tng.region_code
                ,tng.region_code
                ,o.id
                ,rt.id
                ,pr.id
                ,now()
            FROM _tmp_ng_regions tng
            INNER JOIN office o
                ON o.name = 'Nigeria'
            INNER JOIN region_type rt
                ON tng.region_type = rt.name
                AND tng.region_type = 'Province'
            INNER JOIN region pr
                ON pr.name = 'Nigeria';

            INSERT INTO region
            (name,region_code,slug,office_id,region_type_id,parent_region_id,created_at)

            SELECT
                tng.region_name
                ,tng.region_code
                ,tng.region_code
                ,o.id
                ,rt.id
                ,pr.id
                ,now()
            FROM _tmp_ng_regions tng
            INNER JOIN office o
                ON o.name = 'Nigeria'
            INNER JOIN region_type rt
                ON tng.region_type = rt.name
                AND tng.region_type = 'District'
            INNER JOIN region pr
                ON LEFT(CAST(tng.region_code AS VARCHAR),2) = CAST(pr.region_code AS VARCHAR);


            INSERT INTO region
            (name,region_code,slug,office_id,region_type_id,parent_region_id,created_at)

            SELECT
                 tng.region_name
                ,tng.region_code
                ,tng.region_code
                ,o.id
                ,rt.id
                ,pr.id
                ,now()
            FROM _tmp_ng_regions tng
            INNER JOIN office o
                ON o.name = 'Nigeria'
            INNER JOIN region_type rt
                ON tng.region_type = rt.name
                AND tng.region_type = 'Sub-District'
            INNER JOIN region pr
                ON LEFT(CAST(tng.region_code AS VARCHAR),4) = CAST(pr.region_code AS VARCHAR);


            INSERT INTO region_map
            (source_object_id,master_object_id,mapped_by_id)

            SELECT sr.id, r.id,x.user_id FROM source_region sr
            INNER join region r
            ON sr.region_code = r.region_code
            INNER JOIN (
                SELECT id as user_id FROM auth_user LIMIT 1
            )x
            ON 1=1;


        """)
    ]
