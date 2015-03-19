DROP FUNCTION IF EXISTS fn_agg_datapoint(cache_job_id int);
CREATE FUNCTION fn_agg_datapoint(cache_job_id INT)
RETURNS TABLE(id int) AS $$

	DELETE FROM agg_datapoint ad
	USING datapoint d
	WHERE d.region_id = ad.region_id
	AND d.campaign_id = ad.campaign_id
	AND d.indicator_id = ad.indicator_id
	AND d.cache_job_id = $1;

	DELETE FROM agg_datapoint ad
	USING datapoint d
	INNER JOIN region r 
	ON d.region_id = r.id
	WHERE r.parent_region_id = ad.region_id
	AND d.campaign_id = ad.campaign_id
	AND d.indicator_id = ad.indicator_id
	AND d.cache_job_id = $1;

	INSERT INTO agg_datapoint
	(region_id,campaign_id,indicator_id,cache_job_id,value)

	SELECT 
		region_id,campaign_id,indicator_id,cache_job_id,value
	FROM datapoint d
	WHERE d.cache_job_id = $1;

	-- INSERT PARENTS --
 	INSERT INTO agg_datapoint
	(region_id,campaign_id,indicator_id,cache_job_id,value)

	SELECT 
		parent_region_id,campaign_id,indicator_id,cache_job_id,SUM(value)
	FROM agg_datapoint ad
	INNER JOIN region r 
	ON ad.region_id = r.id
	AND ad.cache_job_id = $1
	AND NOT EXISTS ( 
		SELECT 1 FROM agg_datapoint ad_exists
		WHERE ad.indicator_id = ad_exists.indicator_id 
		AND ad.campaign_id = ad_exists.campaign_id
		AND r.parent_region_id = ad_exists.region_id
	)
	GROUP BY parent_region_id,campaign_id,indicator_id,cache_job_id;

	SELECT id FROM agg_datapoint
	WHERE cache_job_id = $1
	LIMIT 1;

$$

LANGUAGE SQL;
