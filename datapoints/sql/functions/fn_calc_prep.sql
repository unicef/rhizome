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

		DROP TABLE IF EXISTS _tmp_indicator_lookup;
		CREATE TEMP TABLE _tmp_indicator_lookup
		AS
		SELECT DISTINCT
			cic.indicator_component_id as indicator_in
			, cic.indicator_id as indicator_out
			, CAST(1 AS BOOLEAN) as is_calc
		FROM calculated_indicator_component cic
		WHERE EXISTS (
			SELECT 1 FROM agg_datapoint d
			WHERE cic.indicator_component_id = d.indicator_id
			AND d.cache_job_id = $1
		)

		UNION ALL

		SELECT DISTINCT
				d.indicator_id as indicator_in
				, d.indicator_id as indicator_out
				, CAST(0 AS BOOLEAN) as is_calc
		FROM agg_datapoint d
		WHERE d.cache_job_id = $1;

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

 		WHERE NOT EXISTS (
 		SELECT 1 FROM _tmp_indicator_lookup til_exists
 		WHERE til.indicator_in = til_exists.indicator_in
 		AND til.indicator_out = til_exists.indicator_out
);

	-- now using the indicator_map create a temp table created above, find all of the information
	-- needed to perform all calucaltions for this job

	-- This table will be used, instead of the agg_datapoint table for the remainder of the calc process


	DROP TABLE IF EXISTS _tmp_calc_datapoint ;
	CREATE TABLE _tmp_calc_datapoint AS

	SELECT DISTINCT
		ad2.id
		,ad2.region_id
		,ad2.campaign_id
		,ad2.indicator_id
		,ad2.value
		,'t' as is_calc
	FROM agg_datapoint ad
	INNER JOIN _tmp_indicator_lookup til
		ON ad.indicator_id = til.indicator_in
		AND ad.value > 0
		AND ad.value != 'Nan'
	INNER JOIN agg_datapoint ad2
		ON ad.region_id = ad2.region_id
		AND ad.campaign_id = ad2.campaign_id
		AND ad2.indicator_id = til.indicator_out
	WHERE ad.cache_job_id = $1;

	CREATE UNIQUE INDEX uq_ix ON _tmp_calc_datapoint (region_id, campaign_id, indicator_id);

	DELETE FROM _tmp_calc_datapoint WHERE value = 'NaN'; -- FIX

	RETURN QUERY

	SELECT ad.id FROM agg_datapoint ad
	--WHERE dwc.cache_job_id = $1
	LIMIT 1;

END
$func$ LANGUAGE PLPGSQL;
