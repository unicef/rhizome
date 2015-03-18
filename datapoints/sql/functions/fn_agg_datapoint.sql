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

		UNION ALL
		
		SELECT DISTINCT ad.id FROM agg_datapoint ad
		INNER JOIN datapoint d
			ON ad.campaign_id = d.campaign_id
			AND ad.indicator_id = d.indicator_id
		WHERE EXISTS (
			SELECT 1 FROM region r 
			WHERE ad.region_id = r.parent_region_id
			AND d.region_id = r.id
		)
		AND d.cache_job_id = $1
		
	);	

	INSERT INTO agg_datapoint
	(region_id,indicator_id,campaign_id,cache_job_id,value)

	SELECT region_id,indicator_id,campaign_id,cache_job_id,value 
	FROM datapoint	
	WHERE cache_job_id = $1
	
	UNION ALL

	SELECT r.parent_region_id,indicator_id,campaign_id,cache_job_id,SUM(value)
	FROM datapoint d 
	INNER JOIN region r 
		ON d.region_id = r.id
	WHERE cache_job_id = $1
	GROUP BY r.parent_region_id,indicator_id,campaign_id,cache_job_id;


	-- Mark All Component Indicator Values with the passed cache_job_id 
	-- This makes it easier for the calc datapoint (that is, cache_job_id can be
	-- a join condition in each select statment used in fn_calc_datapoint()) 
	
	-- that is.. find the agg_datapoint IDS that are part of the 
	-- calculation but have not yet been changed by this sproc and set the cache_job_id

	UPDATE agg_datapoint 
	SET cache_job_id = $1
	WHERE id in (

		SELECT 
			to_update.id
		FROM agg_datapoint ad_updated
		INNER JOIN calculated_indicator_component cic_updated
			ON ad_updated.indicator_id = cic_updated.indicator_component_id
			AND cache_job_id = $1
			INNER JOIN calculated_indicator_component cic_to_update 
			ON cic_updated.indicator_id = cic_to_update.indicator_id
		INNER JOIN agg_datapoint to_update
			ON to_update.region_id = ad_updated.region_id
			AND to_update.campaign_id = ad_updated.campaign_id
			AND to_update.indicator_id = cic_to_update.indicator_component_id
			AND to_update.id != ad_updated.id
	);

	SELECT id FROM agg_datapoint LIMIT 1;

$$

LANGUAGE SQL;
