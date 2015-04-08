DROP FUNCTION IF EXISTS fn_calc_datapoint(cache_job_id int);
CREATE FUNCTION fn_calc_datapoint(cache_job_id int)
RETURNS TABLE(id int) AS
$func$
BEGIN

	PERFORM * FROM fn_calc_prep($1);


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
    	FROM _tmp_agg_datapoint
    	WHERE is_calc = 'f';

         ---- SUM OF PARTS ------
        INSERT INTO datapoint_with_computed
        (indicator_id,region_id,campaign_id,value,cache_job_id)

        SELECT DISTINCT
		cic.indicator_id
		,ad.region_id
		,ad.campaign_id
		,SUM(ad.value) as value
		,$1
        FROM _tmp_agg_datapoint ad
        INNER JOIN calculated_indicator_component cic
            ON ad.indicator_id = cic.indicator_component_id
            AND cic.calculation = 'PART_TO_BE_SUMMED'
-- 	WHERE NOT EXISTS (  -- LEAF LEVEL INDICATORS --
-- 		SELECT 1 FROM calculated_indicator_component cic2
-- 		WHERE cic.indicator_id = cic2.indicator_component_id
-- 	)
        GROUP BY ad.campaign_id, ad.region_id, cic.indicator_id,ad.cache_job_id;


        ----- PART / WHOLE ------
        INSERT INTO datapoint_with_computed
        (indicator_id,region_id,campaign_id,value,cache_job_id)

        SELECT DISTINCT
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

        SELECT DISTINCT
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
          	FROM _tmp_agg_datapoint ad
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
          	FROM _tmp_agg_datapoint ad
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
          	FROM _tmp_agg_datapoint ad
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
