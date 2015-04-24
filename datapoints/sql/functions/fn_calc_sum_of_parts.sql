DROP FUNCTION IF EXISTS fn_calc_sum_of_parts(cache_job_id int);
CREATE FUNCTION fn_calc_sum_of_parts(cache_job_id int)
RETURNS TABLE(id int) AS
$func$
BEGIN

  ---- SUM OF PARTS ------

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
  	AND calculation = 'PART_TO_BE_SUMMED'

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
  	AND calculation = 'PART_TO_BE_SUMMED'

    )

    INSERT INTO _tmp_calc_datapoint
    (indicator_id,region_id,campaign_id,value)

    SELECT
        ig.indicator_id
      , dwc.region_id
      , dwc.campaign_id
      , SUM(dwc.value) as agg_value
    FROM ind_graph ig
    INNER JOIN _tmp_calc_datapoint dwc
        ON 1 = 1
        AND ig.indicator_component_id = dwc.indicator_id
    AND NOT EXISTS (
      SELECT 1 FROM _tmp_calc_datapoint tcd
      WHERE dwc.region_id = tcd.region_id
      AND dwc.campaign_id = tcd.campaign_id
      AND ig.indicator_id = tcd.indicator_id
    )

    GROUP BY ig.indicator_id, dwc.region_id, dwc.campaign_id;

	RETURN QUERY

	SELECT ad.id FROM agg_datapoint ad
	--WHERE dwc.cache_job_id = $1
	LIMIT 1;

END
$func$ LANGUAGE PLPGSQL;
