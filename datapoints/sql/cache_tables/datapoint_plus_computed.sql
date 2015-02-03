

DROP TABLE IF EXISTS datapoint_with_computed;
CREATE TABLE datapoint_with_computed AS

SELECT
ID
,indicator_id
,region_id
,campaign_id
,value
,CAST(0 as BOOLEAN) as is_calc
FROM datapoint

UNION ALL

SELECT
x.max_dp_id + row_number() OVER (ORDER BY d_part.campaign_id,part.indicator_id,d_part.region_id)  AS id
,part.indicator_id as master_indicator_id
,d_part.region_id
,d_part.campaign_id
,d_part.value / NULLIF(d_whole.value,0) as value
,CAST(1 as BOOLEAN) as is_calc
FROM
(
	SELECT max(id) as max_dp_id FROM datapoint
) x
INNER JOIN calculated_indicator_component part
ON 1=1
INNER JOIN calculated_indicator_component whole
ON part.indicator_id = whole.indicator_id
AND whole.calculation = 'WHOLE'
AND part.calculation = 'PART'
INNER JOIN datapoint d_part
ON part.indicator_component_id = d_part.indicator_id
INNER JOIN datapoint d_whole
ON whole.indicator_component_id = d_whole.indicator_id
AND d_part.campaign_id = d_whole.campaign_id
AND d_part.region_id = d_whole.region_id;

GRANT SELECT ON datapoint_with_computed TO djangoapp;
