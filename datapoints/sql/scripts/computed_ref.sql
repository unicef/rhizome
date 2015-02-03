

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
SELECT 'pct of HR Districts with locations where OPV is delivered together with any other polio-funded services demanded by the community (health, protection, education, other). With access breakdown.','Number of high risk districts','whole' UNION ALL

---- 2.1.2015 ----

SELECT '% of FRR funded for the next 6 months','Amount FRR funds committed','part' UNION ALL
SELECT '% of FRR funded for the next 6 months','Amount total requested FRR funds','whole' UNION ALL
SELECT '% of UNICEF Polio Positions in place at National + State / Province level','Number of Unicef polio positions in their posts in PBR-approved structures','part' UNION ALL
SELECT '% of UNICEF Polio Positions in place at National + State / Province level','Target number of Unicef polio positions in PBR-approved structures','whole' UNION ALL
SELECT '% of High Risk districts which reported on balance of SIA vaccine stocks after last SIA round','Number of HRDs which reported on balance of SIA vaccine stocks after last SIA round','part' UNION ALL
SELECT '% of High Risk districts which reported on balance of SIA vaccine stocks after last SIA round','Number of high risk districts','whole' UNION ALL
SELECT '# of established LT vaccination transit points vs. total # identified by the programme','Number of established LT vaccination transit points','part' UNION ALL
SELECT '# of established LT vaccination transit points vs. total # identified by the programme','Total number of LT vaccination transit points planned by the programme','whole' UNION ALL
SELECT '# of established LT vaccination transit points with a dedicated social mobilizer, vs. total # identified by the programme','Number of established LT vaccination transit points with a dedicated social mobilizer','part' UNION ALL
SELECT '# of established LT vaccination transit points with a dedicated social mobilizer, vs. total # identified by the programme','Total number of LT vaccination transit points planned by the programme','whole' UNION ALL
SELECT '# and % of targeted social mobilizers and supervisors in place','Number of social mobilizers and supervisors in place','part' UNION ALL
SELECT '# and % of targeted social mobilizers and supervisors in place','Target number of social mobilizers and supervisors','whole' UNION ALL
SELECT '% of vaccination teams in which at least one member is from the local community in HR areas','Number of vaccination teams with at least 1 member from the local community','part' UNION ALL
SELECT '% of vaccination teams in which at least one member is from the local community in HR areas','Number of vaccination teams','whole' UNION ALL
SELECT '% of vaccination teams in which at least one member is female in HR areas','Number of vaccination teams with at least one female','part' UNION ALL
SELECT '% of vaccination teams in which at least one member is female in HR areas','Number of vaccination teams','whole' UNION ALL
SELECT '% of female social mobilisers among social mobilizers in place','Number of female social mobilizers','part' UNION ALL
SELECT '% of female social mobilisers among social mobilizers in place','Number of social mobilizers in place','whole' UNION ALL
SELECT '% of vaccinators and SM''s operating in HRD who have been trained on professional Inter Personal Communication package provided by UNICEF in the last 6 months','Number of vaccinators and SMs operating in HRDs trained on professional IPC package in last 6 months','part' UNION ALL
SELECT '% of vaccinators and SM''s operating in HRD who have been trained on professional Inter Personal Communication package provided by UNICEF in the last 6 months','Number of vaccinators and social mobilizers','whole' UNION ALL
SELECT '% of social mobilizers trained or refreshed with the integrated health package in the last 6 months','Number of social mobilizers trained or refreshed with the integrated health package in the last 6 months','part' UNION ALL
SELECT '% of social mobilizers trained or refreshed with the integrated health package in the last 6 months','Number of social mobilizers in place','whole' UNION ALL
SELECT '% of Social Mobilizers who received on-the-job supervision during their last working week','Number of social mobilizers who received on-the-job supervision during their last working week','part' UNION ALL
SELECT '% of Social Mobilizers who received on-the-job supervision during their last working week','Number of social mobilizers in place','whole' UNION ALL
SELECT '% of social mobilizers who received timely payment for last campaign/month''s salary among ALL social mobilisers involved in the campaign.','Number of social mobilizers receiving timely payment for last campaign','part' UNION ALL
SELECT '% of social mobilizers who received timely payment for last campaign/month''s salary among ALL social mobilisers involved in the campaign.','Number of social mobilizers in place','whole' UNION ALL
SELECT 'In accessible parts of High Risk Districts, % of children missed due to refusal among all targeted children','Number of children missed due to refusal','part' UNION ALL
SELECT 'In accessible parts of High Risk Districts, % of children missed due to refusal among all targeted children','Number of children targeted in high-risk districts','whole' UNION ALL
SELECT 'In accessible parts of High Risk Districts, proportion of children missed due to absences among all targeted children','Number of children missed due to absences','part' UNION ALL
SELECT 'In accessible parts of High Risk Districts, proportion of children missed due to absences among all targeted children','Number of children targeted in high-risk districts','whole' UNION ALL
SELECT '% of caregivers in HRDs who know number of times they need to visit the RI site for routine immunization before a child reaches 1 year of age','Number of caregivers in HRD who know times needed to visit RI site before 1 yo','part' UNION ALL
SELECT '% of caregivers in HRDs who know number of times they need to visit the RI site for routine immunization before a child reaches 1 year of age','Number of caregivers in high risk districts','whole' UNION ALL
SELECT '# and % of RI sessions monitored having stockouts of any vaccine during last month','Number of RI sessions monitored having stockouts of any vaccine in the last month','part' UNION ALL
SELECT '# and % of RI sessions monitored having stockouts of any vaccine during last month','Number of RI sessions monitored','whole' UNION ALL
SELECT '% of HR Districts with locations where OPV is delivered together with any other polio-funded services demanded by the community (health, protection, education, other). With access breakdown.','Number of high risk districts with locations where OPV is delivered together with any other polio-funded services demanded by community','part' UNION ALL
SELECT '% of HR Districts with locations where OPV is delivered together with any other polio-funded services demanded by the community (health, protection, education, other). With access breakdown.','Number of high risk districts','whole' UNION ALL
SELECT 'Endprocess_Percent missed children','Endprocess_Missed children - All reasons','part' UNION ALL
SELECT 'Endprocess_Percent missed children','Endprocess_Number of children seen','whole' UNION ALL
SELECT 'Outside_Percent missed children','Outside_Total Not Marked','part' UNION ALL
SELECT 'Outside_Percent missed children','Outside_Total seen','whole' UNION ALL
SELECT 'Endprocess_Percent vaccination influencer is personal decision','Endprocess_Influence1 - Personal decision','part' UNION ALL
SELECT 'Endprocess_Percent vaccination influencer is personal decision','Endprocess_All vaccination influencers','whole' UNION ALL
SELECT 'Endprocess_Percent vaccination influencer is radio','Endprocess_Influence5 - Radio','part' UNION ALL
SELECT 'Endprocess_Percent vaccination influencer is radio','Endprocess_All vaccination influencers','whole' UNION ALL
SELECT 'Endprocess_Percent vaccination influencer is husband','Endprocess_Influence2 - Husband','part' UNION ALL
SELECT 'Endprocess_Percent vaccination influencer is husband','Endprocess_All vaccination influencers','whole' UNION ALL
SELECT 'Endprocess_Percent vaccination influencer is neighbour','Endprocess_Influence6 - Neighbour','part' UNION ALL
SELECT 'Endprocess_Percent vaccination influencer is neighbour','Endprocess_All vaccination influencers','whole' UNION ALL
SELECT 'Endprocess_Percent vaccination influencer is traditional leader','Endprocess_Influence3 - Traditional leader','part' UNION ALL
SELECT 'Endprocess_Percent vaccination influencer is traditional leader','Endprocess_All vaccination influencers','whole' UNION ALL
SELECT 'Endprocess_Pct vaccination influencer is community mobiliser','Endprocess_Influence7 - Community mobiliser','part' UNION ALL
SELECT 'Endprocess_Pct vaccination influencer is community mobiliser','Endprocess_All vaccination influencers','whole' UNION ALL
SELECT 'Endprocess_Percent vaccination influencer is religious leader','Endprocess_Influence4 - Religious leader','part' UNION ALL
SELECT 'Endprocess_Percent vaccination influencer is religious leader','Endprocess_All vaccination influencers','whole' UNION ALL
SELECT 'Endprocess_Percent vaccination influencer is vaccinator','Endprocess_Influence8 - Vaccinator','part' UNION ALL
SELECT 'Endprocess_Percent vaccination influencer is vaccinator','Endprocess_All vaccination influencers','whole' UNION ALL
SELECT 'Endprocess_Percent source of info is town announcer','Endprocess_Source of info on IPDs - Town announcer','part' UNION ALL
SELECT 'Endprocess_Percent source of info is town announcer','Endprocess_All sources of info on IPDs','whole' UNION ALL
SELECT 'Endprocess_Percent source of info is mosque announcement','Endprocess_Source of info on IPDs - Mosque announcement','part' UNION ALL
SELECT 'Endprocess_Percent source of info is mosque announcement','Endprocess_All sources of info on IPDs','whole' UNION ALL
SELECT 'Endprocess_Percent source of info is relative','Endprocess_Source of info on IPDs - Relative','part' UNION ALL
SELECT 'Endprocess_Percent source of info is relative','Endprocess_All sources of info on IPDs','whole' UNION ALL
SELECT 'Endprocess_Percent source of info is radio','Endprocess_Source of info on IPDs - Radio','part' UNION ALL
SELECT 'Endprocess_Percent source of info is radio','Endprocess_All sources of info on IPDs','whole' UNION ALL
SELECT 'Endprocess_Percent source of info is newspaper','Endprocess_Source of info on IPDs - Newspaper','part' UNION ALL
SELECT 'Endprocess_Percent source of info is newspaper','Endprocess_All sources of info on IPDs','whole' UNION ALL
SELECT 'Endprocess_Percent source of info is health worker','Endprocess_Source of info on IPDs - Health worker','part' UNION ALL
SELECT 'Endprocess_Percent source of info is health worker','Endprocess_All sources of info on IPDs','whole' UNION ALL
SELECT 'Endprocess_Percent source of info is traditional leader','Endprocess_Source of info on IPDs - Traditional leader','part' UNION ALL
SELECT 'Endprocess_Percent source of info is traditional leader','Endprocess_All sources of info on IPDs','whole' UNION ALL
SELECT 'Endprocess_Percent source of info is poster','Endprocess_Source of info on IPDs - Poster','part' UNION ALL
SELECT 'Endprocess_Percent source of info is poster','Endprocess_All sources of info on IPDs','whole' UNION ALL
SELECT 'Endprocess_Percent source of info is community mobiliser','Endprocess_Source of info on IPDs - Community mobiliser','part' UNION ALL
SELECT 'Endprocess_Percent source of info is community mobiliser','Endprocess_All sources of info on IPDs','whole' UNION ALL
SELECT 'Endprocess_Percent source of info is religious leader','Endprocess_Source of info on IPDs - Religious leader','part' UNION ALL
SELECT 'Endprocess_Percent source of info is religious leader','Endprocess_All sources of info on IPDs','whole' UNION ALL
SELECT 'Endprocess_Percent source of info is banner','Endprocess_Source of info on IPDs - Banner','part' UNION ALL
SELECT 'Endprocess_Percent source of info is banner','Endprocess_All sources of info on IPDs','whole' UNION ALL
SELECT 'Endprocess_Percent missed children due to HH not in plan','Endprocess_NOimmReas1 - Household not in microplan','part' UNION ALL
SELECT 'Endprocess_Percent missed children due to HH not in plan','Endprocess_Missed children - All reasons','whole' UNION ALL
SELECT 'Endprocess_Pct missed children due to HH in plan but not visited','Endprocess_NOimmReas2 - Household in microplan but not visited','part' UNION ALL
SELECT 'Endprocess_Pct missed children due to HH in plan but not visited','Endprocess_Missed children - All reasons','whole' UNION ALL
SELECT 'Endprocess_Pct missed children due to child absent','Endprocess_Reason for missed children - child absent','part' UNION ALL
SELECT 'Endprocess_Pct missed children due to child absent','Endprocess_Missed children - All reasons','whole' UNION ALL
SELECT 'Endprocess_Pct missed children due to non compliance','Endprocess_Reason for missed children - Non compliance','part' UNION ALL
SELECT 'Endprocess_Pct missed children due to non compliance','Endprocess_Missed children - All reasons','whole' UNION ALL
SELECT 'Endprocess_Pct missed children due to security','Endprocess_NOimmReas20 - Security','part' UNION ALL
SELECT 'Endprocess_Pct missed children due to security','Endprocess_Missed children - All reasons','whole' UNION ALL
SELECT 'Endprocess_Pct of children absent due to playground','Endprocess_NOimmReas3 - Child at playground','part' UNION ALL
SELECT 'Endprocess_Pct of children absent due to playground','Endprocess_Reason for missed children - child absent','whole' UNION ALL
SELECT 'Endprocess_Pct of children absent due to child at social event','Endprocess_NoimmReas4 - Child at social event','part' UNION ALL
SELECT 'Endprocess_Pct of children absent due to child at social event','Endprocess_Reason for missed children - child absent','whole' UNION ALL
SELECT 'Endprocess_Pct of children absent due to child at market','Endprocess_NOimmReas5 - Child at market','part' UNION ALL
SELECT 'Endprocess_Pct of children absent due to child at market','Endprocess_Reason for missed children - child absent','whole' UNION ALL
SELECT 'Endprocess_Pct of children absent due to child at farm','Endprocess_NOimmReas6 - Child at farm','part' UNION ALL
SELECT 'Endprocess_Pct of children absent due to child at farm','Endprocess_Reason for missed children - child absent','whole' UNION ALL
SELECT 'Endprocess_Pct of children absent due to child at school','Endprocess_NOimmReas7 - Child at school','part' UNION ALL
SELECT 'Endprocess_Pct of children absent due to child at school','Endprocess_Reason for missed children - child absent','whole' UNION ALL
SELECT 'Endprocess_Pct of non compliance due to child sick','Endprocess_NOimmReas8 - Child sick','part' UNION ALL
SELECT 'Endprocess_Pct of non compliance due to child sick','Endprocess_Reason for missed children - Non compliance','whole' UNION ALL
SELECT 'Endprocess_Pct of non compliance due to polio is rare','Endprocess_NOimmReas11 - Polio is rare','part' UNION ALL
SELECT 'Endprocess_Pct of non compliance due to polio is rare','Endprocess_Reason for missed children - Non compliance','whole' UNION ALL
SELECT 'Endprocess_Pct of non compliance due to religious belief','Endprocess_NOimmReas14 - Religious belief','part' UNION ALL
SELECT 'Endprocess_Pct of non compliance due to religious belief','Endprocess_Reason for missed children - Non compliance','whole' UNION ALL
SELECT 'Endprocess_Pct of non compliance due to no pluses given','Endprocess_NOimmReas17 - No pluses given','part' UNION ALL
SELECT 'Endprocess_Pct of non compliance due to no pluses given','Endprocess_Reason for missed children - Non compliance','whole' UNION ALL
SELECT 'Endprocess_Pct of non compliance due to too many rounds','Endprocess_NOimmReas9 - Too many rounds','part' UNION ALL
SELECT 'Endprocess_Pct of non compliance due to too many rounds','Endprocess_Reason for missed children - Non compliance','whole' UNION ALL
SELECT 'Endprocess_Pct of non compliance due to polio has cure','Endprocess_NOimmReas12 - Polio has cure','part' UNION ALL
SELECT 'Endprocess_Pct of non compliance due to polio has cure','Endprocess_Reason for missed children - Non compliance','whole' UNION ALL
SELECT 'Endprocess_Pct of non compliance due to political differences','Endprocess_NOimmReas15 - Political differences','part' UNION ALL
SELECT 'Endprocess_Pct of non compliance due to political differences','Endprocess_Reason for missed children - Non compliance','whole' UNION ALL
SELECT 'Endprocess_Pct of non compliance due to fear of OPV side effects','Endprocess_NOimmReas10 - Fear of OPV side effects','part' UNION ALL
SELECT 'Endprocess_Pct of non compliance due to fear of OPV side effects','Endprocess_Reason for missed children - Non compliance','whole' UNION ALL
SELECT 'Endprocess_Pct of non compliance due to other remedies available','Endprocess_NOimmReas13 - There are other remedies available','part' UNION ALL
SELECT 'Endprocess_Pct of non compliance due to other remedies available','Endprocess_Reason for missed children - Non compliance','whole' UNION ALL
SELECT 'Endprocess_Pct of non compliance due to unhappy with team','Endprocess_NOimmReas16 - Unhappy with vaccination team','part' UNION ALL
SELECT 'Endprocess_Pct of non compliance due to unhappy with team','Endprocess_Reason for missed children - Non compliance','whole' UNION ALL
SELECT 'Endprocess_Pct of non compliance due to no caregiver consent','Endprocess_NOimmReas19 - No caregiver consent','part' UNION ALL
SELECT 'Endprocess_Pct of non compliance due to no caregiver consent','Endprocess_Reason for missed children - Non compliance','whole' UNION ALL
SELECT 'Endprocess_Pct of non compliance due to no felt need','Endprocess_NOimmReas18 - No felt need','part' UNION ALL
SELECT 'Endprocess_Pct of non compliance due to no felt need','Endprocess_Reason for missed children - Non compliance','whole' UNION ALL
SELECT 'Redo_Percent non compliance resolved by traditional leader','Redo_Non compliance resolved by traditional leader','part' UNION ALL
SELECT 'Redo_Percent non compliance resolved by traditional leader','Redo_Number of children 0 to 59 months missed in HH due to non compliance','whole' UNION ALL
SELECT 'Redo_Percent non compliance resolved by community leader','Redo_Non compliance resolved by community leader','part' UNION ALL
SELECT 'Redo_Percent non compliance resolved by community leader','Redo_Number of children 0 to 59 months missed in HH due to non compliance','whole' UNION ALL
SELECT 'Redo_Percent non compliance resolved by religious leader','Redo_Percent non compliance resolved by religious leader','part' UNION ALL
SELECT 'Redo_Percent non compliance resolved by religious leader','Redo_Number of children 0 to 59 months missed in HH due to non compliance','whole' UNION ALL
SELECT 'Redo_Percent non compliance resolved by other','Redo_Non compliance resolved by other','part' UNION ALL
SELECT 'Redo_Percent non compliance resolved by other','Redo_Number of children 0 to 59 months missed in HH due to non compliance','whole'

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
