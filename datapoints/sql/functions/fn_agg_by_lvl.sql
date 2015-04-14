DROP FUNCTION IF EXISTS fn_agg_by_lvl(lvl INT);
CREATE FUNCTION fn_agg_by_lvl(lvl INT)

RETURNS TABLE(
	parent_region_id INT
) AS
$func$
BEGIN

	INSERT INTO _tmp_agg_data
	(id, region_id, campaign_id, indicator_id, value)
	SELECT NULL, r.parent_region_id, tad.campaign_id, tad.indicator_id, SUM(value) as val_sum
	FROM _reg_tree rt
	INNER JOIN region r
		ON rt.parent_region_id = r.parent_region_id
	INNER JOIN _tmp_agg_data tad
		ON r.id = tad.region_id
	WHERE rt.lvl = $1
	GROUP BY r.parent_region_id, tad.campaign_id, tad.indicator_id;

	UPDATE _reg_tree rt
	SET is_processed = 't'
	WHERE rt.lvl = $1;

	RETURN QUERY

	SELECT rt.parent_region_id FROM _reg_tree rt
	WHERE rt.lvl = $1

;

END
$func$ LANGUAGE PLPGSQL;
