
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


DROP TABLE IF EXISTS datapoint_abstracted;
CREATE TABLE datapoint_abstracted
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
ORDER BY c.start_date DESC;


DROP TABLE IF EXISTS _indicators_with_data;

CREATE TEMP TABLE _indicators_with_data AS
SELECT 
	row_number() OVER (order by x.id) as looper
	,x.id as indicator_id
	,CAST(NULL AS TIMESTAMP) AS process_start_time
	,CAST(0 AS BOOLEAN) AS processed_flag
FROM (
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
)x;

SELECT * FROM _indicators_with_data


DO
$do$
DECLARE
 _counter int := 0;
 _loop_indicator_id INT = 1;
BEGIN
WHILE _counter <= (SELECT MAX(looper) from _indicators_with_data)
LOOP

   _loop_indicator_id = (SELECT indicator_id FROM _indicators_with_data WHERE looper = _counter);
  

   ALTER TABLE datapoint_abstracted
   ADD COLUMN 


   RAISE NOTICE 'The indicator_id is %', _loop_indicator_id;  -- coerced to text automatically
	

   _counter := _counter + 1;

END LOOP;
END
$do$




CREATE OR REPLACE FUNCTION alterscorecolumns()
  RETURNS void AS
$BODY$
BEGIN
  execute 'ALTER TABLE _indicators_with_data ADD total_score integer';
--  execute 'UPDATE hi_scores SET total_score = score1+score2+score3';
END
$BODY$
language plpgsql;

