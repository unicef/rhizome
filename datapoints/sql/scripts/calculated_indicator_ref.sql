

DROP TABLE IF EXISTS _tmp_calc_indicators;
CREATE TABLE _tmp_calc_indicators AS

SELECT 
        REPLACE(REPLACE(master_indicator,'%','pct'),'#','number') as master_indicator
	,component_indicator
	,calculation
FROM (

SELECT   CAST(NULL AS VARCHAR) AS master_indicator
	,CAST(NULL AS VARCHAR) AS component_indicator
	,CAST(NULL AS VARCHAR) AS calculation

UNION ALL	


SELECT 'pct of FRR funded for the next 6 months','Amount FRR funds committed','part' UNION ALL
SELECT 'pct of FRR funded for the next 6 months','Amount total requested FRR funds','whole' UNION ALL
SELECT 'pct of UNICEF Polio Positions in place at National + State / Province level','Number of Unicef polio positions in their posts in PBR-approved structures','part' UNION ALL
SELECT 'pct of UNICEF Polio Positions in place at National + State / Province level','Target number of Unicef polio positions in PBR-approved structures','whole' UNION ALL
SELECT 'pct of High Risk districts which reported on balance of SIA vaccine stocks after last SIA round','Number of HRDs which reported on balance of SIA vaccine stocks after last SIA round','part' UNION ALL
SELECT 'pct of High Risk districts which reported on balance of SIA vaccine stocks after last SIA round','Number of high risk districts','whole' UNION ALL
SELECT 'number of established LT vaccination transit points vs. total number identified by the programme','Number of established LT vaccination transit points','part' UNION ALL
SELECT 'number of established LT vaccination transit points vs. total number identified by the programme','Total number of LT vaccination transit points planned by the programme','whole' UNION ALL
SELECT 'number of established LT vaccination transit points with a dedicated social mobilizer, vs. total number identified by the programme','Number of established LT vaccination transit points with a dedicated social mobilizer','part' UNION ALL
SELECT 'number of established LT vaccination transit points with a dedicated social mobilizer, vs. total number identified by the programme','Total number of LT vaccination transit points planned by the programme','whole' UNION ALL
SELECT 'number and pct of targeted social mobilizers and supervisors in place','Number of social mobilizers and supervisors in place','part' UNION ALL
SELECT 'number and pct of targeted social mobilizers and supervisors in place','Target number of social mobilizers and supervisors','whole' UNION ALL
SELECT 'pct of vaccination teams in which at least one member is from the local community in HR areas','Number of vaccination teams with at least 1 member from the local community','part' UNION ALL
SELECT 'pct of vaccination teams in which at least one member is from the local community in HR areas','Number of vaccination teams','whole' UNION ALL
SELECT 'pct of vaccination teams in which at least one member is female in HR areas','Number of vaccination teams with at least one female','part' UNION ALL
SELECT 'pct of vaccination teams in which at least one member is female in HR areas','Number of vaccination teams','whole' UNION ALL
SELECT 'pct of female social mobilisers among social mobilizers in place','Number of female social mobilizers','part' UNION ALL
SELECT 'pct of female social mobilisers among social mobilizers in place','Number of social mobilizers in place','whole' UNION ALL
SELECT 'pct of vaccinators and SM''s operating in HRD who have been trained on professional Inter Personal Communication package provided by UNICEF in the last 6 months','Number of vaccinators and SMs operating in HRDs trained on professional IPC package in last 6 months','part' UNION ALL
SELECT 'pct of vaccinators and SM''s operating in HRD who have been trained on professional Inter Personal Communication package provided by UNICEF in the last 6 months','Number of vaccinators and social mobilizers','whole' UNION ALL
SELECT 'pct of social mobilizers trained or refreshed with the integrated health package in the last 6 months','Number of social mobilizers trained or refreshed with the integrated health package in the last 6 months','part' UNION ALL
SELECT 'pct of social mobilizers trained or refreshed with the integrated health package in the last 6 months','Number of social mobilizers in place','whole' UNION ALL
SELECT 'pct of Social Mobilizers who received on-the-job supervision during their last working week','Number of social mobilizers who received on-the-job supervision during their last working week','part' UNION ALL
SELECT 'pct of Social Mobilizers who received on-the-job supervision during their last working week','Number of social mobilizers in place','whole' UNION ALL
SELECT 'pct of social mobilizers who received timely payment for last campaign/month''s salary among ALL social mobilisers involved in the campaign.','Number of social mobilizers receiving timely payment for last campaign','part' UNION ALL
SELECT 'pct of social mobilizers who received timely payment for last campaign/month''s salary among ALL social mobilisers involved in the campaign.','Number of social mobilizers in place','whole' UNION ALL
SELECT 'In accessible parts of High Risk Districts, pct of children missed due to refusal among all targeted children','Number of children missed due to refusal','part' UNION ALL
SELECT 'In accessible parts of High Risk Districts, pct of children missed due to refusal among all targeted children','Number of children targeted in high-risk districts','whole' UNION ALL
SELECT 'In accessible parts of High Risk Districts, proportion of children missed due to absences among all targeted children','Number of children missed due to absences','part' UNION ALL
SELECT 'In accessible parts of High Risk Districts, proportion of children missed due to absences among all targeted children','Number of children targeted in high-risk districts','whole' UNION ALL
SELECT 'pct of caregivers in HRDs who know number of times they need to visit the RI site for routine immunization before a child reaches 1 year of age','Number of caregivers in HRD who know times needed to visit RI site before 1 yo','part' UNION ALL
SELECT 'pct of caregivers in HRDs who know number of times they need to visit the RI site for routine immunization before a child reaches 1 year of age','Number of caregivers in high risk districts','whole' UNION ALL
SELECT 'number and pct of RI sessions monitored having stockouts of any vaccine during last month','Number of RI sessions monitored having stockouts of any vaccine in the last month','part' UNION ALL
SELECT 'number and pct of RI sessions monitored having stockouts of any vaccine during last month','Number of RI sessions monitored','whole' UNION ALL
SELECT 'pct of HR Districts with locations where OPV is delivered together with any other polio-funded services demanded by the community (health, protection, education, other). With access breakdown.','Number of high risk districts with locations where OPV is delivered together with any other polio-funded services demanded by community','part' UNION ALL
SELECT 'pct of HR Districts with locations where OPV is delivered together with any other polio-funded services demanded by the community (health, protection, education, other). With access breakdown.','Number of high risk districts','whole'

)x
WHERE master_indicator IS NOT NULL;


INSERT INTO indicator
(name,short_name,description,is_reported,slug,source_id,created_at)
SELECT DISTINCT
	master_indicator
	,master_indicator
	,master_indicator
	,CAST(0 as BOOLEAN)
	,LOWER(REPLACE(master_indicator,' ','-'))
	,1
	,now()
FROM _tmp_calc_indicators tc
WHERE NOT EXISTS
(
SELECT 1 FROM indicator i
WHERE i.name = tc.master_indicator
);

INSERT INTO calculated_indicator_component
(indicator_id,indicator_component_id,calculation,created_at)

SELECT   mst_i.id
	,comp_i.id
	,UPPER(ti.calculation)
	,now()
FROM _tmp_calc_indicators ti
JOIN indicator mst_i
ON ti.master_indicator = mst_i.description
INNER JOIN indicator comp_i
ON ti.component_indicator = comp_i.description
WHERE NOT EXISTS (
	SELECT 1 from calculated_indicator_component clc
	WHERE mst_i.id = clc.indicator_id
	and comp_i.id = clc.indicator_component_id
);

--select * from indicator where name = 'Number of children missed due to absences'



