DROP FUNCTION IF EXISTS fn_agg_datapoint(region_type_id);
CREATE FUNCTION fn_agg_datapoint() 
RETURNS TABLE(id int)
    AS $$

	DELETE FROM  agg_datapoint
	INNER JOIN region r
	ON ad.region_id = r.id
	AND r.region_type_id = $1;

	INSERT INTO agg_datapoint
	(region_id, campaign_id, indicator_id, value, is_agg)

	SELECT
		region_id, campaign_id, indicator_id, value, 't'
	FROM datapoint d
	WHERE NOT EXISTS (
		SELECT 1 FROM agg_datapoint ad
		WHERE d.indicator_id = ad.indicator_id
		AND d.campaign_id = ad.campaign_id
		AND d.region_id = ad.indicator_id
	);



	    INSERT INTO agg_datapoint
	    (region_id, campaign_id, indicator_id, value, is_agg)

	    SELECT
		r.parent_region_id, campaign_id, indicator_id, SUM(COALESCE(value,0)), 't'
	    FROM agg_datapoint ag
	    INNER JOIN region r
		ON ag.region_id = r.id
		AND r.region_type_id = 1$
	    WHERE NOT EXISTS (
		SELECT 1 FROM agg_datapoint ag_2
		WHERE 1 = 1
		AND ag.indicator_id = ag_2.indicator_id
		AND ag.campaign_id = ag_2.campaign_id
		AND r.parent_region_id = ag_2.region_id
	    )
	    GROUP BY r.parent_region_id, ag.indicator_id, ag.campaign_id;

    SELECT id FROM agg_datapoint LIMIT 1;

    $$
    LANGUAGE SQL;
