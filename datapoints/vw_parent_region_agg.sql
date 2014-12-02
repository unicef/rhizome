CREATE VIEW parent_region_agg
AS

SELECT 
	row_number() OVER (ORDER BY r.parent_region_id,d.indicator_id,campaign_id) AS id
	,r.parent_region_id
	,d.indicator_id
	,campaign_id
	,sum(d.value) as the_sum
FROM datapoint d 
INNER JOIN region r 
ON d.region_id = r.id
GROUP BY r.parent_region_id,d.indicator_id,campaign_id;

