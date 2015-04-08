

DROP FUNCTION IF EXISTS fn_calc_sum_of_parts(cache_job_id int);
CREATE FUNCTION fn_calc_sum_of_parts(cache_job_id int)
RETURNS TABLE(id int) AS
$func$
BEGIN

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
      -- 	SELECT 1 FROM calculated_indicator_component cic2
      -- 	WHERE cic.indicator_id = cic2.indicator_component_id
  -- 	)
  GROUP BY ad.campaign_id, ad.region_id, cic.indicator_id,ad.cache_job_id;


	RETURN QUERY

	SELECT ad.id FROM agg_datapoint ad
	--WHERE dwc.cache_job_id = $1
	LIMIT 1;

END
$func$ LANGUAGE PLPGSQL;
