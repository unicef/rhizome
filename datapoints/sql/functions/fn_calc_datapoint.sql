DROP FUNCTION IF EXISTS fn_calc_datapoint(cache_job_id int);
CREATE FUNCTION fn_calc_datapoint(cache_job_id int)
RETURNS TABLE(id int) AS $$

	-- delete before reinsert --

	DELETE FROM datapoint_with_computed dwc
	USING agg_datapoint ad
	INNER JOIN ( -- a table with all of the idicators needed for a calculation
		SELECT 
			cic.indicator_component_id as input_indicator_id
			,cic_all.indicator_component_id as output_indicator_id
		FROM calculated_indicator_component cic
		INNER JOIN calculated_indicator_component cic_all
		ON cic.indicator_id = cic_all.indicator_id

		UNION ALL
		
		SELECT 
			cic.indicator_component_id as input_indicator
			,cic.indicator_id as output_indicator
		FROM calculated_indicator_component cic
	)x
	ON ad.indicator_id = x.input_indicator_id
	WHERE dwc.campaign_id = ad.campaign_id
	AND dwc.region_id = ad.region_id
	AND ad.cache_job_id = $1
	AND x.output_indicator_id = dwc.indicator_id;

	-- insert agg data (no calculation) --
   	INSERT INTO datapoint_with_computed
    	(indicator_id,region_id,campaign_id,value,is_agg,cache_job_id)

    	SELECT
    		indicator_id
    		,region_id
    		,campaign_id
    		,value
    		,is_agg
    		,cache_job_id
    	FROM agg_datapoint
    	WHERE cache_job_id = $1;

         ---- SUM OF PARTS ------
        INSERT INTO datapoint_with_computed
        (indicator_id,region_id,campaign_id,value,cache_job_id)

        SELECT
		cic.indicator_id
		,ad.region_id
		,ad.campaign_id
		,SUM(ad.value) as value
		,cache_job_id
        FROM agg_datapoint ad
        INNER JOIN calculated_indicator_component cic
            ON ad.indicator_id = cic.indicator_component_id
            AND cic.calculation = 'PART_TO_BE_SUMMED'
	    AND ad.cache_job_id = $1
--     	    AND ad.cache_job_id = 91
--     	    AND cic.indicator_id = 251
--     	    AND region_id = 65327
--     	    AND campaign_id = 111
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
        FROM(
          SELECT max(id) as max_dp_id FROM datapoint_with_computed
        ) x
        INNER JOIN calculated_indicator_component part
            ON 1 = 1
        INNER JOIN calculated_indicator_component whole
            ON part.indicator_id = whole.indicator_id
            AND whole.calculation = 'WHOLE'
            AND part.calculation = 'PART'
        INNER JOIN datapoint_with_computed d_part
            ON part.indicator_component_id = d_part.indicator_id
        INNER JOIN datapoint_with_computed d_whole
            ON whole.indicator_component_id = d_whole.indicator_id
            AND d_part.campaign_id = d_whole.campaign_id
            AND d_part.region_id = d_whole.region_id
            WHERE (d_part.cache_job_id = $1 or d_whole.cache_job_id = $1);

--         INSERT INTO datapoint_with_computed
--         (indicator_id,region_id,campaign_id,value,cache_job_id)
-- 
--         SELECT
-- 		denom.master_indicator_id
-- 		,denom.region_id
-- 		,denom.campaign_id
-- 		,(CAST(num_whole.value as FLOAT) - CAST(num_part.value as FLOAT)) / NULLIF(CAST(denom.value AS FLOAT),0) as calculated_value
--                , $1
--           FROM (
--           	SELECT
--           		cic.indicator_id as master_indicator_id
--           		,ad.region_id
--           		,ad.indicator_id
--           		,ad.campaign_id
--           		,ad.value
-- 			,ad.cache_job_id
--           	FROM agg_datapoint ad
--           	INNER JOIN calculated_indicator_component cic
--           	ON cic.indicator_component_id = ad.indicator_id
--           	AND calculation = 'PART_OF_DIFFERENCE'
--           	AND ad.cache_job_id = $1
--           )num_part
-- 
--           INNER JOIN (
--           	SELECT
--           		cic.indicator_id as master_indicator_id
--           		,ad.region_id
--           		,ad.indicator_id
--           		,ad.campaign_id
--           		,ad.value
-- 			,ad.cache_job_id
--           	FROM agg_datapoint ad
--           	INNER JOIN calculated_indicator_component cic
--           	ON cic.indicator_component_id = ad.indicator_id
--           	AND calculation = 'WHOLE_OF_DIFFERENCE'
-- 		AND ad.cache_job_id = $1
-- 
--           )num_whole
--           ON num_part.master_indicator_id = num_whole.master_indicator_id
--           AND num_part.region_id = num_whole.region_id
--           AND num_part.campaign_id = num_whole.campaign_id
-- 
--           INNER JOIN
--           (
--           	SELECT
--           		cic.indicator_id as master_indicator_id
--           		,ad.region_id
--           		,ad.indicator_id
--           		,ad.campaign_id
--           		,ad.value
--           		,ad.cache_job_id
--           	FROM agg_datapoint ad
--           	INNER JOIN calculated_indicator_component cic
--           	ON cic.indicator_component_id = ad.indicator_id
--           	AND calculation = 'WHOLE_OF_DIFFERENCE_DENOMINATOR'
-- 		AND ad.cache_job_id = $1
--           )denom
--           ON num_whole.region_id = denom.region_id
--           AND num_whole.master_indicator_id = denom.master_indicator_id
--           AND num_whole.campaign_id = denom.campaign_id;

	-- FIX ME --
	UPDATE datapoint_with_computed SET value = 0.00 
	WHERE cache_job_id = $1
	AND value is NULL;

	SELECT id FROM datapoint_with_computed
	WHERE indicator_id = $1
	LIMIT 1;

    $$

    LANGUAGE SQL;
