DROP TABLE IF EXISTS agg_datapoint;
CREATE TABLE agg_datapoint
AS

SELECT
    d.id
    ,d.region_id
    ,d.campaign_id
    ,d.indicator_id
    ,value
    , CAST(0 AS BOOLEAN) AS is_agg
  FROM datapoint d

  UNION ALL

  SELECT
    -1 as id
    , r.parent_region_id
    , d.campaign_id
    , d.indicator_id
    , SUM(d.value) AS value
    , CAST(1 AS BOOLEAN) AS is_agg
  FROM datapoint d
  INNER JOIN region  r
  ON d.region_id = r.id
  AND NOT EXISTS (
    SELECT 1 FROM datapoint tid
    WHERE r.parent_region_id = tid.region_id
    AND d.campaign_id = tid.campaign_id
    AND tid.indicator_id = d.indicator_id
  )
  GROUP BY r.parent_region_id, d.campaign_id, d.indicator_id

  UNION ALL

  SELECT  -- NCO dashboard --
  -2 as id
  , r.id as region_id
    , x.campaign_id
    , x.indicator_id
    , x.value
    , CAST(1 AS BOOLEAN) AS is_agg
  FROM (
  SELECT
       cic.indicator_component_id as indicator_id
    , r.office_id
    , d.campaign_id
    , SUM(CASE WHEN value = 'NaN' then 0 else value end) as value
  FROM calculated_indicator_component cic
  INNER JOIN datapoint d
  ON cic.indicator_component_id = d.indicator_id
  INNER JOIN region r
  ON d.region_id = r.id
  WHERE cic.indicator_id in ( 274, 346 )
  GROUP BY r.office_id, d.campaign_id, cic.indicator_component_id
  )x
  INNER JOIN office o
  ON x.office_id = o.id
  INNER JOIN region r
  ON LOWER(o.name) = LOWER(r.name);



----
----

DROP TABLE IF EXISTS datapoint_with_computed;
CREATE TABLE datapoint_with_computed AS

SELECT
ID
,indicator_id
,region_id
,campaign_id
,value
,is_agg
,CAST(0 as BOOLEAN) as is_calc
FROM agg_datapoint;

-- make ID column auto increment
DROP SEQUENCE IF EXISTS dwc_seq;
CREATE SEQUENCE dwc_seq;
ALTER TABLE datapoint_with_computed ALTER COLUMN id SET DEFAULT nextval('dwc_seq');
ALTER TABLE datapoint_with_computed ALTER COLUMN id SET NOT NULL;
ALTER SEQUENCE dwc_seq OWNED BY datapoint_with_computed.id;

----- PART / WHOLE ------
INSERT INTO datapoint_with_computed
(indicator_id,region_id,campaign_id,value,is_calc)

SELECT
part.indicator_id as master_indicator_id
,d_part.region_id
,d_part.campaign_id
,d_part.value / NULLIF(d_whole.value,0) as value
,CAST(1 as BOOLEAN) as is_calc
FROM(
  SELECT max(id) as max_dp_id FROM datapoint_with_computed
) x
INNER JOIN calculated_indicator_component part
ON 1=1
INNER JOIN calculated_indicator_component whole
ON part.indicator_id = whole.indicator_id
AND whole.calculation = 'WHOLE'
AND part.calculation = 'PART'
INNER JOIN agg_datapoint d_part
ON part.indicator_component_id = d_part.indicator_id
INNER JOIN agg_datapoint d_whole
ON whole.indicator_component_id = d_whole.indicator_id
AND d_part.campaign_id = d_whole.campaign_id
AND d_part.region_id = d_whole.region_id;


----- SUM OF PARTS ------
INSERT INTO datapoint_with_computed
(indicator_id,region_id,campaign_id,value,is_calc)

SELECT
i_part.indicator_id
,region_id
,campaign_id
,SUM(ad.value) as value
,CAST(1 as BOOLEAN) as is_calc
FROM calculated_indicator_component i_part
INNER JOIN agg_datapoint ad
ON i_part.indicator_component_id = ad.indicator_id
WHERE i_part.calculation = 'PART_TO_BE_SUMMED'
GROUP BY i_part.indicator_id,region_id,campaign_id;

GRANT SELECT ON datapoint_with_computed TO djangoapp;

INSERT INTO datapoint_with_computed
(indicator_id,region_id,campaign_id,value,is_calc)
SELECT
x.indicator_id
,x.region_id
,x.campaign_id
,x.calc_value
,CAST(1 as BOOLEAN) as is_calc
FROM (
  SELECT
  part.to_calc_ind_id  as indicator_id
  ,part.region_id
  ,part.campaign_id
  ,(whole.value - part.value) / NULLIF(whole.value,0) as calc_value
  FROM (
    SELECT d.value, d.region_id, d.campaign_id, d.indicator_id, cic.calculation, cic.indicator_id as to_calc_ind_id
    FROM calculated_indicator_component cic
    INNER JOIN datapoint d
    ON cic.indicator_component_id = d.indicator_id
    WHERE calculation = 'PART_OF_DIFFERENCE'
  ) part
  INNER JOIN (
    SELECT d.value, d.region_id, d.campaign_id, d.indicator_id, cic.calculation, cic.indicator_id as to_calc_ind_id
    FROM calculated_indicator_component cic
    INNER JOIN datapoint d
    ON cic.indicator_component_id = d.indicator_id
    WHERE calculation = 'WHOLE_OF_DIFFERENCE'
  ) whole
  ON part.to_calc_ind_id = whole.to_calc_ind_id
  AND part.region_id = whole.region_id
  AND part.campaign_id = whole.campaign_id
)x
WHERE x.calc_value IS NOT NULL;
