DROP VIEW IF EXISTS vw_missing_mappings CASCADE;
CREATE VIEW vw_missing_mappings
AS

WITH first_join AS
(
SELECT
 	d.id as datapoint_id
 	,d.source_datapoint_id
 	,d.region_id
	,sr.id as source_id
 	,d.campaign_id
 	,sc.id as source_id
 	,d.indicator_id
 	,si.id as source_id
 	,sd.document_id
FROM datapoint d
INNER JOIN source_datapoint sd
	ON d.source_datapoint_id = sd.id
INNER JOIN source_region sr
	ON sr.region_code = sd.region_code
INNER JOIN source_campaign sc
 	ON sc.campaign_string = sd.campaign_string
INNER JOIN source_indicator si
	ON si.indicator_string = sd.indicator_string
)


SELECT
	row_number() OVER (ORDER BY datapoint_id, document_id, what_is_missing)  AS id
	,*
FROM
(
	SELECT
		fj.datapoint_id
		, fj.document_id
		, 'indicator' AS what_is_missing
	FROM first_join fj
	WHERE NOT EXISTS
	(
		SELECT 1 FROM indicator_map im
		WHERE fj.indicator_id = im.master_id
		AND fj.source_id = im.source_id
	)


	UNION ALL

	SELECT
		fj.datapoint_id
		, fj.document_id
		,'region' ASwhat_is_missing
	FROM first_join fj
	WHERE NOT EXISTS
	(
		SELECT 1 FROM region_map rm
		WHERE fj.region_id = rm.master_id
		AND fj.source_id = rm.source_id
	)

	UNION ALL

	SELECT
		fj.datapoint_id
		, fj.document_id
		,'campaign' AS what_is_missing
	FROM first_join fj
	WHERE NOT EXISTS
	(
		SELECT 1 FROM campaign_map cm
		WHERE fj.campaign_id = cm.master_id
		AND fj.source_id = cm.source_id

	)

)x;

GRANT SELECT, DELETE ON vw_missing_mappings to djangoapp;

-- CREATE OR REPLACE RULE missing_mapping_DELETE AS ON DELETE TO vw_missing_mappings DO INSTEAD (
--      DELETE FROM datapoint WHERE id=OLD.datapoint_id;);
--
