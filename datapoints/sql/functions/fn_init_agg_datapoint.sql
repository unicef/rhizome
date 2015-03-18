
DROP FUNCTION IF EXISTS fn_init_agg_datapoint();
CREATE FUNCTION fn_init_agg_datapoint()
RETURNS TABLE(id int)
AS $$

	TRUNCATE TABLE agg_datapoint;

	INSERT INTO agg_datapoint
	(region_id, campaign_id, indicator_id, value, is_agg, cache_job_id)

	SELECT
		region_id, campaign_id, indicator_id, value, 't', -1 --$1
	FROM datapoint d;

	SELECT id from agg_datapoint limit 1;

$$
LANGUAGE SQL;
