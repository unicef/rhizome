
DROP TABLE IF EXISTS calculated_datapoint;

CREATE TABLE calculated_datapoint AS

SELECT
	 row_number() OVER (ORDER BY d_part.campaign_id,part.indicator_id,d_part.region_id)  AS id
	,part.indicator_id as master_indicator_id
	,d_part.region_id
	,d_part.campaign_id
	,d_part.value / NULLIF(d_whole.value,0) as value
	,CAST(1 as BOOLEAN) as is_calc
FROM calculated_indicator_component part
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


DROP TABLE IF EXISTS _region_campaign_with_data;
CREATE TEMP TABLE _region_campaign_with_data
AS
SELECT 
	r.id as  region_id
	,c.id as campaign_id
FROM region r
INNER JOIN campaign c
ON 1=1
WHERE EXISTS (
	SELECT 1 FROM datapoint d
	WHERE r.id = d.region_id
)
AND EXISTS (
	SELECT 1 FROM datapoint d2
	WHERE c.id = d2.campaign_id
)
ORDER BY c.start_date DESC

SELECT * FROM (
	SELECT
		id
	FROM indicator i
	WHERE is_reported = 'f'

	UNION ALL

	SELECT id
	FROM indicator i 
	WHERE EXISTS ( 
		SELECT 1 FROM datapoint d
		WHERE i.id = d.indicator_id
	) -- Distinct Indicators --
)



SELECT generate_series AS date,
       b.desc AS TYPE,
       (random() * 10000 + 1)::int AS val
FROM generate_series((now() - '100 days'::interval)::date, now()::date, '1 day'::interval),
  (SELECT unnest(ARRAY['OSX', 'Windows', 'Linux']) AS DESC) b;