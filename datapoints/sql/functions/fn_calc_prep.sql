DROP FUNCTION IF EXISTS fn_calc_prep(cache_job_id int);
CREATE FUNCTION fn_calc_prep(cache_job_id int)
RETURNS TABLE(id int) AS
$func$
BEGIN


  -- http://stackoverflow.com/questions/19499461/postgresql-functions-execute-create-table-unexpected-results

	-- IN ORDER TO PERFORM THE CALCULATIONS NEEDED, WE NEED TO FIND --
	-- THE COMPONENT AND CALCULATED INDICATORS RELEVANT FOR THIS JOB --

	-- 1. find relevant calculated indicators create temp table
	-- 2. find relevand raw indicators needed for a claculation
	      --> the underlying indicator data hsould not be deleted/reinserted,
	      --> but we do need to be able to determine where this information
	      --> is to effect any downstream calculatiosn for this job.

				DROP TABLE IF EXISTS _region_campaign;
				DROP TABLE IF EXISTS _raw_indicators;
				DROP TABLE IF EXISTS _indicators_needed_to_calc;
				DROP TABLE IF EXISTS _tmp_calc_datapoint ;

				CREATE TABLE _region_campaign AS
				SELECT DISTINCT ad.region_id, ad.campaign_id
				FROM agg_datapoint ad
				WHERE ad.cache_job_id = $1;

				CREATE TABLE _raw_indicators AS
				SELECT DISTINCT ad.indicator_id
				FROM agg_datapoint ad
				WHERE ad.cache_job_id = $1
				;

				-----

				CREATE TABLE _indicators_needed_to_calc AS

				-- NOW FIND DATA THAT MUST BE PROCESSED BASED ON TMP TABLES ABOVE --
				WITH RECURSIVE ind_graph AS
				(
				-- non-recursive term ( rows where the components aren't
				-- master_indicators in another calculation )

					SELECT
							cic.id
						,cic.indicator_id
						,cic.indicator_component_id
						--,0 as lvl
					FROM calculated_indicator_component cic
					WHERE NOT EXISTS (
						SELECT 1 FROM calculated_indicator_component cic_leaf
						WHERE cic.indicator_component_id = cic_leaf.indicator_id
					)
					--AND calculation = 'PART_TO_BE_SUMMED'

					UNION ALL

					-- recursive term --
					SELECT
						cic_recurs.id
						,cic_recurs.indicator_id
						,ig.indicator_component_id
						--,ig.lvl + 1
					FROM calculated_indicator_component AS cic_recurs
					INNER JOIN ind_graph AS ig
					ON (cic_recurs.indicator_component_id = ig.indicator_id)
					--AND calculation = 'PART_TO_BE_SUMMED'
				)

				-- ALL MASTER INDICATORS ( AT ALL LEVELS ) --
				SELECT DISTINCT ig.indicator_id
				FROM ind_graph ig
				INNER JOIN _raw_indicators ri
				ON ri.indicator_id = indicator_component_id;

				CREATE UNIQUE INDEX uq_ind_ix ON _indicators_needed_to_calc (indicator_id);

				-- ALL COMPONENT INDICATORS NEEDED TO MAKE THE CALC --

				INSERT INTO _indicators_needed_to_calc
				(indicator_id)

				SELECT DISTINCT
					cic.indicator_component_id
				FROM calculated_indicator_component cic
				INNER JOIN _indicators_needed_to_calc intc
					ON cic.indicator_id = intc.indicator_id
				WHERE NOT EXISTS (
					SELECT 1 FROM _indicators_needed_to_calc tc
					WHERE cic.indicator_component_id = tc.indicator_id
				);


				CREATE TABLE _tmp_calc_datapoint AS

				SELECT DISTINCT
					ad.id
					,ad.region_id
					,ad.campaign_id
					,ad.indicator_id
					,ad.value
					,'t' as is_calc
				FROM agg_datapoint ad
				INNER JOIN _indicators_needed_to_calc intc
					ON ad.indicator_id = intc.indicator_id
					AND ad.value != 'Nan'
				INNER JOIN _region_campaign rc
					ON ad.region_id = rc.region_id
					AND ad.campaign_id = rc.campaign_id;

	CREATE UNIQUE INDEX uq_ix ON _tmp_calc_datapoint (region_id, campaign_id, indicator_id);

	DELETE FROM _tmp_calc_datapoint WHERE value = 'NaN'; -- FIX

	RETURN QUERY

	SELECT ad.id FROM agg_datapoint ad
	WHERE ad.cache_job_id = $1
	LIMIT 1;

END
$func$ LANGUAGE PLPGSQL;
