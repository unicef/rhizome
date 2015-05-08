
DROP FUNCTION IF EXISTS fn_calc_part_over_whole(cache_job_id int);
CREATE FUNCTION fn_calc_part_over_whole(cache_job_id int)
RETURNS TABLE(id int) AS
$func$
BEGIN

  ----- PART / WHOLE ------
  INSERT INTO _tmp_calc_datapoint
  (indicator_id,region_id,campaign_id,value)

  SELECT DISTINCT
  part.indicator_id as master_id
  ,d_part.region_id
  ,d_part.campaign_id
  ,d_part.value / NULLIF(d_whole.value,0) as value
  FROM calculated_indicator_component part
  INNER JOIN calculated_indicator_component whole
      ON part.indicator_id = whole.indicator_id
      AND whole.calculation = 'WHOLE'
      AND part.calculation = 'PART'
  INNER JOIN _tmp_calc_datapoint d_part
      ON part.indicator_component_id = d_part.indicator_id
  INNER JOIN _tmp_calc_datapoint d_whole
      ON whole.indicator_component_id = d_whole.indicator_id
      AND d_part.campaign_id = d_whole.campaign_id
      AND d_part.region_id = d_whole.region_id;

    RETURN QUERY

  	SELECT ad.id FROM agg_datapoint ad
  	--WHERE dwc.cache_job_id = $1
  	LIMIT 1;

  END
  $func$ LANGUAGE PLPGSQL;
