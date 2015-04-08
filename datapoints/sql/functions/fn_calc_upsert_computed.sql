DROP FUNCTION IF EXISTS fn_calc_upsert_computed(cache_job_id int);
CREATE FUNCTION fn_calc_upsert_computed(cache_job_id int)
RETURNS TABLE(id int) AS
$func$
BEGIN

	TRUNCATE TABLE datapoint_with_computed;

	INSERT INTO datapoint_with_computed
	(region_id, campaign_id, indicator_id, value, cache_job_id)

	SELECT region_id, campaign_id, indicator_id, value, $1
	FROM _tmp_calc_datapoint
	WHERE region_id = 12912;


	RETURN QUERY

	SELECT ad.id FROM agg_datapoint ad
	--WHERE dwc.cache_job_id = $1
	LIMIT 1;

END
$func$ LANGUAGE PLPGSQL;
