--SELECT * FROM fn_populate_doc_meta(1013)


DROP FUNCTION IF EXISTS fn_populate_doc_meta(input_document_id INT);
CREATE FUNCTION fn_populate_doc_meta(input_document_id INT)
RETURNS TABLE
(
	 id INT
	,db_model VARCHAR(255)
	,source_string VARCHAR(255)
	,source_object_id BIGINT
	,master_object_id BIGINT
	,master_object_cnt BIGINT
	,source_object_cnt BIGINT
) AS
$func$
BEGIN

        DROP TABLE IF EXISTS _doc_data;
        CREATE TABLE _doc_data AS

        SELECT
        	 sd.id as source_datapoint_id
        	,sd.document_id
        	,indicator_string
        	,campaign_string
        	,region_code
        FROM source_datapoint sd
        WHERE sd.document_id = $1;

        DROP TABLE IF EXISTS _doc_meta_cnt;
        CREATE TABLE _doc_meta_cnt AS
        SELECT
        	*
        	,CAST(NULL AS INT) AS source_object_id
        	,CAST(-1 AS INT) as master_object_id
        	,CAST(0 AS INT) as master_object_cnt
        FROM (
        	SELECT
        		'source_indicator' as db_model
        		,indicator_string as source_string
        		,COUNT(1) AS source_object_cnt
        	FROM _doc_data
        	GROUP BY indicator_string

        	UNION ALL

        	SELECT
        		'source_campaign' as db_model
        		,campaign_string
        		,COUNT(1) AS c
        	FROM _doc_data
        	GROUP BY campaign_string

        	UNION ALL

        	SELECT
        		'source_region' as db_model
        		,region_code
        		,COUNT(1) AS c
        	FROM _doc_data
        	GROUP BY region_code
        )x
        INNER JOIN (
        	SELECT dd.document_id
        	FROM _doc_data dd LIMIT 1
        )y
        ON 1=1;

        -----------------------------
        -- insert source meta data --
        -----------------------------

        ----------------
        -- indicators --
        ----------------
        INSERT INTO source_indicator
        (indicator_string, document_id,source_guid)

        SELECT dmc.source_string, dmc.document_id, dmc.source_string || '-' || dmc.document_id
        FROM _doc_meta_cnt dmc
        WHERE dmc.db_model = 'source_indicator'
        AND NOT EXISTS (
        	SELECT 1 FROM source_indicator si
        	WHERE dmc.db_model = 'source_indicator'
        	AND dmc.source_string = si.indicator_string
        );

        UPDATE _doc_meta_cnt dmc
        SET
        	source_object_id = si.id
        FROM source_indicator si
        WHERE dmc.db_model = 'source_indicator'
        AND dmc.source_string = si.indicator_string;

        -- MASTER INDICATOR ID --
        UPDATE _doc_meta_cnt dmc
        SET
        	master_object_id = im.master_object_id
        FROM indicator_map im
        WHERE dmc.db_model = 'source_indicator'
        AND dmc.source_object_id = im.source_object_id;


        -------------
        -- REGIONS --
        -------------

        INSERT INTO source_region
        (region_code,document_id,source_guid,is_high_risk)

        SELECT dmc.source_string, dmc.document_id, dmc.source_string || '-' || dmc.document_id, 'f'
        FROM _doc_meta_cnt dmc
        WHERE dmc.db_model = 'source_region'
        AND NOT EXISTS (
        	SELECT 1 FROM source_region sr
        	WHERE dmc.db_model = 'source_region'
        	AND dmc.source_string = sr.region_code
        );

        UPDATE _doc_meta_cnt dmc
        SET
        	source_object_id = sr.id
        FROM source_region sr
        WHERE dmc.db_model = 'source_region'
        AND dmc.source_string = sr.region_code;


        -- MASTER REGION ID --
        UPDATE _doc_meta_cnt dmc
        SET
        	master_object_id = rm.master_object_id
        FROM region_map rm
        WHERE dmc.db_model = 'source_region'
        AND dmc.source_object_id = rm.source_object_id;

        -------------
        -- CAMPAIGNS --
        -------------

        INSERT INTO source_campaign
        (campaign_string,document_id,source_guid)

        SELECT dmc.source_string, dmc.document_id, dmc.source_string || '-' || dmc.document_id
        FROM _doc_meta_cnt dmc
        WHERE dmc.db_model = 'source_campaign'
        AND NOT EXISTS (
        	SELECT 1 FROM source_campaign sc
        	WHERE dmc.db_model = 'source_campaign'
        	AND dmc.source_string = sc.campaign_string
        );

        -- SOURCE CAMPAIGN ID --
        UPDATE _doc_meta_cnt dmc
        SET
        	source_object_id = sc.id
        FROM source_campaign sc
        WHERE dmc.db_model = 'source_campaign'
        AND dmc.source_string = sc.campaign_string;

        -- MASTER CAMPAIGN ID --
        UPDATE _doc_meta_cnt dmc
        SET
        	master_object_id = cm.master_object_id
        FROM campaign_map cm
        WHERE dmc.db_model = 'source_campaign'
        AND dmc.source_object_id = cm.source_object_id;

        DROP TABLE IF EXISTS _synced_datapoints;
        CREATE TEMP TABLE _synced_datapoints  as
        SELECT
        	dd.region_code
        	,dd.indicator_string
        	,dd.campaign_string
        FROM _doc_data dd
        INNER JOIN datapoint d
        ON dd.source_datapoint_id = d.source_datapoint_id;


        UPDATE _doc_meta_cnt dmc
        SET master_object_cnt = x.cnt
        FROM (
        	SELECT 'source_indicator' as db_model,indicator_string as source_string ,COUNT(1) as cnt
        	FROM _synced_datapoints
        	GROUP BY indicator_string

        	UNION ALL

        	SELECT 'source_region' as db_model,region_code, COUNT(1) as cnt
        	FROM _synced_datapoints
        	GROUP BY region_code

        	UNION ALL

        	SELECT 'source_campaign' as db_model, campaign_string, COUNT(1) as cnt
        	FROM _synced_datapoints
        	GROUP BY campaign_string
        )x
        WHERE dmc.db_model = x.db_model
        AND dmc.source_string = x.source_string;


		RETURN QUERY

		--- RETURN TO RAW QUERYSET -----
        SELECT
        	dmc.document_id as id
        	,CAST(dmc.db_model AS VARCHAR)
        	,CAST(dmc.source_string AS VARCHAR)
        	,CAST(dmc.source_object_id AS BIGINT)
        	,CAST(dmc.master_object_id AS BIGINT)
        	,CAST(dmc.master_object_cnt AS BIGINT)
        	,CAST(dmc.source_object_cnt AS BIGINT)
        FROM _doc_meta_cnt dmc;


END
$func$ LANGUAGE PLPGSQL;
