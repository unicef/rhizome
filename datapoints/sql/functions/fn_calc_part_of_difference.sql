DROP FUNCTION IF EXISTS fn_calc_part_of_difference(cache_job_id int);
CREATE FUNCTION fn_calc_part_of_difference(cache_job_id int)
RETURNS TABLE(id int) AS
$func$
BEGIN

        INSERT INTO _tmp_calc_datapoint
        (indicator_id,region_id,campaign_id,value)

        SELECT DISTINCT
    		denom.master_id
    		,denom.region_id
    		,denom.campaign_id
    		,(CAST(num_whole.value as FLOAT) - CAST(num_part.value as FLOAT)) / NULLIF(CAST(denom.value AS FLOAT),0) as calculated_value
              FROM (
              	SELECT
              		cic.indicator_id as master_id
              		,ad.region_id
              		,ad.indicator_id
              		,ad.campaign_id
              		,ad.value
              	FROM _tmp_calc_datapoint ad
              	INNER JOIN calculated_indicator_component cic
              	ON cic.indicator_component_id = ad.indicator_id
              	AND calculation = 'PART_OF_DIFFERENCE'
              )num_part

          INNER JOIN (
          	SELECT
          		cic.indicator_id as master_id
          		,ad.region_id
          		,ad.indicator_id
          		,ad.campaign_id
          		,ad.value
          	FROM  _tmp_calc_datapoint ad
          	INNER JOIN calculated_indicator_component cic
          	ON cic.indicator_component_id = ad.indicator_id
          	AND calculation = 'WHOLE_OF_DIFFERENCE'
          )num_whole
          ON num_part.master_id = num_whole.master_id
          AND num_part.region_id = num_whole.region_id
          AND num_part.campaign_id = num_whole.campaign_id

          INNER JOIN
          (
          	SELECT
          		cic.indicator_id as master_id
          		,ad.region_id
          		,ad.indicator_id
          		,ad.campaign_id
          		,ad.value
          	FROM _tmp_calc_datapoint ad
          	INNER JOIN calculated_indicator_component cic
          	ON cic.indicator_component_id = ad.indicator_id
          	AND calculation = 'WHOLE_OF_DIFFERENCE_DENOMINATOR'
          )denom
          ON num_whole.region_id = denom.region_id
          AND num_whole.master_id = denom.master_id
          AND num_whole.campaign_id = denom.campaign_id;

    RETURN QUERY

    SELECT ad.id FROM agg_datapoint ad
    --WHERE dwc.cache_job_id = $1
    LIMIT 1;

END
$func$ LANGUAGE PLPGSQL;
