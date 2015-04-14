
--SELECT * FROM fn_agg_datapoint(57)
DROP FUNCTION IF EXISTS fn_agg_datapoint(cache_job_id INT);
CREATE FUNCTION fn_agg_datapoint(cache_job_id INT)
RETURNS TABLE(id int) AS
$func$
BEGIN


DROP TABLE IF EXISTS _campaign_indicator;
		CREATE TABLE _campaign_indicator AS
		SELECT DISTINCT campaign_id, indicator_id FROM datapoint d
		WHERE d.cache_job_id = $1;

  		DROP TABLE IF EXISTS _tmp_agg;
  		CREATE TABLE _tmp_agg AS


		WITH RECURSIVE region_tree AS
		    (
		    -- non-recursive term ( rows where the components aren't
		    -- master_indicators in another calculation )

		  	SELECT
		  		rg.parent_region_id
		  		,rg.id as region_id
		  		,0 as lvl
		  	FROM region rg
		  	WHERE NOT EXISTS (
		  		SELECT 1 FROM region rg_leaf
		  		WHERE rg.id = rg_leaf.parent_region_id
		  	)

		  	UNION ALL

		  	-- recursive term --
		  	SELECT
		  		 r_recurs.parent_region_id
		  		,rt.region_id
		  		,rt.lvl + 1
		  	FROM region AS r_recurs
		  	INNER JOIN region_tree AS rt
		  	ON (r_recurs.id = rt.parent_region_id)
			AND r_recurs.parent_region_id IS NOT NULL
		    )

		SELECT DISTINCT
			d.id as datapoint_id, d.region_id, d.campaign_id, d.indicator_id, rt.parent_region_id, d.value, d.cache_job_id
			--,rt.parent_region_id
		FROM region_tree rt
		INNER JOIN region r
			ON rt.parent_region_id = r.parent_region_id
		INNER JOIN datapoint d
			ON r.id = d.region_id
		INNER JOIN _campaign_indicator ci
			ON d.indicator_id = ci.indicator_id
			AND d.campaign_id = ci.campaign_id;

		INSERT INTO _tmp_agg
		(region_id, campaign_id, indicator_id, value)

		SELECT parent_region_id, campaign_id, indicator_id, SUM(value)
		FROM _tmp_agg
		GROUP BY parent_region_id, campaign_id, indicator_id;

		UPDATE agg_datapoint ad
			SET cache_job_id = $1
			, value = ta.value
		FROM _tmp_agg ta
		WHERE ta.region_id = ad.region_id
		AND ta.campaign_id = ad.campaign_id
		AND ta.indicator_id = ad.indicator_id;
		--AND ad.value != ta.value;

		INSERT INTO agg_datapoint
		(region_id, campaign_id, indicator_id, value,cache_job_id)
		SELECT region_id, campaign_id, indicator_id, value, $1
		FROM _tmp_agg ta
		WHERE NOT EXISTS (
			SELECT 1 FROM agg_datapoint ad
			WHERE ta.region_id = ad.region_id
			AND ta.campaign_id = ad.campaign_id
			AND ta.indicator_id = ad.indicator_id
		);

		-- SET ALL DATAPOINTS THAT ARE DEPENDENT ON THIS CALCULATION = THE NEW CACHE JOB ID

		UPDATE datapoint d
			SET cache_job_id = $1
		FROM _tmp_agg ta
		WHERE d.id = ta.datapoint_id;


		RETURN QUERY

		SELECT ad.region_id FROM agg_datapoint ad
		WHERE ad.cache_job_id = $1
		LIMIT 1;



END
$func$ LANGUAGE PLPGSQL;
