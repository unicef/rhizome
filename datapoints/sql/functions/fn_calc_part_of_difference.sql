DROP FUNCTION IF EXISTS fn_calc_part_of_difference(cache_job_id int);
CREATE FUNCTION fn_calc_part_of_difference(cache_job_id int)
RETURNS TABLE(id int) AS
$func$
BEGIN

INSERT INTO _tmp_calc_datapoint
(indicator_id,location_id,campaign_id,value)

  SELECT indicator_id,x.location_id,x.campaign_id, x.calculated_value
  FROM (
  SELECT DISTINCT
    		denom.master_id
    		,denom.location_id
    		,denom.campaign_id
    		,(CAST(num_whole.value as FLOAT) - CAST(num_part.value as FLOAT)) / NULLIF(CAST(denom.value AS FLOAT),0) as calculated_value
              FROM (
              	SELECT
              		cic.indicator_id as master_id
              		,ad.location_id
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
          		,ad.location_id
          		,ad.indicator_id
          		,ad.campaign_id
          		,ad.value
          	FROM  _tmp_calc_datapoint ad
          	INNER JOIN calculated_indicator_component cic
          	ON cic.indicator_component_id = ad.indicator_id
          	AND calculation = 'WHOLE_OF_DIFFERENCE'
          )num_whole
          ON num_part.master_id = num_whole.master_id
          AND num_part.location_id = num_whole.location_id
          AND num_part.campaign_id = num_whole.campaign_id

          INNER JOIN
          (
          	SELECT
          		cic.indicator_id as master_id
          		,ad.location_id
          		,ad.indicator_id
          		,ad.campaign_id
          		,ad.value
          	FROM _tmp_calc_datapoint ad
          	INNER JOIN calculated_indicator_component cic
          	ON cic.indicator_component_id = ad.indicator_id
          	AND calculation = 'WHOLE_OF_DIFFERENCE_DENOMINATOR'
          )denom
          ON num_whole.location_id = denom.location_id
          AND num_whole.master_id = denom.master_id
          AND num_whole.campaign_id = denom.campaign_id
    )x
    WHERE NOT EXISTS (

    SELECT 1 FROM _tmp_calc_datapoint t
    WHERE x.location_id = t.location_id
    AND x.campaign_id = t.campaign_id
    AND x.indicator_id = t.indicator_id
    );

    RETURN QUERY

    SELECT ad.id FROM agg_datapoint ad
    --WHERE dwc.cache_job_id = $1
    LIMIT 1;

END
$func$ LANGUAGE PLPGSQL;
