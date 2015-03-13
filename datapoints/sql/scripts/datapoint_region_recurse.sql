
WITH RECURSIVE agg_region
(indicator_id, campaign_id, region_id, value) AS (

SELECT 
	d.indicator_id
	,d.campaign_id
	,d.region_id
	,d.value
	,0 as agg_level
FROM datapoint d

UNION ALL

SELECT 
	indicator_id
	,campaign_id
	,r.parent_region_id
	,ag.value
	,agg_level + 1 as agg_level
FROM region r, agg_region ag 
WHERE ag.region_id = r.id
AND ag.agg_level < 5
)

SELECT * FROM agg_region;