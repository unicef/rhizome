
DROP FUNCTION IF EXISTS fn_populate_doc_meta(document_id INT);
CREATE FUNCTION fn_populate_doc_meta(document_id INT)
RETURNS TABLE
(
	 id INT
) AS
$func$
BEGIN


-- GET ALL THE SOURCE DATAPOINT DATA IN TEMP TABLE --
DROP TABLE IF EXISTS _tmp_sdps;
CREATE TEMP TABLE _tmp_sdps
AS

SELECT region_code, indicator_string, campaign_string, document_id
FROM source_datapoint
WHERE document_id = 1055;


--INSERT SOURCE META WHERE NOT EXISTS--

-- region --
INSERT INTO source_region
(region_code)
SELECT region_code from _tmp_sdps tsdp
WHERE NOT EXISTS (
	SELECT 1 from source_region ser
	WHERE tsdp.region_code = ser.region_code
);

-- campaign --
INSERT INTO source_campaign
(campaign_string)
SELECT campaign_string from _tmp_sdps tsdp
WHERE NOT EXISTS (
	SELECT 1 from source_campaign sc
	WHERE tsdp.campaign_string = sc.campaign_string
);

-- indicator --
INSERT INTO source_indicator
(indicator_string)
SELECT indicator_string from _tmp_sdps tsdp
WHERE NOT EXISTS (
	SELECT 1 from source_indicator si
	WHERE tsdp.indicator_string = si.indicator_string
);


INSERT INTO document_detail
(document_id, source_object_id, source_string, source_dp_count, db_model,master_dp_count,master_object_id)

SELECT
	 MIN(tsdp.document_id)
	 ,MIN(si.id) as source_object_id
	,tsdp.indicator_string
	,COUNT(1) AS source_dp_count
	,'indicator' as db_model
	,0 as master_db_count
	,1 as master_object_id
FROM _tmp_sdps tsdp
INNER JOIN source_indicator si
ON tsdp.indicator_string = si.indicator_string
GROUP BY tsdp.indicator_string

UNION ALL

SELECT
	 MIN(tsdp.document_id)
	,MIN(sc.id) as source_object_id
	,tsdp.campaign_string
	,COUNT(1) AS source_dp_count
	,'campaign' as db_model
	,0 as master_db_count
	,1 as master_object_id
FROM _tmp_sdps tsdp
INNER JOIN source_campaign sc
ON tsdp.campaign_string = sc.campaign_string
GROUP BY tsdp.campaign_string

UNION ALL

SELECT
	 MIN(tsdp.document_id)
	,MIN(sr.id) as source_object_id
	,tsdp.region_code
	,COUNT(1) AS source_dp_count
	,'region' as db_model
	,0 as master_db_count
	,1 as master_object_id
FROM _tmp_sdps tsdp
INNER JOIN source_region sr
ON tsdp.region_code = sr.region_code
GROUP BY tsdp.region_code;

END
$func$ LANGUAGE PLPGSQL;
