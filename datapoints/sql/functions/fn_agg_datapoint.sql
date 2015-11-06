	DROP FUNCTION IF EXISTS fn_agg_datapoint(cache_job_id INT);
	CREATE FUNCTION fn_agg_datapoint(cache_job_id INT)
	RETURNS TABLE(id int) AS
	$func$
	BEGIN

			DROP TABLE IF EXISTS _campaign_indicator;
			DROP TABLE IF EXISTS _to_agg;
			DROP TABLE IF EXISTS _tmp_agg;

			CREATE TABLE _campaign_indicator AS
			SELECT DISTINCT campaign_id, indicator_id FROM datapoint d
			WHERE d.cache_job_id = $1;

			CREATE TABLE _to_agg AS

			WITH RECURSIVE location_tree AS
					(
					-- non-recursive term ( rows where the components aren't
					-- master_indicators in another calculation )

					SELECT
						rg.parent_location_id
						,rg.parent_location_id as immediate_parent_id
						,rg.id as location_id
						,0 as lvl
					FROM location rg

					UNION ALL

					-- recursive term --
					SELECT
						r_recurs.parent_location_id
						,rt.parent_location_id as immediate_parent_id
						,rt.location_id
						,rt.lvl + 1
					FROM location AS r_recurs
					INNER JOIN location_tree AS rt
					ON (r_recurs.id = rt.parent_location_id)
				AND r_recurs.parent_location_id IS NOT NULL
			)

			SELECT DISTINCT
				d.id as datapoint_id
				,d.indicator_id
				,d.campaign_id
				,d.location_id
				,d.value
				,rt.parent_location_id
				,rt.immediate_parent_id
			FROM location_tree rt
			INNER JOIN datapoint d
			ON rt.location_id = d.location_id
			AND d.value IS NOT NULL
			INNER JOIN _campaign_indicator ci
			ON d.indicator_id = ci.indicator_id
			AND d.campaign_id = ci.campaign_id
			WHERE EXISTS (

						SELECT 1 -- DATA AT SAME locationAL LEVEL AS REQUESTED
						FROM location r
						WHERE r.parent_location_id = rt.parent_location_id
						AND rt.location_id = d.location_id

						UNION ALL

						SELECT 1-- DATA AT SAME locationAL LEVEL AS REQUESTED
						FROM location r
						WHERE r.id = rt.location_id
						AND r.parent_location_id IS NULL

			)
			and d.value IS NOT NULL
			and d.value != 'NaN';

			CREATE TABLE _tmp_agg AS

			SELECT DISTINCT
				d.datapoint_id
				,d.location_id
				,d.campaign_id
				,d.indicator_id
				,d.value
			FROM _to_agg d

			UNION ALL

			SELECT
				CAST(NULL AS INT) as id
				,d.parent_location_id
				,d.campaign_id
				,d.indicator_id
				,SUM(d.value) as value
			FROM _to_agg d

			WHERE NOT EXISTS (
				SELECT 1 FROM _to_agg ta
				WHERE d.immediate_parent_id = ta.location_id
				AND d.campaign_id = ta.campaign_id
				AND d.indicator_id = ta.indicator_id
			)
			AND NOT EXISTS (
				SELECT 1 FROM _to_agg ta
				WHERE d.parent_location_id = ta.location_id
				AND d.campaign_id = ta.campaign_id
				AND d.indicator_id = ta.indicator_id
			)
			AND d.parent_location_id is not null
			GROUP BY d.parent_location_id, d.campaign_id, d.indicator_id;

			CREATE UNIQUE INDEX rc_agg_ix ON _tmp_agg(location_id,campaign_id,indicator_id);

			-- OVERRIDES --
			UPDATE _tmp_agg ta
			SET   value = d.value
				, datapoint_id = d.id
			FROM datapoint d
			WHERE ta.location_id = d.location_id
			AND ta.campaign_id = d.campaign_id
			AND ta.indicator_id = d.indicator_id
			AND d.value IS NOT NULL
			AND d.value != 'NaN';

			-- DELETES in data entry (value is null) --
			DELETE FROM _tmp_agg ta
			USING datapoint d
			WHERE ta.location_id = d.location_id
			AND ta.campaign_id = d.campaign_id
			AND ta.indicator_id = d.indicator_id
			AND d.value IS NULL
			AND d.value != 'NaN';


			--- UPDATE THE REST OF THE DATAPOINT TABLE SO WE--
			--- WONT NEED TO RE-PROCESS THIS DATA AGAIN ---
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
			WHERE ta.location_id = ad.location_id
			AND ta.campaign_id = ad.campaign_id
			AND ta.indicator_id = ad.indicator_id;

			-- INSERT NEW --
			INSERT INTO agg_datapoint
			(location_id, campaign_id, indicator_id, value,cache_job_id)
			SELECT location_id, campaign_id, indicator_id, value, $1
			FROM _tmp_agg ta
			WHERE NOT EXISTS (
				SELECT 1 FROM agg_datapoint ad
				WHERE ta.location_id = ad.location_id
				AND ta.campaign_id = ad.campaign_id
				AND ta.indicator_id = ad.indicator_id
			);

			SELECT ad.location_id FROM agg_datapoint ad
			WHERE ad.cache_job_id = $1
			LIMIT 1;


	END
	$func$ LANGUAGE PLPGSQL;
