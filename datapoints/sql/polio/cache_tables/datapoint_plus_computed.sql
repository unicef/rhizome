
DROP TABLE IF EXISTS datapoint_with_computed;
CREATE TABLE datapoint_with_computed AS

SELECT
ID
,indicator_id
,region_id
,campaign_id
,value
,CAST(0 as BOOLEAN) as is_calc
FROM datapoint;

-- make ID column auto increment
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
INNER JOIN datapoint d_part
ON part.indicator_component_id = d_part.indicator_id
INNER JOIN datapoint d_whole
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
,SUM(d.value) as value
,CAST(1 as BOOLEAN) as is_calc
FROM datapoint d
INNER JOIN calculated_indicator_component i_part
ON i_part.indicator_component_id = d.indicator_id
AND i_part.calculation = 'PART_TO_BE_SUMMED'
GROUP BY i_part.indicator_id,region_id,campaign_id;

GRANT SELECT ON datapoint_with_computed TO djangoapp;



SELECT
x.indicator_id
,x.region_id
,x.campaign_id
,x.value
,CAST(1 as BOOLEAN) as is_calc
FROM (
	SELECT
	part.to_calc_ind_id  as indicator_id
	,part.region_id
	,part.campaign_id
	,(whole.value - part.value) / NULLIF(whole.value,0) as value
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
