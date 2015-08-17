DROP FUNCTION IF EXISTS fn_upsert_source_dps(user_id INT, document_id INT);
CREATE FUNCTION fn_upsert_source_dps(user_id INT, document_id INT)
RETURNS TABLE
(
	 id INT
) AS
$func$
BEGIN

	DROP TABLE IF EXISTS _dp_to_upsert;
	CREATE TEMP TABLE _dp_to_upsert
	AS
	SELECT
		indicator_id
		, campaign_id
		, region_id
		, document_id
		,SUM(value) as value
		,max(source_submission_id) as source_submission_id
	FROM doc_datapoint d
	WHERE document_id = 74
	AND is_valid = 't'
	AND agg_on_region = 't'
	GROUP BY indicator_id, campaign_id, region_id, document_id;

	DELETE FROM datapoint
	WHERE id in (
	SELECT d.id
	FROM datapoint d
	INNER JOIN _dp_to_upsert tu
		ON d.region_id = tu.region_id
		AND d.indicator_id = tu.indicator_id
		AND d.campaign_id = tu.campaign_id
	);

	INSERT INTO datapoint
	(indicator_id, campaign_id, region_id, value, source_submission_id, cache_job_id, changed_by_id,created_at)
	SELECT indicator_id, campaign_id, region_id, value, source_submission_id, -1, $1,now()
	FROM _dp_to_upsert;

	SELECT id FROM datapoint d
	INNER JOIN source_datapoint sd
	ON d.source_submission_id = sd.source_submission_id
	AND sd.document_id = $2;

END
$func$ LANGUAGE PLPGSQL;
