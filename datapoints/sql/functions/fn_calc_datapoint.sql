DROP FUNCTION IF EXISTS fn_calc_datapoint(cache_job_id int);
CREATE FUNCTION fn_calc_datapoint(cache_job_id int)
RETURNS TABLE(id int) AS
$func$
BEGIN
	
	--http://stackoverflow.com/questions/19499461/postgresql-functions-execute-create-table-unexpected-results

	-- IN ORDER TO PERFORM THE CALCULATIONS NEEDED, WE NEED TO FIND -- 
	-- THE COMPONENT AND CALCULATED INDICATORS RELEVANT FOR THIS JOB --

	-- 1. find relevant calculated indicators create temp table
	-- 2. find relevand raw indicators needed for a claculation
	      --> the underlying indicator data hsould not be deleted/reinserted,
	      --> but we do need to be able to determine where this information 
	      --> is to effect any downstream calculatiosn for this job.
	      
	EXECUTE FORMAT ('

		DROP TABLE IF EXISTS _tmp_indicator_lookup;
		CREATE TABLE _tmp_indicator_lookup 
		AS
		SELECT DISTINCT
			cic.indicator_component_id as indicator_in
			, cic.indicator_id as indicator_out
			, CAST(1 AS BOOLEAN) as is_calc
		FROM calculated_indicator_component cic
		WHERE EXISTS ( 
			SELECT 1 FROM agg_datapoint d 
			WHERE cic.indicator_component_id = d.indicator_id
			AND cache_job_id = %1$s
		);',$1
	);

	-- NOW INSERT THE INDICATORS NEEDED TO MAKE THE CALCULATION --
	INSERT INTO _tmp_indicator_lookup
	(indicator_in, indicator_out, is_calc)

	SELECT 
		indicator_in
		, cic.indicator_component_id
		, CAST(0 AS BOOLEAN) AS is_calc
	FROM _tmp_indicator_lookup
	INNER JOIN calculated_indicator_component cic
	ON indicator_out = cic.indicator_id;
	
	-- now using the indicator_map create a temp table created above, find all of the information
	-- needed to perform all calucaltions for this job 
	 
	-- This table will be used, instead of the agg_datapoint table for the remainder of the calc process 

	EXECUTE FORMAT ('
	DROP TABLE IF EXISTS _tmp_agg_datpoint ;
	CREATE TEMP TABLE _tmp_agg_datpoint AS

	SELECT 
		ad2.*
		,til.is_calc
	FROM agg_datapoint ad
	INNER JOIN _tmp_indicator_lookup til
		ON ad.indicator_id = til.indicator_in
	INNER JOIN agg_datapoint ad2
		ON ad.region_id = ad2.region_id
		AND ad.campaign_id = ad2.campaign_id
		AND ad2.indicator_id = til.indicator_out
	WHERE ad.cache_job_id = %1$s;',$1
	);

	-- DONE CREATING ALL TEMP TABLES -- 

	----------------------------
	-- delete before reinsert --
	----------------------------

	DELETE FROM datapoint_with_computed dwc
	USING _tmp_agg_datpoint ad
	WHERE dwc.campaign_id = ad.campaign_id
	AND dwc.region_id = ad.region_id
	AND dwc.indicator_id = ad.indicator_id;

	-- insert agg data (no calculation) --
   	INSERT INTO datapoint_with_computed
    	(indicator_id,region_id,campaign_id,value,is_agg,cache_job_id)

    	SELECT
    		indicator_id
    		,region_id
    		,campaign_id
    		,value
    		,is_agg
    		,$1
    	FROM _tmp_agg_datpoint
    	WHERE is_calc = 'f';

         ---- SUM OF PARTS ------
        INSERT INTO datapoint_with_computed
        (indicator_id,region_id,campaign_id,value,cache_job_id)

        SELECT
		cic.indicator_id
		,ad.region_id
		,ad.campaign_id
		,SUM(ad.value) as value
		,$1
        FROM _tmp_agg_datpoint ad
        INNER JOIN calculated_indicator_component cic
            ON ad.indicator_id = cic.indicator_component_id
            AND cic.calculation = 'PART_TO_BE_SUMMED'
        GROUP BY ad.campaign_id, ad.region_id, cic.indicator_id,ad.cache_job_id;

        ----- PART / WHOLE ------
        INSERT INTO datapoint_with_computed
        (indicator_id,region_id,campaign_id,value,cache_job_id)

        SELECT
		part.indicator_id as master_indicator_id
		,d_part.region_id
		,d_part.campaign_id
		,d_part.value / NULLIF(d_whole.value,0) as value
		,$1
        FROM calculated_indicator_component part
        INNER JOIN calculated_indicator_component whole
            ON part.indicator_id = whole.indicator_id
            AND whole.calculation = 'WHOLE'
            AND part.calculation = 'PART'
        INNER JOIN datapoint_with_computed d_part
            ON part.indicator_component_id = d_part.indicator_id
            AND d_part.cache_job_id = $1
        INNER JOIN datapoint_with_computed d_whole
            ON whole.indicator_component_id = d_whole.indicator_id
            AND d_part.campaign_id = d_whole.campaign_id
            AND d_part.region_id = d_whole.region_id
            AND d_whole.cache_job_id = $1;
            

        INSERT INTO datapoint_with_computed
        (indicator_id,region_id,campaign_id,value,cache_job_id)

        SELECT
		denom.master_indicator_id
		,denom.region_id
		,denom.campaign_id
		,(CAST(num_whole.value as FLOAT) - CAST(num_part.value as FLOAT)) / NULLIF(CAST(denom.value AS FLOAT),0) as calculated_value
               ,$1
          FROM (
          	SELECT
          		cic.indicator_id as master_indicator_id
          		,ad.region_id
          		,ad.indicator_id
          		,ad.campaign_id
          		,ad.value
			,ad.cache_job_id
          	FROM _tmp_agg_datpoint ad
          	INNER JOIN calculated_indicator_component cic
          	ON cic.indicator_component_id = ad.indicator_id
          	AND calculation = 'PART_OF_DIFFERENCE'
          )num_part

          INNER JOIN (
          	SELECT
          		cic.indicator_id as master_indicator_id
          		,ad.region_id
          		,ad.indicator_id
          		,ad.campaign_id
          		,ad.value
			,ad.cache_job_id
          	FROM _tmp_agg_datpoint ad
          	INNER JOIN calculated_indicator_component cic
          	ON cic.indicator_component_id = ad.indicator_id
          	AND calculation = 'WHOLE_OF_DIFFERENCE'
          )num_whole
          ON num_part.master_indicator_id = num_whole.master_indicator_id
          AND num_part.region_id = num_whole.region_id
          AND num_part.campaign_id = num_whole.campaign_id

          INNER JOIN
          (
          	SELECT
          		cic.indicator_id as master_indicator_id
          		,ad.region_id
          		,ad.indicator_id
          		,ad.campaign_id
          		,ad.value
          		,ad.cache_job_id
          	FROM _tmp_agg_datpoint ad
          	INNER JOIN calculated_indicator_component cic
          	ON cic.indicator_component_id = ad.indicator_id
          	AND calculation = 'WHOLE_OF_DIFFERENCE_DENOMINATOR'
          )denom
          ON num_whole.region_id = denom.region_id
          AND num_whole.master_indicator_id = denom.master_indicator_id
          AND num_whole.campaign_id = denom.campaign_id;

	-- FIX ME --
	UPDATE datapoint_with_computed SET value = 0.00 
	--WHERE cache_job_id = $1
	WHERE value is NULL;

	-- FIX ME -- 
	DELETE FROM datapoint_with_computed dwc
	WHERE region_id is null;
	
	RETURN QUERY
	
	SELECT ad.id FROM agg_datapoint ad
	--WHERE dwc.cache_job_id = $1
	LIMIT 1;

END
$func$ LANGUAGE PLPGSQL;


SELECT * FROM fn_calc_datapoint(-1)

