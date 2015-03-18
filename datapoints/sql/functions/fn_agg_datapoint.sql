
DROP FUNCTION IF EXISTS fn_agg_datapoint(cache_job_id int);
CREATE FUNCTION fn_agg_datapoint(cache_job_id INT)
RETURNS TABLE(id int) AS $$

	DELETE FROM agg_datapoint
	WHERE ID IN (
		SELECT ad.id FROM agg_datapoint ad
		INNER JOIN datapoint d
			ON ad.region_id = d.region_id
			AND ad.campaign_id = d.campaign_id
			AND ad.indicator_id = d.indicator_id
		WHERE d.cache_job_id = $1
	);
	

	INSERT INTO agg_datapoint
	(region_id,indicator_id,campaign_id,cache_job_id,value)

	SELECT region_id,indicator_id,campaign_id,cache_job_id,value 
	FROM datapoint
	
	WHERE cache_job_id = $1;
	
	SELECT id FROM agg_datapoint LIMIT 1;

$$

LANGUAGE SQL;


