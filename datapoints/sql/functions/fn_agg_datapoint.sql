DROP FUNCTION IF EXISTS fn_agg_datapoint(cache_job_id INT,region_ids int[]);
CREATE FUNCTION fn_agg_datapoint(cache_job_id INT,region_ids int[] )
RETURNS TABLE(id int) AS $$


	EXECUTE FORMAT ('

		DROP TABLE IF EXISTS _tmp_agg_data;
		CREATE TEMP TABLE _tmp_agg_data
		AS
		SELECT *
		FROM datapoint d
		WHERE cache_job_id = %1$s
		;',$1
	);

	-- NOW INSERT THE INDICATORS NEEDED TO MAKE THE CALCULATION --
	INSERT INTO _tmp_indicator_lookup
	(indicator_in, indicator_out, is_calc)

	SELECT
		indicator_in
		, cic.indicator_component_id
		, CAST(0 AS BOOLEAN) AS is_calc
	FROM _tmp_indicator_lookup til
	INNER JOIN calculated_indicator_component cic
	ON indicator_out = cic.indicator_id



	/*
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
	AND d.value is not null -- THIS SHOULD NOT HAPPEN
	AND d.region_id = ANY($2);


	-- INSERT PARENT DATA --
 	INSERT INTO agg_datapoint
 	(region_id, campaign_id, indicator_id, value, cache_job_id)
	SELECT
		r.parent_region_id, ad.campaign_id, ad.indicator_id, SUM(value) as value, $1 as cache_job_id
	FROM agg_datapoint ad
	INNER JOIN region r
		ON ad.region_id = r.id
 	WHERE EXISTS ( -- see POLIO-491 --
 		SELECT 1 FROM agg_datapoint ad_needs_compute
 		INNER JOIN region agg_r
			ON ad_needs_compute.region_id = agg_r.id
 		WHERE agg_r.parent_region_id = r.parent_region_id
 		AND ad_needs_compute.cache_job_id = $1
 		AND ad_needs_compute.indicator_id = ad.indicator_id
 		AND ad_needs_compute.campaign_id = ad.campaign_id
 		LIMIT 1
 	)
	AND NOT EXISTS ( -- data stored at for the parent_region for this cache_job_id
		SELECT 1 FROM agg_datapoint ad_exists
		WHERE r.parent_region_id = ad_exists.region_id
		AND ad.indicator_id = ad_exists.indicator_id
		AND ad.campaign_id = ad_exists.campaign_id
		AND ad_exists.cache_job_id = $1
	)
	AND NOT EXISTS ( -- data stored at the parent level
		SELECT 1 FROM datapoint dp
		WHERE r.parent_region_id = dp.region_id
		AND ad.indicator_id = dp.indicator_id
		AND ad.campaign_id = dp.campaign_id
	)
	AND ad.value is not null
	GROUP BY r.parent_region_id, ad.indicator_id, ad.campaign_id;

	-- WHEN THE LOOP IS DONE THIS SHOULD RETURN NO ROWS --

	SELECT DISTINCT parent_region_id as ID
	FROM region r
	WHERE id = ANY($2)
	AND parent_region_id IS NOT NULL

	*/

$$

LANGUAGE SQL;
