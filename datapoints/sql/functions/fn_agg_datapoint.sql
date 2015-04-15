DROP FUNCTION IF EXISTS fn_agg_datapoint(cache_job_id INT);
CREATE FUNCTION fn_agg_datapoint(cache_job_id INT)
RETURNS TABLE(id int) AS
$func$
BEGIN


		DROP TABLE IF EXISTS _campaign_indicator;
		CREATE TABLE _campaign_indicator AS
		SELECT DISTINCT campaign_id, indicator_id FROM datapoint d
		WHERE d.cache_job_id = $1;

		DROP TABLE IF EXISTS _to_agg;
		CREATE TEMP TABLE _to_agg AS

		WITH RECURSIVE region_tree AS
				(
				-- non-recursive term ( rows where the components aren't
				-- master_indicators in another calculation )

				SELECT
					rg.parent_region_id
					,rg.id as region_id
					,0 as lvl
				FROM region rg
			WHERE EXISTS (
				SELECT 1 FROM datapoint d
				WHERE d.region_id = rg.id
				AND d.cache_job_id = $1
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
			d.id as datapoint_id
			,d.indicator_id
			,d.campaign_id
			,d.region_id
			,d.value
			,rt.parent_region_id
		FROM region_tree rt
		INNER JOIN region r
		ON r.parent_region_id = rt.parent_region_id
		INNER JOIN datapoint d
		ON r.id = d.region_id
		INNER JOIN _campaign_indicator ci
			ON d.indicator_id = ci.indicator_id
			AND d.campaign_id = ci.campaign_id;


		DROP TABLE IF EXISTS _tmp_agg;
		CREATE TABLE _tmp_agg AS

		SELECT
			d.datapoint_id
			,d.region_id
			,d.campaign_id
			,d.indicator_id
			,d.value
		FROM _to_agg d

		UNION ALL

		SELECT
			CAST(NULL AS INT) as id
			,d.parent_region_id
			,d.campaign_id
			,d.indicator_id
			,SUM(d.value) as value
		FROM _to_agg d
		WHERE NOT EXISTS (
			SELECT 1 FROM _to_agg ta
			WHERE d.parent_region_id = ta.region_id
			AND d.campaign_id = ta.campaign_id
			AND d.indicator_id = ta.indicator_id
		)
		GROUP BY d.parent_region_id, d.campaign_id, d.indicator_id;

		CREATE UNIQUE INDEX rc_agg_ix ON _tmp_agg(region_id,campaign_id,indicator_id);

		-- OVERRIDES --
		UPDATE _tmp_agg ta
			set value = d.value
			, datapoint_id = d.id
		FROM datapoint d
		WHERE ta.region_id = d.region_id
		AND ta.campaign_id = d.campaign_id
		AND ta.indicator_id = d.indicator_id;

		--- UPDATE THE REST OF THE DATAPOINT TABLE --
		--- DONT NEED TO RE-PROCESS THIS DATA ---
		UPDATE datapoint d
		SET cache_job_id = $1
		WHERE d.id in (
			SELECT datapoint_id
			FROM _to_agg ta
			WHERE ta.datapoint_id IS NOT NULL
		);

		--------------------
		--- BEGIN UPSERT ---
		--------------------


		-- UPDATE EXISTING --
		UPDATE agg_datapoint ad
			SET cache_job_id = $1
			, value = ta.value
		FROM _tmp_agg ta
		WHERE ta.region_id = ad.region_id
		AND ta.campaign_id = ad.campaign_id
		AND ta.indicator_id = ad.indicator_id;
		--AND ad.value != ta.value;

		-- INSERT NEW --
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


		RETURN QUERY

		SELECT ad.region_id FROM agg_datapoint ad
		WHERE ad.cache_job_id = $1
		LIMIT 1;

END
$func$ LANGUAGE PLPGSQL;
