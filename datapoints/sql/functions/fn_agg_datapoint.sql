DROP FUNCTION IF EXISTS fn_agg_datapoint(cache_job_id INT,region_ids int[]);
CREATE FUNCTION fn_agg_datapoint(cache_job_id INT,region_ids int[] )
RETURNS TABLE(id int) AS $$

	-- DELETE RAW INDICATORS FROM OTHER CACHE_JOBS -
	DELETE FROM agg_datapoint ad
	USING datapoint d 
	WHERE ad.indicator_id = d.indicator_id
	AND ad.campaign_id = d.campaign_id
	AND d.cache_job_id = $1
	AND ad.region_id = ANY($2);
	
	-- INSERT RAW DATAPOINTS --
	INSERT INTO agg_datapoint 
	(region_id, campaign_id, indicator_id, value, cache_job_id)
	
	SELECT
		region_id, d.campaign_id, d.indicator_id, d.value, d.cache_job_id
	FROM datapoint d
	WHERE cache_job_id = $1
	AND NOT EXISTS ( 
		SELECT 1 FROM agg_datapoint ad
		WHERE ad.region_id = d.region_id
		AND ad.indicator_id = d.indicator_id
		AND ad.campaign_id = d.campaign_id
		AND ad.cache_job_id = d.cache_job_id
	)
	AND d.region_id = ANY($2);

	-- DELETE PARENT DATA --
	DELETE FROM agg_datapoint ad
	WHERE cache_job_id != $1
	AND EXISTS ( 
		SELECT 1 FROM datapoint d
		WHERE ad.region_id = d.region_id
		AND ad.indicator_id = d.indicator_id
		AND ad.campaign_id = d.campaign_id
		AND ad.cache_job_id = d.cache_job_id
	);

	-- INSERT PARENT DATA --
	INSERT INTO agg_datapoint
	(region_id, campaign_id, indicator_id, value, cache_job_id)
	SELECT 
		r.parent_region_id, ad.indicator_id, ad.campaign_id, SUM(value) as value, ad.cache_job_id
	FROM agg_datapoint ad
	INNER JOIN region r
		ON ad.region_id = r.id
		AND ad.cache_job_id = $1
		AND r.id = ANY($2)
	WHERE NOT EXISTS ( -- data stored at for the parent_region for this cache_job_id 
		SELECT 1 FROM agg_datapoint ad_exists
		WHERE ad.region_id = ad_exists.region_id
		AND ad.indicator_id = ad_exists.indicator_id
		AND ad.campaign_id = ad_exists.campaign_id
		AND ad.cache_job_id = ad_exists.cache_job_id
	)
	GROUP BY r.parent_region_id, ad.indicator_id, ad.campaign_id,ad.cache_job_id;

	-- WHEN THE LOOP IS DONE THIS SHOULD RETURN NO ROWS --
	
	SELECT DISTINCT parent_region_id as ID
	FROM region r
	WHERE id = ANY($2)
	
$$

LANGUAGE SQL;
