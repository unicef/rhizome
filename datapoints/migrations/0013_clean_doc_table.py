# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.contrib.auth.models import User

class Migration(migrations.Migration):

    dependencies = [
        ('datapoints', '0012_ingest_geojson'),
    ]

    operations = [

    migrations.RunSQL("""
        DROP TABLE IF EXISTS _docs_to_delete;
        CREATE TABLE _docs_to_delete as
        SELECT
        	id
        	,doc_title
        FROM source_doc
        --@@THESE ARE THE DOCUMENTS WE ARE KEEPING@@--
        WHERE id not in (
        20,      --SEED_FINAL.csv-1443542624	View Raw Data
        14,	--PAK.2015.04.upload.csv-1442948602	View Raw Data
        13,	--PAK.2015.04.upload.csv-1442948541	View Raw Data
        12,	--nga.im.2015.07.recode.csv-1442939067	View Raw Data
        10,	--vcm_support_supervision_results.csv-1442768281	View Raw Data
        9,	--vcm_birth_tracking_results.csv-1442768237	View Raw Data
        8,	--Health_Camps_results.csv-1442768181	View Raw Data
        7,	--vcm_register_results.csv-1442767806	View Raw Data
        4,	--seed_datapoints.csv-1442701554	View Raw Data
        2,	--nigeria_inside_all.csv-1442692673	View Raw Data
        1	--initialize-db	View Raw Data
        );


        --SELECT *
        DELETE
        FROM doc_object_map
        WHERE document_id IN (
        	SELECT id from _docs_to_delete
        );

        -- SELECT *
        DELETE
        FROM submission_detail sd
        WHERE document_id IN (
        	SELECT id from _docs_to_delete
        );

        -- SELECT *
        DELETE
        FROM doc_detail dd
        WHERE document_id IN (
        	SELECT id from _docs_to_delete
        );


        --SELECT *
        DELETE
        FROM doc_datapoint dd
        WHERE document_id IN (
        	SELECT id from _docs_to_delete
        );


        -- SELECT *
        DELETE
        FROM datapoint_with_computed dwc
        USING datapoint d
        WHERE d.location_id = dwc.location_id
        AND d.campaign_id = dwc.campaign_id
        AND d.cache_job_id = dwc.cache_job_id
        AND d.source_submission_id in (
        	SELECT ss.id FROM source_submission ss
        	INNER JOIN _docs_to_delete dd
        	ON ss.document_id = dd.id
        );

        -- SELECT *
        DELETE
        FROM agg_datapoint ad
        USING datapoint d
        WHERE d.location_id = ad .location_id
        AND d.campaign_id = ad.campaign_id
        AND d.indicator_id = ad.indicator_id
        AND d.cache_job_id = ad.cache_job_id
        AND d.source_submission_id in (
        	SELECT ss.id FROM source_submission ss
        	INNER JOIN _docs_to_delete dd
        	ON ss.document_id = dd.id
        );


        --SELECT *
        DELETE
        FROM datapoint d
        WHERE d.source_submission_id IN (
        	SELECT ss.id FROM source_submission ss
        	INNER JOIN _docs_to_delete dd
        	ON ss.document_id = dd.id
        );

        -- SELECT *
        DELETE
        FROM source_submission ss
        WHERE ss.document_id in (
        	SELECT id FROM _docs_to_delete
        );

        DELETE
        -- SELECT *
        FROM source_doc where id in (
        	SELECT id from _docs_to_delete
        );

    """)
    ]
