
DROP FUNCTION IF EXISTS fn_calc_part_over_whole(cache_job_id int);
CREATE FUNCTION fn_calc_part_over_whole(cache_job_id int)
RETURNS TABLE(id int) AS
$func$
BEGIN

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


    RETURN QUERY

  	SELECT ad.id FROM agg_datapoint ad
  	--WHERE dwc.cache_job_id = $1
  	LIMIT 1;

  END
  $func$ LANGUAGE PLPGSQL;
