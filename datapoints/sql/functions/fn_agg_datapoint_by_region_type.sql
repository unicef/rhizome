DROP FUNCTION IF EXISTS fn_agg_datapoint();
CREATE FUNCTION fn_agg_datapoint() 
RETURNS TABLE(id int)
    AS $$

    TRUNCATE TABLE agg_datapoint;

    INSERT INTO agg_datapoint
    (region_id, campaign_id, indicator_id, value, is_agg)

    SELECT
        region_id, campaign_id, indicator_id, value, 't'
    FROM datapoint d
    WHERE value != 'NaN'
    AND NOT EXISTS (
        SELECT 1 FROM calculated_indicator_component cic
        WHERE d.indicator_id = cic.indicator_id);


    INSERT INTO agg_datapoint
    (region_id, campaign_id, indicator_id, value, is_agg)

    SELECT
	r.parent_region_id, campaign_id, indicator_id, SUM(COALESCE(value,0)), 't'
    FROM agg_datapoint ag
    INNER JOIN region r
	ON ag.region_id = r.id
    INNER JOIN region_type rt
	ON r.region_type_id = rt.id
	AND rt.name = 'settlement'
    WHERE NOT EXISTS (
	SELECT 1 FROM agg_datapoint ag_2
	WHERE 1 = 1
	AND ag.indicator_id = ag_2.indicator_id
	AND ag.campaign_id = ag_2.campaign_id
	AND r.parent_region_id = ag_2.region_id
    )
    GROUP BY r.parent_region_id, ag.indicator_id, ag.campaign_id;

	----

    INSERT INTO agg_datapoint
    (region_id, campaign_id, indicator_id, value, is_agg)

    SELECT
	r.parent_region_id, campaign_id, indicator_id, SUM(COALESCE(value,0)), 't'
    FROM agg_datapoint ag
    INNER JOIN region r
	ON ag.region_id = r.id
    INNER JOIN region_type rt
	ON r.region_type_id = rt.id
	AND rt.name = 'sub-district'
    WHERE NOT EXISTS (
	SELECT 1 FROM agg_datapoint ag_2
	WHERE 1 = 1
	AND ag.indicator_id = ag_2.indicator_id
	AND ag.campaign_id = ag_2.campaign_id
	AND r.parent_region_id = ag_2.region_id
    )
    GROUP BY r.parent_region_id, ag.indicator_id, ag.campaign_id;

    ----

    INSERT INTO agg_datapoint
    (region_id, campaign_id, indicator_id, value, is_agg)

    SELECT
	r.parent_region_id, campaign_id, indicator_id, SUM(COALESCE(value,0)), 't'
    FROM agg_datapoint ag
    INNER JOIN region r
	ON ag.region_id = r.id
    INNER JOIN region_type rt
	ON r.region_type_id = rt.id
	AND rt.name = 'district'
    WHERE NOT EXISTS (
	SELECT 1 FROM agg_datapoint ag_2
	WHERE 1 = 1
	AND ag.indicator_id = ag_2.indicator_id
	AND ag.campaign_id = ag_2.campaign_id
	AND r.parent_region_id = ag_2.region_id
    )
    GROUP BY r.parent_region_id, ag.indicator_id, ag.campaign_id;

    ----

    INSERT INTO agg_datapoint
    (region_id, campaign_id, indicator_id, value, is_agg)

    SELECT
	r.parent_region_id, campaign_id, indicator_id, SUM(COALESCE(value,0)), 't'
    FROM agg_datapoint ag
    INNER JOIN region r
	ON ag.region_id = r.id
    INNER JOIN region_type rt
	ON r.region_type_id = rt.id
	AND rt.name = 'district'
    WHERE NOT EXISTS (
	SELECT 1 FROM agg_datapoint ag_2
	WHERE 1 = 1
	AND ag.indicator_id = ag_2.indicator_id
	AND ag.campaign_id = ag_2.campaign_id
	AND r.parent_region_id = ag_2.region_id
    )
    GROUP BY r.parent_region_id, ag.indicator_id, ag.campaign_id;

    ----

    
    INSERT INTO agg_datapoint
    (region_id, campaign_id, indicator_id, value, is_agg)

    SELECT
	r.parent_region_id, campaign_id, indicator_id, SUM(COALESCE(value,0)), 't'
    FROM agg_datapoint ag
    INNER JOIN region r
	ON ag.region_id = r.id
    INNER JOIN region_type rt
	ON r.region_type_id = rt.id
	AND rt.name = 'province'
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
