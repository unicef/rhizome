DROP FUNCTION IF EXISTS fn_calc_sum_of_parts(cache_job_id int);
CREATE FUNCTION fn_calc_sum_of_parts(cache_job_id int)
RETURNS TABLE(id int) AS
$func$
BEGIN

---- SUM OF PARTS ------
INSERT INTO _tmp_calc_datapoint
(indicator_id,region_id,campaign_id,value)

SELECT
  cic.indicator_id
  ,tcd.region_id
  ,tcd.campaign_id
  ,SUM(tcd.value) as value
FROM  _tmp_calc_datapoint tcd
INNER JOIN calculated_indicator_component cic
  ON tcd.indicator_id = cic.indicator_component_id
  AND cic.calculation = 'PART_TO_BE_SUMMED'
WHERE cic.indicator_id != 265
GROUP BY tcd.campaign_id, tcd.region_id, cic.indicator_id;

---- SUM OF PARTS ------
INSERT INTO _tmp_calc_datapoint
(indicator_id,region_id,campaign_id,value)

SELECT
  cic.indicator_id
  ,tcd.region_id
  ,tcd.campaign_id
  ,SUM(tcd.value) as value
FROM  _tmp_calc_datapoint tcd
INNER JOIN calculated_indicator_component cic
  ON tcd.indicator_id = cic.indicator_component_id
  AND cic.calculation = 'PART_TO_BE_SUMMED'
-- WHERE NOT EXISTS (
--   SELECT 1 FROM _tmp_calc_datapoint tcd_exists
--   WHERE tcd.region_id = tcd_exists.region_id
--   AND tcd.indicator_id = tcd_exists.indicator_id
--   AND tcd.campaign_id = tcd_exists.campaign_id
-- )
WHERE cic.indicator_id = 265
GROUP BY tcd.campaign_id, tcd.region_id, cic.indicator_id;


/*
WITH RECURSIVE ind_graph AS
(
    -- non-recursive term ( rows where the components aren't
    -- master_indicators in another calculation )

	SELECT
		id
		,indicator_id
		,indicator_component_id
		,0 as lvl
	FROM calculated_indicator_component cic
	WHERE NOT EXISTS (
		SELECT 1 FROM calculated_indicator_component cic_leaf
		WHERE cic.indicator_component_id = cic_leaf.indicator_id
	)
	AND calculation = 'PART_TO_BE_SUMMED'

	UNION ALL

	-- recursive term
	SELECT
		cic_recurs.id
		,cic_recurs.indicator_id
		,cic_recurs.indicator_component_id
		,ig.lvl + 1
	FROM calculated_indicator_component AS cic_recurs
	INNER JOIN ind_graph AS ig
	ON (cic_recurs.indicator_component_id = ig.indicator_id)
	AND calculation = 'PART_TO_BE_SUMMED'
	)

SELECT *
FROM ind_graph
ORDER BY lvl DESC;
*/



	RETURN QUERY

	SELECT ad.id FROM agg_datapoint ad
	--WHERE dwc.cache_job_id = $1
	LIMIT 1;

END
$func$ LANGUAGE PLPGSQL;
