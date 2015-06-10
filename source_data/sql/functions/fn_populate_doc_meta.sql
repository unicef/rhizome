DROP FUNCTION IF EXISTS fn_populate_doc_meta(document_id INT);
CREATE FUNCTION fn_populate_doc_meta(document_id INT)
RETURNS TABLE
(
	ID INT,
	doc_id INT,
	source_object_id INT,
	source_string VARCHAR,
	source_dp_count INT,
	master_dp_count INT,
	db_model VARCHAR,
	master_object_id INT,
	map_id INT

) AS
$func$
BEGIN


-- GET ALL THE SOURCE DATAPOINT DATA IN TEMP TABLE --
DROP TABLE IF EXISTS _tmp_sdps;
CREATE TEMP TABLE _tmp_sdps
AS

SELECT sd.id ,region_code, indicator_string, campaign_string, sd.document_id
FROM source_datapoint sd
WHERE sd.document_id = $1;


--INSERT SOURCE META WHERE NOT EXISTS--

-- region --
INSERT INTO source_region
(region_code,source_guid,document_id)
SELECT DISTINCT region_code ,replace(region_code,' ','_'),$1
from _tmp_sdps tsdp
WHERE NOT EXISTS (
	SELECT 1 from source_region ser
	WHERE tsdp.region_code = ser.region_code
);

-- campaign --
INSERT INTO source_campaign
(campaign_string,source_guid,document_id)
SELECT DISTINCT campaign_string , replace(campaign_string,' ','_'),$1
FROM _tmp_sdps tsdp
WHERE NOT EXISTS (
	SELECT 1 from source_campaign sc
	WHERE tsdp.campaign_string = sc.campaign_string
);

-- indicator --
INSERT INTO source_indicator
(indicator_string, source_guid, document_id)
SELECT DISTINCT indicator_string , REPLACE(indicator_string,' ','_'), $1
from _tmp_sdps tsdp
WHERE NOT EXISTS (
	SELECT 1 from source_indicator si
	WHERE tsdp.indicator_string = si.indicator_string
);


-- FIND ID AND COUNT FOR MASTER METADATA IDS --
DROP TABLE IF EXISTS _synced_dbs;
CREATE TABLE _synced_dbs AS

SELECT
	 d.region_id
	,tsdp.region_code
	,d.campaign_id
	,tsdp.campaign_string
	,d.indicator_id
	,tsdp.indicator_string
FROM _tmp_sdps tsdp
INNER JOIN datapoint d
ON tsdp.id = d.source_datapoint_id;


DELETE FROM document_detail dd
WHERE dd.document_id = $1;

INSERT INTO document_detail
(document_id, source_object_id, source_string, source_dp_count, db_model,master_dp_count,master_object_id,map_id)

SELECT
	 x.document_id
	,x.source_object_id
	,CAST(x.source_string as VARCHAR)
	,x.source_dp_count
	,CAST(x.db_model AS VARCHAR)
	,COALESCE(y.dp_cnt,0) as master_db_count
	,-1 as master_object_id
	,-1 as map_id
FROM (
	SELECT
 		 MIN(tsdp.document_id) as document_id
		 ,MIN(si.id) as source_object_id
		,tsdp.indicator_string as source_string
		,COUNT(1) AS source_dp_count
		,'indicator' as db_model
	FROM _tmp_sdps tsdp
	INNER JOIN source_indicator si
	ON tsdp.indicator_string = si.indicator_string
	GROUP BY tsdp.indicator_string
)x

LEFT JOIN (
	SELECT indicator_string, max(indicator_id) as indicator_id ,count(1) as dp_cnt
	FROM _synced_dbs
	GROUP BY indicator_string
)y
ON x.source_string = y.indicator_string


UNION ALL

SELECT
	 x.document_id
	,x.source_object_id
	,CAST(x.source_string as VARCHAR)
	,x.source_dp_count
	,CAST(x.db_model AS VARCHAR)
	,COALESCE(y.dp_cnt,0) as master_db_count
	,-1 as master_object_id
	,-1 as map_id
FROM (
	SELECT
 		 MIN(tsdp.document_id) as document_id
		 ,MIN(sc.id) as source_object_id
		,tsdp.campaign_string as source_string
		,COUNT(1) AS source_dp_count
		,'campaign' as db_model
	FROM _tmp_sdps tsdp
	INNER JOIN source_campaign sc
	ON tsdp.campaign_string = sc.campaign_string
	GROUP BY tsdp.campaign_string
)x

LEFT JOIN (
	SELECT campaign_string, max(campaign_id) as campaign_id ,count(1) as dp_cnt
	FROM _synced_dbs
	GROUP BY campaign_string
)y
ON x.source_string = y.campaign_string

UNION ALL

SELECT
	 x.document_id
	,x.source_object_id
	,CAST(x.source_string as VARCHAR)
	,x.source_dp_count
	,CAST(x.db_model AS VARCHAR)
	,COALESCE(y.dp_cnt,0) as master_db_count
	,-1 as master_object_id
	,-1 as map_id
FROM (
	SELECT
 		 MIN(tsdp.document_id) as document_id
		,MIN(sr.id) as source_object_id
		,tsdp.region_code as source_string
		,COUNT(1) AS source_dp_count
		,'region' as db_model
	FROM _tmp_sdps tsdp
	INNER JOIN source_region sr
	ON tsdp.region_code = sr.region_code
	GROUP BY tsdp.region_code
)x

LEFT JOIN (
	SELECT region_code, max(region_id) as region_id ,count(1) as dp_cnt
	FROM _synced_dbs
	GROUP BY region_code
)y
ON x.source_string = y.region_code;

-- UPDATE MASTER OBJECT IDS --

UPDATE document_detail dd
SET master_object_id = rm.master_object_id
	,map_id = rm.id
FROM region_map rm
WHERE dd.source_object_id = rm.source_object_id
AND dd.document_id = $1
AND dd.db_model = 'region';

UPDATE document_detail dd
SET master_object_id = im.master_object_id
	,map_id = im.id
FROM indicator_map im
WHERE dd.source_object_id = im.source_object_id
AND dd.document_id = $1
AND dd.db_model = 'indicator';

UPDATE document_detail dd
SET master_object_id = cm.master_object_id
	,map_id = cm.id
FROM campaign_map cm
WHERE dd.source_object_id = cm.source_object_id
AND dd.document_id = $1
AND dd.db_model = 'campaign';

RETURN QUERY

SELECT * FROM document_detail dd
WHERE dd.document_id = $1;

END
$func$ LANGUAGE PLPGSQL;
