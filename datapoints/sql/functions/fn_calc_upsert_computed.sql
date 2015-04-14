DROP FUNCTION IF EXISTS fn_calc_upsert_computed(cache_job_id int);
CREATE FUNCTION fn_calc_upsert_computed(cache_job_id int)
RETURNS TABLE(id int) AS
$func$
BEGIN

	UPDATE datapoint_with_computed dwc
		SET value = tcd.value
			, cache_job_id = $1
	FROM _tmp_calc_datapoint tcd
	WHERE dwc.region_id = tcd.region_id
	AND dwc.indicator_id = tcd.indicator_id
	AND dwc.campaign_id = tcd.campaign_id;


	INSERT INTO datapoint_with_computed
	(region_id, campaign_id, indicator_id, value, cache_job_id)

	SELECT region_id, campaign_id, indicator_id, value, $1
	FROM _tmp_calc_datapoint tcd
	WHERE NOT EXISTS (
		SELECT 1 FROM datapoint_with_computed dwc
		WHERE tcd.region_id = dwc.region_id
		AND tcd.campaign_id = dwc.campaign_id
	 	AND tcd.indicator_id = dwc.indicator_id
	);


	RETURN QUERY

	SELECT ad.id FROM agg_datapoint ad
	--WHERE dwc.cache_job_id = $1
	LIMIT 1;

END
$func$ LANGUAGE PLPGSQL;
