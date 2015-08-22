# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('datapoints', '0003_load_ng_regions'),
    ]

    operations = [
    migrations.RunSQL("""

    INSERT INTO auth_group
    (name)
    SELECT 'can_edit_all_indicators';

    INSERT INTO auth_user_groups
    (user_id,group_id)
    SELECT au.id,ag.id FROM auth_user au
    INNER JOIN auth_group ag
    ON ag.name = 'can_edit_all_indicators';

	INSERT INTO indicator_permission
	(group_id, indicator_id)
	SELECT ag.id, i.id FROM indicator i
	INNER JOIN auth_group ag
	ON ag.name = 'can_edit_all_indicators';

	INSERT INTO region_permission
	(read_write, region_id, user_id)
	SELECT 'r', r.id, au.id
	FROM region r
	INNER JOIN auth_user au
	ON 1=1;
	INSERT INTO region_permission
	(read_write, region_id, user_id)
	SELECT 'w' , region_id, user_id FROM region_permission;


    INSERT INTO indicator
        (id, name, description, short_name, slug, is_reported, created_at)
        SELECT
        	indicator_id, name, description, short_name, CAST(indicator_id as VARCHAR), CAST(0 AS BOOLEAN), now()
        FROM (
        SELECT 461 as indicator_id,'# of established LT vaccination transit points vs. total # identified by the programme' as name,'# of established LT vaccination transit points vs. total # identified by the programme' as description,'# of established LT vaccination transit points vs. total # identified by the programme' as short_name UNION ALL
        SELECT 462,'Number of regions sampled','The total number of regions sampled.','# regions sampled' UNION ALL
        SELECT 41,'Number of vaccinators','Number of vaccinators','Number of vaccinators' UNION ALL
        SELECT 159,'Number of aVDPV2 cases','Number of aVDPV2 cases','Number of aVDPV2 cases' UNION ALL
        SELECT 162,'Number of iVDPV cases','Number of iVDPV cases','Number of iVDPV cases' UNION ALL
        SELECT 32,'Number of Unicef polio positions in their posts in PBR-approved structures','Number of Unicef polio positions in their posts in PBR-approved structures','Number of Unicef polio positions in their posts in PBR' UNION ALL
        SELECT 31,'Target number of Unicef polio positions in PBR-approved structures','Target number of Unicef polio positions in PBR-approved structures','Target number of Unicef polio positions in PBR-approv' UNION ALL
        SELECT 21,'Number of all missed children','Number of all missed children','All missed children' UNION ALL
        SELECT 24,'Number of children missed due to other reasons','Number of children missed due to other reasons','Missed due to other reasons' UNION ALL
        SELECT 25,'Number of refusals before re-visit','Number of refusals before re-visit','Refusals before re-visit' UNION ALL
        SELECT 26,'Number of refusals after re-visit','Number of refusals after re-visit','Refusals after re-visit' UNION ALL
        SELECT 27,'Number of microplans in high risk districts','Number of microplans in high risk districts','Microplans in High Risk Disrict' UNION ALL
        SELECT 30,'Number of caregivers aware of polio campaigns','Number of caregivers aware of polio campaigns','Number of caregivers aware' UNION ALL
        SELECT 28,'Number of microplans in high risk districts incorporating social data','Number of microplans in high risk districts Incorporating social data','Microplans incorporating social data' UNION ALL
        SELECT 35,'Number of target social mobilizers','Number of target social mobilizers','Number of target social mobilizers' UNION ALL
        SELECT 40,'Number of female social mobilizers','Number of female social mobilizers','Number of female social mobilizers' UNION ALL
        SELECT 45,'FRR updated quarterly','FRR updated quarterly','FRR updated quarterly' UNION ALL
        SELECT 46,'Number of social mobilizers receiving timely payment for last campaign','Number of social mobilizers receiving timely payment for last campaign','Number of social mobilizers receiving timely payment' UNION ALL
        SELECT 34,'Number of high risk sub-districts covered by at least 1 social mobilizer','Number of high risk sub-districts covered by at least 1 social mobilizer','Number of high risk sub-districts w social mobilizers' UNION ALL
        SELECT 43,'Amount total requested FRR funds','Amount total requested FRR funds','Amount total requested FRR funds' UNION ALL
        SELECT 38,'Number of vaccination teams','Number of vaccination teams','Number of vaccination teams' UNION ALL
        SELECT 36,'Number of social mobilizers in place','Number of social mobilizers in place','Number of social mobilizers in place' UNION ALL
        SELECT 29,'Number of caregivers in high risk districts','Number of caregivers in high risk districts','Number of caregivers in high risk districts' UNION ALL
        SELECT 44,'Amount FRR funds committed','Amount FRR funds committed ','Amount FRR funds committed ' UNION ALL
        SELECT 49,'Number of social mobilizers trained on RI in past 6 mo','Number of social mobilizers trained on RI in past 6 mo','Number of social mobilizers trained on RI in past 6 mo' UNION ALL
        SELECT 93,'ODK - Census  Newborns Female','censusnewbornsf','ODK - Census  Newborns Female' UNION ALL
        SELECT 112,'ODK - group_msd_chd_msd_poldiffsf','group_msd_chd_msd_poldiffsf','ODK - group_msd_chd_msd_poldiffsf' UNION ALL
        SELECT 42,'Number of vaccinators operating in HRDs trained on professional IPC package in last 6 months','Number of vaccinators operating in HRDs trained on professional IPC package in last 6 months','# vaccinators in HRDs trained on IPC in last 6 mo' UNION ALL
        SELECT 1,'Polio Cases YTDYYYY','Polio Cases YTDYYYY','Polio Cases YTDYYYY' UNION ALL
        SELECT 53,'Number of districts having NO stockouts of OPV','Number of districts having NO stockouts of OPV','Number of districts having NO stockouts of OPV' UNION ALL
        SELECT 463,'number of social mobilisers participating the telephone survey','number of social mobilisers participating the telephone survey','number of social mobilisers participating the telephone survey' UNION ALL
        SELECT 56,'Number of sub-regional units','Number of sub-regional units','Number of sub-regional units' UNION ALL
        SELECT 57,'Number of sub-regional units where OPV arrived in sufficient time','Number of sub-regional units where OPV arrived in sufficient time','Number of sub-regional units where OPV arrived in time' UNION ALL
        SELECT 70,'Number of WPV1 cases','Number of WPV1 cases','Number of WPV1 cases' UNION ALL
        SELECT 62,'Number of health facilities w/ capacity','Number of health facilities w/ capacity','Number of health facilities w/ capacity' UNION ALL
        SELECT 66,'Number of health facilities having NO stock-outs of OPV','Number of health facilities having NO stock-outs of OPV','Number of health facilities having NO stock-outs of OPV' UNION ALL
        SELECT 176,'Number of established LT vaccination transit points with a dedicated social mobilizer','Number of established LT vaccination transit points with a dedicated social mobilizer','LT Transit Points with SM' UNION ALL
        SELECT 67,'Percentage of States/Regions with OPV supply arriving at state/region level in sufficient time before campaign','Percentage of States/Regions with OPV supply arriving at state/region level in sufficient time before campaign','Percentage of States/Regions with OPV supply arriving a' UNION ALL
        SELECT 470,'Number of children missed due to all access issues (TEMP)','TEMPORARY INDICATOR','Inaccessible Children (TEMP)' UNION ALL
        SELECT 69,'Number of cVDPV2 cases','Number of cVDPV2 cases','Number of cVDPV2 cases' UNION ALL
        SELECT 160,'Number of WPV3 cases','Number of WPV3 cases','Number of WPV3 cases' UNION ALL
        SELECT 161,'Number of WPV1WPV3 cases','Number of WPV1WPV3 cases','Number of WPV1WPV3 cases' UNION ALL
        SELECT 51,'Number of children vaccinated in HRD','Number of children vaccinated in HRD','Number of children vaccinated in HRD' UNION ALL
        SELECT 177,'Number of children vaccinated at transit points last month','Number of children vaccinated at transit points last month','# of children vaccinated at transit points last month' UNION ALL
        SELECT 167,'% missed children due to team did not visit','% missed children due to team did not visit','Not visited' UNION ALL
        SELECT 165,'% missed children due to other reasons','% missed children due to other reasons','Other reasons' UNION ALL
        SELECT 166,'% missed children due to refusal','% missed children due to refusal','Refused' UNION ALL
        SELECT 164,'% missed children due to child not available','% missed children due to child not available','Child absent' UNION ALL
        SELECT 175,'Number of established LT vaccination transit points','Number of established LT vaccination transit points ','LT Transit Points' UNION ALL
        SELECT 95,'ODK - spec_grp_choice','spec_grp_choice','ODK - spec_grp_choice' UNION ALL
        SELECT 169,'FRR Funding Level','Percent of FRR funded for the next 6 months','Funding' UNION ALL
        SELECT 192,'Routine Immunization Defaulter Tracking','Number of routine immunization defaulters tracked and mobilized by SMs last month','RI Defaulter Tracking' UNION ALL
        SELECT 179,'Social Mobilisers and Their Supervisors in Place','Proportion of target social mobilisers and their supervisors in place','Mobilisers in Place' UNION ALL
        SELECT 172,'District OPV Stock Balance Reporting','Percent of high risk districts which reported on balance of SIA vaccine stock after last SIA round','Stock Balance Reporting' UNION ALL
        SELECT 196,'HR district did NOT receive polio vaccine supply at least 3 days before the planned start date of campaign (1 = yes, 0 = no)','HR district did NOT receive polio vaccine supply at least 3 days before the planned start date of campaign (1 = yes, 0 = no)','HRD did NOT receive OPV supply at least 3d before campa' UNION ALL
        SELECT 199,'Total number of all active cold chain equipment in district','Total number of all active cold chain equipment in district','Total # of all active cold chain equipment in district' UNION ALL
        SELECT 206,'Number of social mobilizers and supervisors in place','Number of social mobilizers and supervisors in place','# of SMs and supervisors in place' UNION ALL
        SELECT 37,'Number of vaccination teams with at least one female','Number of vaccination teams with at least one female','Number of vaccination teams with at least one female' UNION ALL
        SELECT 210,'Number of social mobilizers who received on-the-job supervision during their last working week','Number of social mobilizers who received on-the-job supervision during their last working week','# of SMs who received supervision last work week' UNION ALL
        SELECT 211,'Number of refusals resolved','Number of refusals resolved','Number of refusals resolved' UNION ALL
        SELECT 197,'District reported on balance of SIA vaccine stocks after last SIA round? (1=yes, 0=no)','District reported on balance of SIA vaccine stocks after last SIA round? (1=yes, 0=no)','On balance of SIA vaccine stocks' UNION ALL
        SELECT 213,'Number of absences before re-visit','Number of absences before re-visit','# of absences before re-visit' UNION ALL
        SELECT 214,'Number of absences after re-visit','Number of absences after re-visit','# of absences after re-visit' UNION ALL
        SELECT 216,'Number of RI sessions monitored having stockouts of any vaccine in the last month','Number of RI sessions monitored having stockouts of any vaccine in the last month','# of RI sessions monitored having stockouts of any vacc' UNION ALL
        SELECT 217,'Number of RI sessions monitored','Number of RI sessions monitored','Number of RI sessions monitored' UNION ALL
        SELECT 218,'Number of high risk districts with locations where OPV is delivered together with any other polio-funded services demanded by community','Number of high risk districts with locations where OPV is delivered together with any other polio-funded services demanded by community','# HRDs with locations where OPV is delivered w services' UNION ALL
        SELECT 174,'Proportion of access-challenged districts that have had a specific access approach identified','Proportion of access-challenged districts that have had a specific access approach identified','% of access-challenged districts with access approach' UNION ALL
        SELECT 189,'Percent of absences resolved during the previous month (both during campaigns and between rounds)','Percent of absences resolved during the previous month (both during campaigns and between rounds)','Absences Conversion' UNION ALL
        SELECT 134,'ODK - group_spec_events_spec_mslscase','group_spec_events_spec_mslscase','ODK - group_spec_events_spec_mslscase' UNION ALL
        SELECT 202,'Is an access-challenged district that has a specific access approach identified (1=yes, 0=no)','Is an access-challenged district that has a specific access approach identified (1=yes, 0=no)','Is an access-challenged district w access approach' UNION ALL
        SELECT 203,'Is an access-challenged district (1=yes, 0=no)','Is an access-challenged district (1=yes, 0=no)','Is an access-challenged districts' UNION ALL
        SELECT 472,'Is a high risk district where at least 90% of active cold chain equipment are functional (1=yes, 0=no)','Is a high risk district where at least 90% of active cold chain equipment are functional (1=yes, 0=no)','HRD with 90% functional cold chain' UNION ALL
        SELECT 219,'OPV Wastage between 5% and 15%','Proportion of high risk districts where polio vaccine wastage rate in SIAs is between 5 and 15%, calculated from the number of children vaccinated and the number of vaccines used, as recorded in vaccinator tally sheet','Acceptable OPV Wastage' UNION ALL
        SELECT 193,'OPV Delivery with Other Polio-Funded Services','Percent of HRDs where OPV is delivered together with any other polio-funded services demanded by the community','Polio-Plus Activities' UNION ALL
        SELECT 475,'Missed Children','Proportion of children missed among all target children, according to independent monitoring (post campaign assessment) data or polio control room data','% Missed Children' UNION ALL
        SELECT 180,'Vaccinator from Local Community','Percent of vaccination teams in which at least 1 member is from local community in high risk areas','Local Vaccinators' UNION ALL
        SELECT 204,'Total number of LT vaccination transit points planned by the programme','Total number of LT vaccination transit points planned by the programme','Total # of LT transit points planned by the programme' UNION ALL
        SELECT 207,'Target number of social mobilizers and supervisors','Target number of social mobilizers and supervisors','Target # of SMs and supervisors' UNION ALL
        SELECT 215,'Number of absences resolved','Number of absences resolved','Number of absences resolved' UNION ALL
        SELECT 81,'ODK - Total Vaccinated Newborns Male','vaxnewbornsm','ODK - Total Vaccinated Newborns Male' UNION ALL
        SELECT 82,'ODK - Total Vaccinated Newborns Female','vaxnewbornsf','ODK - Total Vaccinated Newborns Female' UNION ALL
        SELECT 89,'ODK - Total Vaccinated Newborns','tot_vaxnewborn','ODK - Total Vaccinated Newborns' UNION ALL
        SELECT 86,'ODK - Total Vaccinated 2 to 11 months','tot_vax2_11mo','ODK - Total Vaccinated 2 to 11 months' UNION ALL
        SELECT 88,'ODK - Total Vaccinated 12 to 59 months','tot_vax12_59mo','ODK - Total Vaccinated 12 to 59 months' UNION ALL
        SELECT 78,'ODK - Total Vaccinated  2-11 months male','vax2_11mom','ODK - Total Vaccinated  2-11 months male' UNION ALL
        SELECT 77,'ODK - Total Vaccinated  2-11 months Female','vax2_11mof','ODK - Total Vaccinated  2-11 months Female' UNION ALL
        SELECT 80,'ODK - Total Vaccinated  12-59 months male','vax12_59mof','ODK - Total Vaccinated  12-59 months male' UNION ALL
        SELECT 79,'ODK - Total Vaccinated  12-59 months Female','vax12_59mom','ODK - Total Vaccinated  12-59 months Female' UNION ALL
        SELECT 74,'ODK - Total Vaccinated','tot_vax','ODK - Total Vaccinated' UNION ALL
        SELECT 83,'ODK - Total Newborns','tot_newborns','ODK - Total Newborns' UNION ALL
        SELECT 136,'ODK - Total Missed Due to Unhappy with Team Male','group_msd_chd_msd_unhappywteamm','ODK - Total Missed Due to Unhappy with Team Male' UNION ALL
        SELECT 137,'ODK - Total Missed Due to Unhappy with Team Female','group_msd_chd_msd_unhappywteamf','ODK - Total Missed Due to Unhappy with Team Female' UNION ALL
        SELECT 141,'ODK - Total Missed Due to Too Many Rounds Male','group_msd_chd_msd_toomanyroundsm','ODK - Total Missed Due to Too Many Rounds Male' UNION ALL
        SELECT 140,'ODK - Total Missed Due to Too Many Rounds Female','group_msd_chd_msd_toomanyroundsf','ODK - Total Missed Due to Too Many Rounds Female' UNION ALL
        SELECT 109,'ODK - Total Missed Due to Social Event Male','group_msd_chd_msd_soceventm','ODK - Total Missed Due to Social Event Male' UNION ALL
        SELECT 110,'ODK - Total Missed Due to Social Event Female','group_msd_chd_msd_soceventf','ODK - Total Missed Due to Social Event Female' UNION ALL
        SELECT 129,'ODK - Total Missed Due to Side Effects Male','group_msd_chd_msd_sideeffectsm','ODK - Total Missed Due to Side Effects Male' UNION ALL
        SELECT 128,'ODK - Total Missed Due to Side Effects Female','group_msd_chd_msd_sideeffectsf','ODK - Total Missed Due to Side Effects Female' UNION ALL
        SELECT 107,'ODK - Total Missed Due to Security Male','group_msd_chd_msd_securitym','ODK - Total Missed Due to Security Male' UNION ALL
        SELECT 108,'ODK - Total Missed Due to Security Female','group_msd_chd_msd_securityf','ODK - Total Missed Due to Security Female' UNION ALL
        SELECT 122,'ODK - Total Missed Due to Religions Beliefs Male','group_msd_chd_msd_relbeliefsm','ODK - Total Missed Due to Religions Beliefs Male' UNION ALL
        SELECT 119,'ODK - Total Missed Due to Religions Beliefs Female','group_msd_chd_msd_relbeliefsf','ODK - Total Missed Due to Religions Beliefs Female' UNION ALL
        SELECT 142,'ODK - Total Missed Due to Polio uncommon Male','group_msd_chd_msd_poliouncommonm','ODK - Total Missed Due to Polio uncommon Male' UNION ALL
        SELECT 143,'ODK - Total Missed Due to Polio uncommon Female','group_msd_chd_msd_poliouncommonf','ODK - Total Missed Due to Polio uncommon Female' UNION ALL
        SELECT 133,'ODK - Total Missed Due to Polio Has Cure Male','group_msd_chd_msd_poliohascurem','ODK - Total Missed Due to Polio Has Cure Male' UNION ALL
        SELECT 132,'ODK - Total Missed Due to Polio Has Cure Female','group_msd_chd_msd_poliohascuref','ODK - Total Missed Due to Polio Has Cure Female' UNION ALL
        SELECT 148,'ODK - Total Missed Due to Other Protection Male','group_msd_chd_msd_otherprotectionm','ODK - Total Missed Due to Other Protection Male' UNION ALL
        SELECT 147,'ODK - Total Missed Due to Other Protection Female','group_msd_chd_msd_otherprotectionf','ODK - Total Missed Due to Other Protection Female' UNION ALL
        SELECT 105,'ODK - Total Missed Due to No Plusses Male','group_msd_chd_msd_noplusesm','ODK - Total Missed Due to No Plusses Male' UNION ALL
        SELECT 106,'ODK - Total Missed Due to No Plusses Female','group_msd_chd_msd_noplusesf','ODK - Total Missed Due to No Plusses Female' UNION ALL
        SELECT 145,'ODK - Total Missed Due to No Government Services Male','group_msd_chd_msd_nogovtservicesm','ODK - Total Missed Due to No Government Services Male' UNION ALL
        SELECT 146,'ODK - Total Missed Due to No Government Services Female','group_msd_chd_msd_nogovtservicesf','ODK - Total Missed Due to No Government Services Female' UNION ALL
        SELECT 194,'District Had Delayed OPV Supply','Percent of High Risk Districts that did not receive polio vaccine supply at least 3 days before the planned starting date of the campaign','Delayed OPV Supply' UNION ALL
        SELECT 117,'ODK - Total Missed Due to No Consent Male','group_msd_chd_msd_noconsentm','ODK - Total Missed Due to No Consent Male' UNION ALL
        SELECT 118,'ODK - Total Missed Due to No Consent Female','group_msd_chd_msd_noconsentf','ODK - Total Missed Due to No Consent Female' UNION ALL
        SELECT 139,'ODK - Total Missed Due to Household not visited Male','group_msd_chd_msd_hhnotvisitedm','ODK - Total Missed Due to Household not visited Male' UNION ALL
        SELECT 138,'ODK - Total Missed Due to Household not visited Female','group_msd_chd_msd_hhnotvisitedf','ODK - Total Missed Due to Household not visited Female' UNION ALL
        SELECT 121,'ODK - Total Missed Due to Felt Not Needed Male','group_msd_chd_msd_nofeltneedm','ODK - Total Missed Due to Felt Not Needed Male' UNION ALL
        SELECT 120,'ODK - Total Missed Due to Felt Not Needed Female','group_msd_chd_msd_nofeltneedf','ODK - Total Missed Due to Felt Not Needed Female' UNION ALL
        SELECT 131,'ODK - Total Missed Due to Family Moved Male','group_msd_chd_msd_familymovedm','ODK - Total Missed Due to Family Moved Male' UNION ALL
        SELECT 130,'ODK - Total Missed Due to Family Moved Female','group_msd_chd_msd_familymovedf','ODK - Total Missed Due to Family Moved Female' UNION ALL
        SELECT 101,'ODK - Total Missed Due to Children at Schools Male','group_msd_chd_msd_schoolm','ODK - Total Missed Due to Children at Schools Male' UNION ALL
        SELECT 100,'ODK - Total Missed Due to Children at Schools Female','group_msd_chd_msd_schoolf','ODK - Total Missed Due to Children at Schools Female' UNION ALL
        SELECT 115,'ODK - Total Missed Due to Child Sick Male','group_msd_chd_msd_childsickm','ODK - Total Missed Due to Child Sick Male' UNION ALL
        SELECT 116,'ODK - Total Missed Due to Child Sick Female','group_msd_chd_msd_childsickf','ODK - Total Missed Due to Child Sick Female' UNION ALL
        SELECT 96,'ODK - Total Missed Due to Child on Farm Male','group_msd_chd_msd_farmm','ODK - Total Missed Due to Child on Farm Male' UNION ALL
        SELECT 97,'ODK - Total Missed Due to Child on Farm Female','group_msd_chd_msd_farmf','ODK - Total Missed Due to Child on Farm Female' UNION ALL
        SELECT 114,'ODK - Total Missed Due to Child Died Male','group_msd_chd_msd_childdiedm','ODK - Total Missed Due to Child Died Male' UNION ALL
        SELECT 123,'ODK - Total Missed Due to Child at Playground Male','group_msd_chd_msd_playgroundm','ODK - Total Missed Due to Child at Playground Male' UNION ALL
        SELECT 124,'ODK - Total Missed Due to Child at Playground Female','group_msd_chd_msd_playgroundf','ODK - Total Missed Due to Child at Playground Female' UNION ALL
        SELECT 98,'ODK - Total Missed Due to Child at Market Male','group_msd_chd_msd_marketm','ODK - Total Missed Due to Child at Market Male' UNION ALL
        SELECT 99,'ODK - Total Missed Due to Child at Market Female','group_msd_chd_msd_marketf','ODK - Total Missed Due to Child at Market Female' UNION ALL
        SELECT 102,'ODK - Total missed due to Aged Out Male','group_msd_chd_msd_agedoutm','ODK - Total missed due to Aged Out Male' UNION ALL
        SELECT 103,'ODK - Total missed due to Aged Out Female','group_msd_chd_msd_agedoutf','ODK - Total missed due to Aged Out Female' UNION ALL
        SELECT 113,'ODK - Total Missed Due to  Child Died Female','group_msd_chd_msd_childdiedf','ODK - Total Missed Due to  Child Died Female' UNION ALL
        SELECT 76,'ODK - Total Missed','tot_missed','ODK - Total Missed' UNION ALL
        SELECT 90,'ODK - Total Children 2 to 11 months','tot_2_11months','ODK - Total Children 2 to 11 months' UNION ALL
        SELECT 92,'ODK - Total children 12 to 59 Months','tot_12_59months','ODK - Total children 12 to 59 Months' UNION ALL
        SELECT 75,'ODK - Total Census','tot_census','ODK - Total Census' UNION ALL
        SELECT 127,'ODK - group_msd_chd_tot_missed_check','group_msd_chd_tot_missed_check','ODK - group_msd_chd_tot_missed_check' UNION ALL
        SELECT 84,'ODK - Census 2 to 11 months Male','census2_11mom','ODK - Census 2 to 11 months Male' UNION ALL
        SELECT 85,'ODK - Census 2 to 11 months Female','census2_11mof','ODK - Census 2 to 11 months Female' UNION ALL
        SELECT 87,'ODK - Census 12 to 59 months Male','census12_59mom','ODK - Census 12 to 59 months Male' UNION ALL
        SELECT 91,'ODK - Census 12 to 59 months Female','census12_59mof','ODK - Census 12 to 59 months Female' UNION ALL
        SELECT 94,'ODK - Census  Newborns Male','censusnewbornsm','ODK - Census  Newborns Male' UNION ALL
        SELECT 111,'ODK - group_msd_chd_msd_poldiffsm','group_msd_chd_msd_poldiffsm','ODK - group_msd_chd_msd_poldiffsm' UNION ALL
        SELECT 126,'ODK - group_spec_events_spec_afpcase','group_spec_events_spec_afpcase','ODK - group_spec_events_spec_afpcase' UNION ALL
        SELECT 149,'ODK - group_spec_events_spec_cmamreferral','group_spec_events_spec_cmamreferral','ODK - group_spec_events_spec_cmamreferral' UNION ALL
        SELECT 104,'ODK - group_spec_events_spec_fic','group_spec_events_spec_fic','ODK - group_spec_events_spec_fic' UNION ALL
        SELECT 125,'ODK - group_spec_events_spec_newborn','group_spec_events_spec_newborn','ODK - group_spec_events_spec_newborn' UNION ALL
        SELECT 150,'ODK - group_spec_events_spec_otherdisease','group_spec_events_spec_otherdisease','ODK - group_spec_events_spec_otherdisease' UNION ALL
        SELECT 151,'ODK - group_spec_events_spec_pregnantmother','group_spec_events_spec_pregnantmother','ODK - group_spec_events_spec_pregnantmother' UNION ALL
        SELECT 144,'ODK - group_spec_events_spec_rireferral','group_spec_events_spec_rireferral','ODK - group_spec_events_spec_rireferral' UNION ALL
        SELECT 152,'ODK - group_spec_events_spec_vcmattendedncer','group_spec_events_spec_vcmattendedncer','ODK - group_spec_events_spec_vcmattendedncer' UNION ALL
        SELECT 135,'ODK - group_spec_events_spec_zerodose','group_spec_events_spec_zerodose','ODK - group_spec_events_spec_zerodose' UNION ALL
        SELECT 274,'Outside_Percent missed children','Outside_Percent missed children','Not Marked' UNION ALL
        SELECT 198,'Number of functional active cold chain equipment in the district','Number of functional active cold chain equipment in the district','# functional active cold chain equipment in district' UNION ALL
        SELECT 201,'District has specific access approach identified (1=yes, 0=no)','District has specific access approach identified (1=yes, 0=no)','District has specific access approach identified' UNION ALL
        SELECT 208,'Number of vaccination teams with at least 1 member from the local community','Number of vaccination teams with at least 1 member from the local community','# of vaccination teams with at least 1 local member' UNION ALL
        SELECT 209,'Number of social mobilizers trained or refreshed with the integrated health package in the last 6 months','Number of social mobilizers trained or refreshed with the integrated health package in the last 6 months','# SMs trained, refreshed w. health package in last 6 mo' UNION ALL
        SELECT 55,'Number of children targeted in high-risk districts','Number of children targeted in high-risk districts','Number of children targeted in HRDs' UNION ALL
        SELECT 220,'Vaccine wastage rate','Vaccine wastage rate','Vaccine wastage rate' UNION ALL
        SELECT 33,'Number of high risk sub-districts','Number of high risk sub-districts ','Number of high risk sub-districts ' UNION ALL
        SELECT 195,'Is a high risk district? (1=yes, 0=no)','Is a high risk district? (1=yes, 0=no)','Is high risk?' UNION ALL
        SELECT 254,'Endprocess_NOimmReas10 - Fear of OPV side effects','Endprocess_NOimmReas10 - Fear of OPV side effects','Fear of Side Effects' UNION ALL
        SELECT 221,'Is an HRD that has polio vaccine wastage rate in SIAs between 5 and 15% (1=yes, 0=no)','Is an HRD that has polio vaccine wastage rate in SIAs between 5 and 15% (1=yes, 0=no)','Is an that has polio vaccine wastage btwn 5-15%' UNION ALL
        SELECT 224,'Percentage of established LT vaccination transit points with a dedicated social mobilizer, out of total number established by the programme','Percentage of established LT vaccination transit points with a dedicated social mobilizer, out of total number established by the programme','Percentage of established LT vaccination transit points with a dedicated social mobilizer, out of total number established by the programme' UNION ALL
        SELECT 222,'Percentage of districts with microplans that passed review (out of districts sampled)','Percentage of districts with microplans that passed review (out of districts sampled)','Percentage of districts with microplans that passed review' UNION ALL
        SELECT 191,'Routine Immunization Session Stockout','Proprotion of routine immunization sessions monitored having stockouts of any vaccine during last month','RI Stockouts' UNION ALL
        SELECT 178,'Geographic Coverage by Social Mobilisers','Proportion of High-Risk sub-districts covered by social mobilisers','Mobiliser Coverage' UNION ALL
        SELECT 184,'Social Mobilisers Training in Integrated Health Package','Proportion of social mobilisers trained or refreshed with the integrated health package in the last 6 months','Mobiliser Training on Polio+' UNION ALL
        SELECT 250,'Endprocess_NOimmReas7 - Child at school','Endprocess_NOimmReas7 - Child at school','School ' UNION ALL
        SELECT 273,'Outside_Total Not Marked','Outside_Total Not Marked','Missed (Outside)' UNION ALL
        SELECT 272,'Endprocess_Percent missed children','Endprocess_Percent missed children','Missed Children' UNION ALL
        SELECT 247,'Endprocess_NoimmReas4 - Child at social event','Endprocess_NoimmReas4 - Child at social event','Social Event ' UNION ALL
        SELECT 249,'Endprocess_NOimmReas6 - Child at farm','Endprocess_NOimmReas6 - Child at farm','Farm ' UNION ALL
        SELECT 242,'Number of vaccine doses wasted','Number of vaccine doses wasted','Number of vaccine doses wasted' UNION ALL
        SELECT 243,'Number of children 12 months and under','Number of children 12 months and under','Number of children 12 months and under' UNION ALL
        SELECT 244,'Number of children under 12 months who received DPT3 or Penta3','Number of children under 12 months who received DPT3 or Penta3','No. of children under 12 months who received RI' UNION ALL
        SELECT 248,'Endprocess_NOimmReas5 - Child at market','Endprocess_NOimmReas5 - Child at market','Market ' UNION ALL
        SELECT 246,'Endprocess_NOimmReas3 - Child at playground','Endprocess_NOimmReas3 - Child at playground','Playground ' UNION ALL
        SELECT 253,'Endprocess_NOimmReas9 - Too many rounds','Endprocess_NOimmReas9 - Too many rounds','Too Many Rounds ' UNION ALL
        SELECT 263,'Endprocess_NOimmReas19 - No caregiver consent','Endprocess_NOimmReas19 - No caregiver consent','No Consent' UNION ALL
        SELECT 251,'Endprocess_Reason for missed children - child absent','Endprocess_Reason for missed children - child absent','Child Absent' UNION ALL
        SELECT 252,'Endprocess_NOimmReas8 - Child sick','Endprocess_NOimmReas8 - Child sick','Child Sick' UNION ALL
        SELECT 236,'Caregiver Knowledge of Routine Immunization','Proportion of caregivers in HRDs who know number of times they need to visit a RI site for routine immunization before a child reaches 1 year of age','Knowledge of RI' UNION ALL
        SELECT 239,'Female Social Moblisers in Place','Proportion of female social mobilisers among social mobilisers in place','Female Mobilisers' UNION ALL
        SELECT 185,'On-the-Job Supervision of Social Mobilisers','Proportion of social mobilisers who received on-the-job supervision during their last working week','Mobiliser Supervision' UNION ALL
        SELECT 226,'Timely Payment to Social Mobilisers','Proportion of social mobilisers who received timely payment for last campaign/month''s salary among ALL social mobilisers involved in the campaign.','Timely Mobiliser Payment' UNION ALL
        SELECT 228,'Vaccinator Training in Inter-Personal Communication Skills','Proportion of vaccinators operating in HRD who have been trained on professional Inter Personal Communication package provided by UNICEF in the last 6 months','Vaccinator Training on IPC Skills' UNION ALL
        SELECT 230,'Female Vaccinator in Team','Proportion of vaccination teams in which at least one member is female in HR areas','Female Vaccinators' UNION ALL
        SELECT 476,'(TW Test) Infected People','How many people infected?','tw-test-outbreak-infected-people' UNION ALL
        SELECT 477,'TW Test Outbreak Infected People','TW Test Outbreak Infected People','TW Test Outbreak Infected People' UNION ALL
        SELECT 279,'Endprocess_Influence5 - Radio','Endprocess_Influence5 - Radio','Radio   ' UNION ALL
        SELECT 258,'Endprocess_NOimmReas14 - Religious belief','Endprocess_NOimmReas14 - Religious belief','Religious Beliefs ' UNION ALL
        SELECT 288,'Endprocess_Percent vaccination influencer is radio','Endprocess_Percent vaccination influencer is radio','Radio ' UNION ALL
        SELECT 266,'Endprocess_NOimmReas20 - Security','Endprocess_NOimmReas20 - Security','Security ' UNION ALL
        SELECT 269,'Endprocess_Number of children 0 to 59 marked','Endprocess_Number of children 0 to 59 marked','Endprocess_Marked0to59' UNION ALL
        SELECT 270,'Endprocess_Number of children 0 to 59 unimmunized','Endprocess_Number of children 0 to 59 unimmunized','Endprocess_UnImmun0to59' UNION ALL
        SELECT 271,'Endprocess_Number of children seen','Endprocess_Number of children seen','Endprocess_Number of children seen' UNION ALL
        SELECT 275,'Outside_Total seen','Outside_Total seen','Outside_Total seen' UNION ALL
        SELECT 287,'Endprocess_Percent vaccination influencer is personal decision','Endprocess_Percent vaccination influencer is personal decision','Personal Decision' UNION ALL
        SELECT 277,'Endprocess_Not aware','Endprocess_Not aware','Endprocess_Not aware' UNION ALL
        SELECT 285,'Endprocess_Influence8 - Vaccinator','Endprocess_Influence8 - Vaccinator','Vaccinator ' UNION ALL
        SELECT 260,'Endprocess_NOimmReas16 - Unhappy with vaccination team','Endprocess_NOimmReas16 - Unhappy with vaccination team','Unhappy with Team' UNION ALL
        SELECT 291,'Endprocess_Percent vaccination influencer is traditional leader','Endprocess_Percent vaccination influencer is traditional leader','Trad. Leader' UNION ALL
        SELECT 282,'Endprocess_Influence3 - Traditional leader','Endprocess_Influence3 - Traditional leader','Trad. Leader   ' UNION ALL
        SELECT 293,'Endprocess_Percent vaccination influencer is religious leader','Endprocess_Percent vaccination influencer is religious leader','Rel. Leader' UNION ALL
        SELECT 284,'Endprocess_Influence4 - Religious leader','Endprocess_Influence4 - Religious leader','Rel. Leader   ' UNION ALL
        SELECT 290,'Endprocess_Percent vaccination influencer is neighbour','Endprocess_Percent vaccination influencer is neighbour','Neighbour ' UNION ALL
        SELECT 265,'Endprocess_Missed children - All reasons','Endprocess_Missed children - All reasons','Missed (Inside)' UNION ALL
        SELECT 286,'Endprocess_All vaccination influencers','Endprocess_All vaccination influencers','Endprocess_All vaccination influencers' UNION ALL
        SELECT 289,'Endprocess_Percent vaccination influencer is husband','Endprocess_Percent vaccination influencer is husband','Husband' UNION ALL
        SELECT 173,'Cold Chain Functional Status','Proportion of high risk districts where at least 90% of active cold chain equipment are functional','Cold Chain Functional Status' UNION ALL
        SELECT 276,'Endprocess_Percent caregiver awareness','Endprocess_Percent caregiver awareness','Caregiver Awareness' UNION ALL
        SELECT 283,'Endprocess_Influence7 - Community mobiliser','Endprocess_Influence7 - Community mobiliser','Comm. Mobiliser ' UNION ALL
        SELECT 292,'Endprocess_Pct vaccination influencer is community mobiliser','Endprocess_Pct vaccination influencer is community mobiliser','Comm. Mobiliser  ' UNION ALL
        SELECT 280,'Endprocess_Influence2 - Husband','Endprocess_Influence2 - Husband','Husband ' UNION ALL
        SELECT 281,'Endprocess_Influence6 - Neighbour','Endprocess_Influence6 - Neighbour','Neighbour  ' UNION ALL
        SELECT 262,'Endprocess_NOimmReas18 - No felt need','Endprocess_NOimmReas18 - No felt need','No Felt Needed' UNION ALL
        SELECT 264,'Endprocess_Reason for missed children - Non compliance','Endprocess_Reason for missed children - Non compliance','Non-Comp. ' UNION ALL
        SELECT 261,'Endprocess_NOimmReas17 - No pluses given','Endprocess_NOimmReas17 - No pluses given','No Pluses ' UNION ALL
        SELECT 267,'Endprocess_NOimmReas1 - Household not in microplan','Endprocess_NOimmReas1 - Household not in microplan','Not in Plan ' UNION ALL
        SELECT 268,'Endprocess_NOimmReas2 - Household in microplan but not visited','Endprocess_NOimmReas2 - Household in microplan but not visited','Not Visited ' UNION ALL
        SELECT 278,'Endprocess_Influence1 - Personal decision','Endprocess_Influence1 - Personal decision','Personal Decision ' UNION ALL
        SELECT 256,'Endprocess_NOimmReas12 - Polio has cure','Endprocess_NOimmReas12 - Polio has cure','Polio has Cure ' UNION ALL
        SELECT 259,'Endprocess_NOimmReas15 - Political differences','Endprocess_NOimmReas15 - Political differences','Political ' UNION ALL
        SELECT 307,'Endprocess_Percent source of info is town announcer','Endprocess_Percent source of info is town announcer','Town Announcer' UNION ALL
        SELECT 324,'Endprocess_Pct of children absent due to child at social event','Endprocess_Pct of children absent due to child at social event','Social Event' UNION ALL
        SELECT 322,'Endprocess_Pct missed children due to security','Endprocess_Pct missed children due to security','Security' UNION ALL
        SELECT 296,'Endprocess_Source of info on IPDs - Radio','Endprocess_Source of info on IPDs - Radio','Radio  ' UNION ALL
        SELECT 303,'Endprocess_Source of info on IPDs - Relative','Endprocess_Source of info on IPDs - Relative','Relative ' UNION ALL
        SELECT 306,'Endprocess_All sources of info on IPDs','Endprocess_All sources of info on IPDs','Endprocess_All sources of info on IPDs' UNION ALL
        SELECT 309,'Endprocess_Percent source of info is relative','Endprocess_Percent source of info is relative','Relative' UNION ALL
        SELECT 295,'Endprocess_Source of info on IPDs - Town announcer','Endprocess_Source of info on IPDs - Town announcer','Town Announcer ' UNION ALL
        SELECT 310,'Endprocess_Percent source of info is radio','Endprocess_Percent source of info is radio','Radio' UNION ALL
        SELECT 314,'Endprocess_Percent source of info is poster','Endprocess_Percent source of info is poster','Poster' UNION ALL
        SELECT 323,'Endprocess_Pct of children absent due to playground','Endprocess_Pct of children absent due to playground','Playground' UNION ALL
        SELECT 319,'Endprocess_Pct missed children due to HH in plan but not visited','Endprocess_Pct missed children due to HH in plan but not visited','Not Visited' UNION ALL
        SELECT 321,'Endprocess_Pct missed children due to non compliance','Endprocess_Pct missed children due to non compliance','Non-Comp.' UNION ALL
        SELECT 311,'Endprocess_Percent source of info is newspaper','Endprocess_Percent source of info is newspaper','Newspaper' UNION ALL
        SELECT 308,'Endprocess_Percent source of info is mosque announcement','Endprocess_Percent source of info is mosque announcement','Mosque' UNION ALL
        SELECT 313,'Endprocess_Percent source of info is traditional leader','Endprocess_Percent source of info is traditional leader','Trad. Leader  ' UNION ALL
        SELECT 325,'Endprocess_Pct of children absent due to child at market','Endprocess_Pct of children absent due to child at market','Market' UNION ALL
        SELECT 318,'Endprocess_Percent missed children due to HH not in plan','Endprocess_Percent missed children due to HH not in plan','Not in Plan' UNION ALL
        SELECT 297,'Endprocess_Source of info on IPDs - Traditional leader','Endprocess_Source of info on IPDs - Traditional leader','Trad. Leader ' UNION ALL
        SELECT 312,'Endprocess_Percent source of info is health worker','Endprocess_Percent source of info is health worker','Health Worker' UNION ALL
        SELECT 316,'Endprocess_Percent source of info is religious leader','Endprocess_Percent source of info is religious leader','Rel. Leader ' UNION ALL
        SELECT 315,'Endprocess_Percent source of info is community mobiliser','Endprocess_Percent source of info is community mobiliser','Comm. Mobiliser' UNION ALL
        SELECT 298,'Endprocess_Source of info on IPDs - Religious leader','Endprocess_Source of info on IPDs - Religious leader','Rel. Leader  ' UNION ALL
        SELECT 320,'Endprocess_Pct missed children due to child absent','Endprocess_Pct missed children due to child absent','Child Absent ' UNION ALL
        SELECT 302,'Endprocess_Source of info on IPDs - Banner','Endprocess_Source of info on IPDs - Banner','Banner' UNION ALL
        SELECT 317,'Endprocess_Percent source of info is banner','Endprocess_Percent source of info is banner','Banner ' UNION ALL
        SELECT 305,'Endprocess_Source of info on IPDs - Community mobiliser','Endprocess_Source of info on IPDs - Community mobiliser','Comm. Mobiliser    ' UNION ALL
        SELECT 304,'Endprocess_Source of info on IPDs - Health worker','Endprocess_Source of info on IPDs - Health worker','Health Worker ' UNION ALL
        SELECT 299,'Endprocess_Source of info on IPDs - Mosque announcement','Endprocess_Source of info on IPDs - Mosque announcement','Mosque ' UNION ALL
        SELECT 300,'Endprocess_Source of info on IPDs - Newspaper','Endprocess_Source of info on IPDs - Newspaper','Newspaper ' UNION ALL
        SELECT 301,'Endprocess_Source of info on IPDs - Poster','Endprocess_Source of info on IPDs - Poster','Poster ' UNION ALL
        SELECT 332,'Endprocess_Pct of non compliance due to too many rounds','Endprocess_Pct of non compliance due to too many rounds','Too Many Rounds' UNION ALL
        SELECT 327,'Endprocess_Pct of children absent due to child at school','Endprocess_Pct of children absent due to child at school','School' UNION ALL
        SELECT 330,'Endprocess_Pct of non compliance due to religious belief','Endprocess_Pct of non compliance due to religious belief','Religious Beliefs' UNION ALL
        SELECT 335,'Endprocess_Pct of non compliance due to fear of OPV side effects','Endprocess_Pct of non compliance due to fear of OPV side effects','Endprocess_Pct of non compliance due to OPV side effect' UNION ALL
        SELECT 336,'Endprocess_Pct of non compliance due to other remedies available','Endprocess_Pct of non compliance due to other remedies available','Endprocess_Pct of non compliance due to other remedies ' UNION ALL
        SELECT 337,'Endprocess_Pct of non compliance due to unhappy with team','Endprocess_Pct of non compliance due to unhappy with team','Endprocess_Pct of non compliance due to unhappy w team' UNION ALL
        SELECT 338,'Endprocess_Pct of non compliance due to no caregiver consent','Endprocess_Pct of non compliance due to no caregiver consent','Endprocess_Pct of non compliance due no caregiver conse' UNION ALL
        SELECT 339,'Endprocess_Pct of non compliance due to no felt need','Endprocess_Pct of non compliance due to no felt need','Endprocess_Pct of non compliance due to no felt need' UNION ALL
        SELECT 334,'Endprocess_Pct of non compliance due to political differences','Endprocess_Pct of non compliance due to political differences','Political' UNION ALL
        SELECT 329,'Endprocess_Pct of non compliance due to polio is rare','Endprocess_Pct of non compliance due to polio is rare','Polio is Rare' UNION ALL
        SELECT 333,'Endprocess_Pct of non compliance due to polio has cure','Endprocess_Pct of non compliance due to polio has cure','Polio has Cure' UNION ALL
        SELECT 344,'Redo_Number of children 0 to 59 months missed in HH due to non compliance','Redo_Number of children 0 to 59 months missed in HH due to non compliance','Redo_No of children 0 to 59 missed in HH due to NC' UNION ALL
        SELECT 348,'Redo_Percent non compliance resolved by other','Redo_Percent non compliance resolved by other','Other' UNION ALL
        SELECT 331,'Endprocess_Pct of non compliance due to no pluses given','Endprocess_Pct of non compliance due to no pluses given','No Pluses' UNION ALL
        SELECT 349,'Endprocess_Aware','Endprocess_Aware','Endprocess_Aware' UNION ALL
        SELECT 350,'Redo_Number of children 0-59 months missed in HH due to child absence','Redo_Number of children 0-59 months missed in HH due to child absence','Redo_Child absent' UNION ALL
        SELECT 351,'Redo_Number of children 0-59 months missed in other NC places','Redo_Number of children 0-59 months missed in other NC places','Redo_ChildNCOther' UNION ALL
        SELECT 352,'Redo_Number of children 0-59 months missed in NC schools','Redo_Number of children 0-59 months missed in NC schools','Redo_ChildNCShool' UNION ALL
        SELECT 353,'Redo_Reasons for NC - Child sick','Redo_Reasons for NC - Child sick','Redo_ChildSick' UNION ALL
        SELECT 354,'Redo_No. immunised in households with community leader intervention - Child absent','Redo_No. immunised in households with community leader intervention - Child absent','Redo_COMImmRedoABSENT' UNION ALL
        SELECT 355,'Redo_No. of household resolved','Redo_No. of household resolved','Redo_HHRevisited' UNION ALL
        SELECT 356,'Redo_No. immunised in other NC places with intervention of community influencers','Redo_No. immunised in other NC places with intervention of community influencers','Redo_IMMOTCommNC' UNION ALL
        SELECT 345,'Redo_Percent non compliance resolved by traditional leader','Redo_Percent non compliance resolved by traditional leader','Trad. Leader     ' UNION ALL
        SELECT 340,'Redo_Non compliance resolved by traditional leader','Redo_Non compliance resolved by traditional leader','Trad. Leader    ' UNION ALL
        SELECT 347,'Redo_Percent non compliance resolved by religious leader','Redo_Percent non compliance resolved by religious leader','Rel. Leader     ' UNION ALL
        SELECT 342,'Redo_Non compliance resolved by religious leader','Redo_Non compliance resolved by religious leader','Rel. Leader    ' UNION ALL
        SELECT 346,'Redo_Percent non compliance resolved by community leader','Redo_Percent non compliance resolved by community leader','Comm. Leader' UNION ALL
        SELECT 328,'Endprocess_Pct of non compliance due to child sick','Endprocess_Pct of non compliance due to child sick','Child Sick ' UNION ALL
        SELECT 341,'Redo_Non compliance resolved by community leader','Redo_Non compliance resolved by community leader','Comm. Leader ' UNION ALL
        SELECT 343,'Redo_Non compliance resolved by other','Redo_Non compliance resolved by other','Other ' UNION ALL
        SELECT 357,'Redo_No. immunised in other NC places with intervention of others','Redo_No. immunised in other NC places with intervention of others','Redo_IMMOTOtherNC' UNION ALL
        SELECT 358,'Redo_No. immunised in other NC places with intervention of religious leaders','Redo_No. immunised in other NC places with intervention of religious leaders','Redo_IMMOTRelNC' UNION ALL
        SELECT 359,'Redo_No. immunised in other NC places with intervention of traditional leaders','Redo_No. immunised in other NC places with intervention of traditional leaders','Redo_IMMOTTradNC' UNION ALL
        SELECT 360,'Redo_No. Immunised in households with traditonal leader intervention - Child absent','Redo_No. Immunised in households with traditonal leader intervention - Child absent','Redo_ImmRedoABSENT' UNION ALL
        SELECT 361,'Redo_No. immunised in NC schools with intervention of community influencer','Redo_No. immunised in NC schools with intervention of community influencer','Redo_IMMSCCommNC' UNION ALL
        SELECT 362,'Redo_No. immunised in NC schools with intervention of others','Redo_No. immunised in NC schools with intervention of others','Redo_IMMSCOtherNC' UNION ALL
        SELECT 363,'Redo_No. immunised in NC schools with intervention of religious leader','Redo_No. immunised in NC schools with intervention of religious leader','Redo_IMMSCRelNC' UNION ALL
        SELECT 364,'Redo_No. immunised in NC schools with intervention of traditional leader','Redo_No. immunised in NC schools with intervention of traditional leader','Redo_IMMSCTradNC' UNION ALL
        SELECT 365,'Redo_Reasons for NC - No caregiver consent','Redo_Reasons for NC - No caregiver consent','Redo_NoCaregiver' UNION ALL
        SELECT 366,'Redo_Number of NC households','Redo_Number of NC households','Redo_NoHHRedo' UNION ALL
        SELECT 370,'Redo_No. of NC children not immunised (not resolved)','Redo_No. of NC children not immunised (not resolved)','Redo_NotImmRedo' UNION ALL
        SELECT 371,'Redo_No. of children absent not immunised (not resolved)','Redo_No. of children absent not immunised (not resolved)','Redo_NotImmRedoABSENT' UNION ALL
        SELECT 372,'Redo_Reasons for NC - OPV safety','Redo_Reasons for NC - OPV safety','Redo_OpvSafety' UNION ALL
        SELECT 368,'Redo_Reasons for NC - No need felt','Redo_Reasons for NC - No need felt','Redo_NoNeedFelt' UNION ALL
        SELECT 369,'Redo_Number of other NC places','Redo_Number of other NC places','Redo_NoNOCOther' UNION ALL
        SELECT 373,'Redo_No. immunised in households with intervention of others - Child absent','Redo_No. immunised in households with intervention of others - Child absent','Redo_OTHERImRedoABSENT' UNION ALL
        SELECT 374,'Redo_No. of other places resolved','Redo_No. of other places resolved','Redo_OTRevisited' UNION ALL
        SELECT 375,'Redo_Reasons for NC - Political differences','Redo_Reasons for NC - Political differences','Redo_PoliticalDifferences' UNION ALL
        SELECT 376,'Redo_Reasons for child absent - Playground','Redo_Reasons for child absent - Playground','Redo_Reason1ABS' UNION ALL
        SELECT 377,'Redo_Reasons for child absent - Market','Redo_Reasons for child absent - Market','Redo_Reason2ABS' UNION ALL
        SELECT 378,'Redo_Reasons for child absent - School','Redo_Reasons for child absent - School','Redo_Reason3ABS' UNION ALL
        SELECT 379,'Redo_Reasons for child absent - Farm','Redo_Reasons for child absent - Farm','Redo_Reason4ABS' UNION ALL
        SELECT 380,'Redo_Reasons for child absent - Social Event','Redo_Reasons for child absent - Social Event','Redo_Reason5ABS' UNION ALL
        SELECT 381,'Redo_Reasons for child absent - Other','Redo_Reasons for child absent - Other','Redo_Reason6ABS' UNION ALL
        SELECT 382,'Redo_Reasons for NC - Reason not given','Redo_Reasons for NC - Reason not given','Redo_ReasonNotGiven' UNION ALL
        SELECT 383,'Redo_Reasons for NC - Religious belief','Redo_Reasons for NC - Religious belief','Redo_ReligiousBelief' UNION ALL
        SELECT 384,'Redo_No. immunised in households with religious leader intervention - Child absent','Redo_No. immunised in households with religious leader intervention - Child absent','Redo_RELImmRedoABSENT' UNION ALL
        SELECT 385,'Redo_No. of schools resolved','Redo_No. of schools resolved','Redo_SCRevisited' UNION ALL
        SELECT 386,'Redo_No. of settlements to revisit','Redo_No. of settlements to revisit','Redo_SettlementsRedo' UNION ALL
        SELECT 387,'Redo_Reasons for NC - Too many rounds','Redo_Reasons for NC - Too many rounds','Redo_TooManyRounds' UNION ALL
        SELECT 388,'Redo_Reasons for NC - unhappy with immunisation personnel','Redo_Reasons for NC - unhappy with immunisation personnel','Redo_UnhappyWith' UNION ALL
        SELECT 367,'Redo_Number of NC schools','Redo_Number of NC schools','Redo_NoNCShools' UNION ALL
        SELECT 389,'Redo_MissedRedo','Redo_MissedRedo','Redo_MissedRedo' UNION ALL
        SELECT 390,'Redo_TargetRedo','Redo_TargetRedo','Redo_TargetRedo' UNION ALL
        SELECT 391,'Outside_Number of settlements visited by suveyor','Outside_Number of settlements visited by suveyor','Outside_Settlementno' UNION ALL
        SELECT 392,'Outside_total number of children sampled in settlement 3','Outside_total number of children sampled in settlement 3','Outside_totSeet3' UNION ALL
        SELECT 393,'Outside_total children not finger marked (not immunized) in settlement 3','Outside_total children not finger marked (not immunized) in settlement 3','Outside_totMist3' UNION ALL
        SELECT 394,'Outside_total number of children sampled in settlement 1','Outside_total number of children sampled in settlement 1','Outside_totSeet1' UNION ALL
        SELECT 395,'Outside_total number of children sampled in settlement 2','Outside_total number of children sampled in settlement 2','Outside_totSeet2' UNION ALL
        SELECT 396,'Outside_total children not finger marked (not immunized) in settlement 1','Outside_total children not finger marked (not immunized) in settlement 1','Outside_totMist1' UNION ALL
        SELECT 397,'Outside_total children not finger marked (not immunized) in settlement 2','Outside_total children not finger marked (not immunized) in settlement 2','Outside_totMist2' UNION ALL
        SELECT 398,'Outside_total number of locations sampled by suveyor','Outside_total number of locations sampled by suveyor','Outside_numberof Locations' UNION ALL
        SELECT 399,'Outside_Unvaccinated this round','Outside_Unvaccinated this round','Outside_Unvaccinated this round' UNION ALL
        SELECT 400,'Outside_0to9mth Seen','Outside_0to9mth Seen','Outside_0to9mth Seen' UNION ALL
        SELECT 5,'Number of vaccine doses used in HRD','Number of vaccine doses used in HRD','Number of vaccine doses used in HRD' UNION ALL
        SELECT 401,'Outside_0to9mth notMarked','Outside_0to9mth notMarked','Outside_0to9mth notMarked' UNION ALL
        SELECT 404,'Outside_children 24-59mth sampled by suveyor','Outside_children 24-59mth sampled by suveyor','Outside_24to59mth Seen' UNION ALL
        SELECT 402,'Outside_children 0-23mth sampled by suveyor','Outside_children 0-23mth sampled by suveyor','Outside_children 0-23mth sampled by suveyor' UNION ALL
        SELECT 403,'Outside_children 0-23mth not finger marked','Outside_children 0-23mth not finger marked','Outside_children 0-23mth not finger marked' UNION ALL
        SELECT 405,'Outside_children 24-59mth not finger marked (not immunized)','Outside_children 24-59mth not finger marked (not immunized)','Outside_24to59mth notMarked' UNION ALL
        SELECT 406,'Outside_total number of children sampled (calculated)','Outside_total number of children sampled (calculated)','Outside_TOTAL Seen' UNION ALL
        SELECT 407,'Outside_total number of children not finger marked (calculated)','Outside_total number of children not finger marked (calculated)','Outside_TOTAL Notmarked' UNION ALL
        SELECT 408,'Outside_total number of children seen in settlement 4','Outside_total number of children seen in settlement 4','Outside_totSeet4' UNION ALL
        SELECT 409,'Outside_total children not finger marked (not immunized) in settlement 4','Outside_total children not finger marked (not immunized) in settlement 4','Outside_totMist4' UNION ALL
        SELECT 410,'Outside_total number of children sampled in settlement 5','Outside_total number of children sampled in settlement 5','Outside_totSeet5' UNION ALL
        SELECT 411,'Outside_total number of children sampled in settlement 6','Outside_total number of children sampled in settlement 6','Outside_totSeet6' UNION ALL
        SELECT 412,'Outside_total children not finger marked (not immunized) in settlement 5','Outside_total children not finger marked (not immunized) in settlement 5','Outside_totMist5' UNION ALL
        SELECT 413,'Outside_total children not finger marked (not immunized) in settlement 6','Outside_total children not finger marked (not immunized) in settlement 6','Outside_totMist6' UNION ALL
        SELECT 414,'Endprocess_HHsampled','Endprocess_HHsampled','Endprocess_HHsampled' UNION ALL
        SELECT 415,'Endprocess_HHvisitedTEAMS','Endprocess_HHvisitedTEAMS','Endprocess_HHvisitedTEAMS' UNION ALL
        SELECT 416,'Endprocess_ZeroDose','Endprocess_ZeroDose','Endprocess_ZeroDose' UNION ALL
        SELECT 417,'Endprocess_TotalYoungest','Endprocess_TotalYoungest','Endprocess_TotalYoungest' UNION ALL
        SELECT 418,'Endprocess_YoungstRI','Endprocess_YoungstRI','Endprocess_YoungstRI' UNION ALL
        SELECT 419,'Endprocess_RAssessMrk','Endprocess_RAssessMrk','Endprocess_RAssessMrk' UNION ALL
        SELECT 420,'Endprocess_RCorctCAT','Endprocess_RCorctCAT','Endprocess_RCorctCAT' UNION ALL
        SELECT 421,'Endprocess_RIncorect','Endprocess_RIncorect','Endprocess_RIncorect' UNION ALL
        SELECT 422,'Endprocess_RXAssessMrk','Endprocess_RXAssessMrk','Endprocess_RXAssessMrk' UNION ALL
        SELECT 423,'Endprocess_RXCorctCAT','Endprocess_RXCorctCAT','Endprocess_RXCorctCAT' UNION ALL
        SELECT 424,'Endprocess_RXIncorect','Endprocess_RXIncorect','Endprocess_RXIncorect' UNION ALL
        SELECT 168,'Number of cVDPV and WPV cases','Number of cVDPV and WPV cases','Number of cVDPV and WPV cases' UNION ALL
        SELECT 158,'Number of children missed due to all access issues','Number of children missed due to all access issues','Inaccessible Children' UNION ALL
        SELECT 187,'Percent of refusals resolved during the previous month (both during campaigns and in between rounds)','Percent of refusals resolved during the previous month (both during campaigns and in between rounds)','Refusals Conversion' UNION ALL
        SELECT 434,'Reason for inaccessible children - Perception of fear','Reason for inaccessible children - Perception of fear','Perception of fear' UNION ALL
        SELECT 435,'Reason for inaccessible children - Local community not supportive','Reason for inaccessible children - Local community not supportive','Local community not supportive' UNION ALL
        SELECT 436,'Reason for inaccessible children - Crime','Reason for inaccessible children - Crime','Crime' UNION ALL
        SELECT 437,'Reason for inaccessible children - Militant / Anti-Govt Elements','Reason for inaccessible children - Militant / Anti-Govt Elements','Militant / Anti-Govt Elements' UNION ALL
        SELECT 438,'Reason for inaccessible children - Security Operations / Incidents','Reason for inaccessible children - Security Operations / Incidents','Security Operations / Incidents' UNION ALL
        SELECT 439,'Reason for inaccessible children - Management issues','Reason for inaccessible children - Management issues','Management issues' UNION ALL
        SELECT 440,'Reason for inaccessible children - Environment issues','Reason for inaccessible children - Environment issues','Reason for inaccessible children - Environment issues' UNION ALL
        SELECT 441,'Reason for inaccessible children - Political issues','Reason for inaccessible children - Political issues','Political issues' UNION ALL
        SELECT 442,'% Reason for inaccessible children - Perception of fear','% Reason for inaccessible children - Perception of fear','% Perception of fear' UNION ALL
        SELECT 443,'% Reason for inaccessible children - Local community not supportive','% Reason for inaccessible children - Local community not supportive','% Local community not supportive' UNION ALL
        SELECT 444,'% Reason for inaccessible children - Crime','% Reason for inaccessible children - Crime','% Crime' UNION ALL
        SELECT 445,'% Reason for inaccessible children - Militant / Anti-Govt Elements','% Reason for inaccessible children - Militant / Anti-Govt Elements','% Militant / Anti-Govt Elements' UNION ALL
        SELECT 446,'% Reason for inaccessible children - Security Operations / Incidents','% Reason for inaccessible children - Security Operations / Incidents','% Security Operations / Incidents' UNION ALL
        SELECT 447,'% Reason for inaccessible children - Management issues','% Reason for inaccessible children - Management issues','% Management issues' UNION ALL
        SELECT 448,'% Reason for inaccessible children - Environment issues','% Reason for inaccessible children - Environment issues','% Environment issues' UNION ALL
        SELECT 449,'% Reason for inaccessible children - Political issues','% Reason for inaccessible children - Political issues','% Political issues' UNION ALL
        SELECT 451,'Reason for inaccessible children - No reason provided','Reason for inaccessible children - No reason provided','Reason for inaccessible children - No reason provided' UNION ALL
        SELECT 450,'% Reason for inaccessible children - No reason provided','% Reason for inaccessible children - No reason provided','% No reason provided' UNION ALL
        SELECT 431,'Number of non-polio AFP cases with zero doses of OPV','Number of non-polio AFP cases with zero doses of OPV','0 Doses' UNION ALL
        SELECT 432,'Number of non-polio AFP cases with 1-3 doses of OPV','Number of non-polio AFP cases with 1-3 doses of OPV','1–3 Doses' UNION ALL
        SELECT 433,'Number of non-polio AFP cases with 4+ doses of OPV','Number of non-polio AFP cases with 4+ doses of OPV','4+ Doses' UNION ALL
        SELECT 294,'Endprocess_Percent vaccination influencer is vaccinator','Endprocess_Percent vaccination influencer is vaccinator','Vaccinator' UNION ALL
        SELECT 257,'Endprocess_NOimmReas13 - There are other remedies available','Endprocess_NOimmReas13 - There are other remedies available','Other Remedies Avail.' UNION ALL
        SELECT 326,'Endprocess_Pct of children absent due to child at farm','Endprocess_Pct of children absent due to child at farm','Farm' UNION ALL
        SELECT 255,'Endprocess_NOimmReas11 - Polio is rare','Endprocess_NOimmReas11 - Polio is rare','Polio is Rare ' UNION ALL
        SELECT 233,'UNICEF Staffing','Proportion of UNICEF Polio Positions in place at National + State / Province level','Human Resouces' UNION ALL
        SELECT 245,'Routine Immunization Coverage (DPT3 or PENTA3)','Proportion of children 12 months and under in HRDs who have received DPT3 or Penta3','RI Coverage'
        )x;
        -- INDICATOR CALCULATIONS --
            INSERT INTO calculated_indicator_component
            (indicator_id, indicator_component_id, calculation,created_at)
            SELECT *,now() FROM (
            SELECT
                 21 as indicator_id
                ,266 as indicator_component_id
                ,'PART_TO_BE_SUMMED' as calculation
            UNION ALL
            SELECT 21,268,'PART_TO_BE_SUMMED' UNION ALL
            SELECT 21,267,'PART_TO_BE_SUMMED' UNION ALL
            SELECT 21,251,'PART_TO_BE_SUMMED' UNION ALL
            SELECT 21,264,'PART_TO_BE_SUMMED' UNION ALL
            SELECT 24,266,'PART_TO_BE_SUMMED' UNION ALL
            SELECT 24,267,'PART_TO_BE_SUMMED' UNION ALL
            SELECT 158,438,'PART_TO_BE_SUMMED' UNION ALL
            SELECT 158,434,'PART_TO_BE_SUMMED' UNION ALL
            SELECT 158,435,'PART_TO_BE_SUMMED' UNION ALL
            SELECT 158,436,'PART_TO_BE_SUMMED' UNION ALL
            SELECT 158,437,'PART_TO_BE_SUMMED' UNION ALL
            SELECT 158,439,'PART_TO_BE_SUMMED' UNION ALL
            SELECT 158,440,'PART_TO_BE_SUMMED' UNION ALL
            SELECT 158,441,'PART_TO_BE_SUMMED' UNION ALL
            SELECT 158,451,'PART_TO_BE_SUMMED' UNION ALL
            SELECT 164,55,'WHOLE' UNION ALL
            SELECT 164,251,'PART' UNION ALL
            SELECT 165,24,'PART' UNION ALL
            SELECT 165,55,'WHOLE' UNION ALL
            SELECT 166,55,'WHOLE' UNION ALL
            SELECT 166,264,'PART' UNION ALL
            SELECT 167,268,'PART' UNION ALL
            SELECT 167,55,'WHOLE' UNION ALL
            SELECT 168,69,'PART_TO_BE_SUMMED' UNION ALL
            SELECT 168,160,'PART_TO_BE_SUMMED' UNION ALL
            SELECT 168,70,'PART_TO_BE_SUMMED' UNION ALL
            SELECT 169,43,'WHOLE' UNION ALL
            SELECT 169,44,'PART' UNION ALL
            SELECT 172,197,'PART' UNION ALL
            SELECT 172,195,'WHOLE' UNION ALL
            SELECT 173,472,'PART' UNION ALL
            SELECT 173,195,'WHOLE' UNION ALL
            SELECT 174,202,'PART' UNION ALL
            SELECT 174,203,'WHOLE' UNION ALL
            SELECT 174,202,'PART' UNION ALL
            SELECT 174,203,'WHOLE' UNION ALL
            SELECT 178,34,'PART' UNION ALL
            SELECT 178,33,'WHOLE' UNION ALL
            SELECT 179,206,'PART' UNION ALL
            SELECT 179,207,'WHOLE' UNION ALL
            SELECT 180,38,'WHOLE' UNION ALL
            SELECT 180,208,'PART' UNION ALL
            SELECT 184,209,'PART' UNION ALL
            SELECT 184,36,'WHOLE' UNION ALL
            SELECT 185,36,'WHOLE' UNION ALL
            SELECT 185,210,'PART' UNION ALL
            SELECT 187,25,'WHOLE_OF_DIFFERENCE_DENOMINATOR' UNION ALL
            SELECT 187,26,'PART_OF_DIFFERENCE' UNION ALL
            SELECT 187,25,'WHOLE_OF_DIFFERENCE' UNION ALL
            SELECT 189,213,'WHOLE_OF_DIFFERENCE_DENOMINATOR' UNION ALL
            SELECT 189,214,'PART_OF_DIFFERENCE' UNION ALL
            SELECT 189,213,'WHOLE_OF_DIFFERENCE' UNION ALL
            SELECT 191,216,'PART' UNION ALL
            SELECT 191,217,'WHOLE' UNION ALL
            SELECT 194,196,'PART' UNION ALL
            SELECT 194,195,'WHOLE' UNION ALL
            SELECT 219,195,'WHOLE' UNION ALL
            SELECT 219,221,'PART' UNION ALL
            SELECT 222,27,'WHOLE' UNION ALL
            SELECT 222,28,'PART' UNION ALL
            SELECT 224,176,'PART' UNION ALL
            SELECT 224,175,'WHOLE' UNION ALL
            SELECT 226,463,'WHOLE' UNION ALL
            SELECT 226,46,'PART' UNION ALL
            SELECT 228,42,'PART' UNION ALL
            SELECT 228,41,'WHOLE' UNION ALL
            SELECT 230,37,'PART' UNION ALL
            SELECT 230,38,'WHOLE' UNION ALL
            SELECT 233,31,'WHOLE' UNION ALL
            SELECT 233,32,'PART' UNION ALL
            SELECT 239,40,'PART' UNION ALL
            SELECT 239,36,'WHOLE' UNION ALL
            SELECT 245,244,'PART' UNION ALL
            SELECT 245,243,'WHOLE' UNION ALL
            SELECT 251,250,'PART_TO_BE_SUMMED' UNION ALL
            SELECT 251,249,'PART_TO_BE_SUMMED' UNION ALL
            SELECT 251,246,'PART_TO_BE_SUMMED' UNION ALL
            SELECT 251,248,'PART_TO_BE_SUMMED' UNION ALL
            SELECT 251,247,'PART_TO_BE_SUMMED' UNION ALL
            SELECT 264,262,'PART_TO_BE_SUMMED' UNION ALL
            SELECT 264,263,'PART_TO_BE_SUMMED' UNION ALL
            SELECT 264,255,'PART_TO_BE_SUMMED' UNION ALL
            SELECT 264,254,'PART_TO_BE_SUMMED' UNION ALL
            SELECT 264,253,'PART_TO_BE_SUMMED' UNION ALL
            SELECT 264,252,'PART_TO_BE_SUMMED' UNION ALL
            SELECT 264,259,'PART_TO_BE_SUMMED' UNION ALL
            SELECT 264,258,'PART_TO_BE_SUMMED' UNION ALL
            SELECT 264,260,'PART_TO_BE_SUMMED' UNION ALL
            SELECT 264,257,'PART_TO_BE_SUMMED' UNION ALL
            SELECT 264,256,'PART_TO_BE_SUMMED' UNION ALL
            SELECT 264,261,'PART_TO_BE_SUMMED' UNION ALL
            SELECT 265,251,'PART_TO_BE_SUMMED' UNION ALL
            SELECT 265,268,'PART_TO_BE_SUMMED' UNION ALL
            SELECT 265,267,'PART_TO_BE_SUMMED' UNION ALL
            SELECT 265,266,'PART_TO_BE_SUMMED' UNION ALL
            SELECT 265,264,'PART_TO_BE_SUMMED' UNION ALL
            SELECT 271,270,'PART_TO_BE_SUMMED' UNION ALL
            SELECT 271,269,'PART_TO_BE_SUMMED' UNION ALL
            SELECT 272,271,'WHOLE' UNION ALL
            SELECT 272,265,'PART' UNION ALL
            SELECT 274,273,'PART' UNION ALL
            SELECT 274,275,'WHOLE' UNION ALL
            SELECT 276,414,'WHOLE_OF_DIFFERENCE_DENOMINATOR' UNION ALL
            SELECT 276,414,'WHOLE_OF_DIFFERENCE' UNION ALL
            SELECT 276,277,'PART_OF_DIFFERENCE' UNION ALL
            SELECT 286,278,'PART_TO_BE_SUMMED' UNION ALL
            SELECT 286,283,'PART_TO_BE_SUMMED' UNION ALL
            SELECT 286,284,'PART_TO_BE_SUMMED' UNION ALL
            SELECT 286,285,'PART_TO_BE_SUMMED' UNION ALL
            SELECT 286,282,'PART_TO_BE_SUMMED' UNION ALL
            SELECT 286,281,'PART_TO_BE_SUMMED' UNION ALL
            SELECT 286,280,'PART_TO_BE_SUMMED' UNION ALL
            SELECT 286,279,'PART_TO_BE_SUMMED' UNION ALL
            SELECT 287,278,'PART' UNION ALL
            SELECT 287,286,'WHOLE' UNION ALL
            SELECT 288,279,'PART' UNION ALL
            SELECT 288,286,'WHOLE' UNION ALL
            SELECT 289,286,'WHOLE' UNION ALL
            SELECT 289,280,'PART' UNION ALL
            SELECT 290,286,'WHOLE' UNION ALL
            SELECT 290,281,'PART' UNION ALL
            SELECT 291,282,'PART' UNION ALL
            SELECT 291,286,'WHOLE' UNION ALL
            SELECT 292,286,'WHOLE' UNION ALL
            SELECT 292,283,'PART' UNION ALL
            SELECT 293,286,'WHOLE' UNION ALL
            SELECT 293,284,'PART' UNION ALL
            SELECT 294,285,'PART' UNION ALL
            SELECT 294,286,'WHOLE' UNION ALL
            SELECT 306,304,'PART_TO_BE_SUMMED' UNION ALL
            SELECT 306,295,'PART_TO_BE_SUMMED' UNION ALL
            SELECT 306,296,'PART_TO_BE_SUMMED' UNION ALL
            SELECT 306,297,'PART_TO_BE_SUMMED' UNION ALL
            SELECT 306,298,'PART_TO_BE_SUMMED' UNION ALL
            SELECT 306,299,'PART_TO_BE_SUMMED' UNION ALL
            SELECT 306,300,'PART_TO_BE_SUMMED' UNION ALL
            SELECT 306,301,'PART_TO_BE_SUMMED' UNION ALL
            SELECT 306,302,'PART_TO_BE_SUMMED' UNION ALL
            SELECT 306,303,'PART_TO_BE_SUMMED' UNION ALL
            SELECT 306,305,'PART_TO_BE_SUMMED' UNION ALL
            SELECT 307,295,'PART' UNION ALL
            SELECT 307,306,'WHOLE' UNION ALL
            SELECT 308,306,'WHOLE' UNION ALL
            SELECT 308,299,'PART' UNION ALL
            SELECT 309,306,'WHOLE' UNION ALL
            SELECT 309,303,'PART' UNION ALL
            SELECT 310,296,'PART' UNION ALL
            SELECT 310,306,'WHOLE' UNION ALL
            SELECT 311,306,'WHOLE' UNION ALL
            SELECT 311,300,'PART' UNION ALL
            SELECT 312,306,'WHOLE' UNION ALL
            SELECT 312,304,'PART' UNION ALL
            SELECT 313,297,'PART' UNION ALL
            SELECT 313,306,'WHOLE' UNION ALL
            SELECT 314,301,'PART' UNION ALL
            SELECT 314,306,'WHOLE' UNION ALL
            SELECT 315,305,'PART' UNION ALL
            SELECT 315,306,'WHOLE' UNION ALL
            SELECT 316,298,'PART' UNION ALL
            SELECT 316,306,'WHOLE' UNION ALL
            SELECT 317,302,'PART' UNION ALL
            SELECT 317,306,'WHOLE' UNION ALL
            SELECT 318,267,'PART' UNION ALL
            SELECT 318,265,'WHOLE' UNION ALL
            SELECT 319,268,'PART' UNION ALL
            SELECT 319,265,'WHOLE' UNION ALL
            SELECT 320,251,'PART' UNION ALL
            SELECT 320,265,'WHOLE' UNION ALL
            SELECT 321,264,'PART' UNION ALL
            SELECT 321,265,'WHOLE' UNION ALL
            SELECT 322,266,'PART' UNION ALL
            SELECT 322,265,'WHOLE' UNION ALL
            SELECT 323,246,'PART' UNION ALL
            SELECT 323,251,'WHOLE' UNION ALL
            SELECT 324,247,'PART' UNION ALL
            SELECT 324,251,'WHOLE' UNION ALL
            SELECT 325,248,'PART' UNION ALL
            SELECT 325,251,'WHOLE' UNION ALL
            SELECT 326,249,'PART' UNION ALL
            SELECT 326,251,'WHOLE' UNION ALL
            SELECT 327,251,'WHOLE' UNION ALL
            SELECT 327,250,'PART' UNION ALL
            SELECT 328,252,'PART' UNION ALL
            SELECT 328,264,'WHOLE' UNION ALL
            SELECT 329,255,'PART' UNION ALL
            SELECT 329,264,'WHOLE' UNION ALL
            SELECT 330,264,'WHOLE' UNION ALL
            SELECT 330,258,'PART' UNION ALL
            SELECT 331,261,'PART' UNION ALL
            SELECT 331,264,'WHOLE' UNION ALL
            SELECT 332,253,'PART' UNION ALL
            SELECT 332,264,'WHOLE' UNION ALL
            SELECT 333,264,'WHOLE' UNION ALL
            SELECT 333,256,'PART' UNION ALL
            SELECT 334,264,'WHOLE' UNION ALL
            SELECT 334,259,'PART' UNION ALL
            SELECT 335,254,'PART' UNION ALL
            SELECT 335,264,'WHOLE' UNION ALL
            SELECT 336,264,'WHOLE' UNION ALL
            SELECT 336,257,'PART' UNION ALL
            SELECT 337,264,'WHOLE' UNION ALL
            SELECT 337,260,'PART' UNION ALL
            SELECT 338,264,'WHOLE' UNION ALL
            SELECT 338,263,'PART' UNION ALL
            SELECT 339,262,'PART' UNION ALL
            SELECT 339,264,'WHOLE' UNION ALL
            SELECT 345,344,'WHOLE' UNION ALL
            SELECT 345,340,'PART' UNION ALL
            SELECT 346,341,'PART' UNION ALL
            SELECT 346,344,'WHOLE' UNION ALL
            SELECT 347,342,'PART' UNION ALL
            SELECT 347,344,'WHOLE' UNION ALL
            SELECT 348,343,'PART' UNION ALL
            SELECT 348,344,'WHOLE' UNION ALL
            SELECT 442,158,'WHOLE' UNION ALL
            SELECT 442,434,'PART' UNION ALL
            SELECT 443,435,'PART' UNION ALL
            SELECT 443,158,'WHOLE' UNION ALL
            SELECT 444,158,'WHOLE' UNION ALL
            SELECT 444,436,'PART' UNION ALL
            SELECT 445,158,'WHOLE' UNION ALL
            SELECT 445,437,'PART' UNION ALL
            SELECT 446,438,'PART' UNION ALL
            SELECT 446,158,'WHOLE' UNION ALL
            SELECT 447,439,'PART' UNION ALL
            SELECT 447,158,'WHOLE' UNION ALL
            SELECT 448,440,'PART' UNION ALL
            SELECT 448,158,'WHOLE' UNION ALL
            SELECT 449,158,'WHOLE' UNION ALL
            SELECT 449,441,'PART' UNION ALL
            SELECT 450,158,'WHOLE' UNION ALL
            SELECT 450,451,'PART' UNION ALL
            SELECT 461,204,'WHOLE' UNION ALL
            SELECT 461,176,'PART' UNION ALL
            SELECT 470,439,'PART_TO_BE_SUMMED' UNION ALL
            SELECT 470,441,'PART_TO_BE_SUMMED' UNION ALL
            SELECT 470,451,'PART_TO_BE_SUMMED' UNION ALL
            SELECT 470,438,'PART_TO_BE_SUMMED' UNION ALL
            SELECT 470,437,'PART_TO_BE_SUMMED' UNION ALL
            SELECT 470,436,'PART_TO_BE_SUMMED' UNION ALL
            SELECT 470,435,'PART_TO_BE_SUMMED' UNION ALL
            SELECT 470,434,'PART_TO_BE_SUMMED' UNION ALL
            SELECT 470,440,'PART_TO_BE_SUMMED' UNION ALL
            SELECT 475,55,'WHOLE' UNION ALL
            SELECT 475,21,'PART'
            )x;


    INSERT INTO indicator_tag
        (id, tag_name)
        SELECT 34,'Management Indicators' UNION ALL
        SELECT 1,'WHO Independent Monitoring' UNION ALL
        SELECT 2,'Nigeria ODK Data';
        INSERT INTO indicator_tag
        (id, tag_name, parent_tag_id)
        SELECT 65,'Cold Chain',42 UNION ALL
        SELECT 66,'Vaccine Management',42 UNION ALL
        SELECT 63,'Funding',41 UNION ALL
        SELECT 64,'Human Resources',41 UNION ALL
        SELECT 58,'Convergence',40 UNION ALL
        SELECT 59,'RI Coverage',40 UNION ALL
        SELECT 60,'RI Defaulter',40 UNION ALL
        SELECT 61,'RI Knowledge',40 UNION ALL
        SELECT 62,'RI Stock',40 UNION ALL
        SELECT 56,'Epidemiology',39 UNION ALL
        SELECT 57,'Under Immunity',39 UNION ALL
        SELECT 52,'Absences',38 UNION ALL
        SELECT 53,'Refusals',38 UNION ALL
        SELECT 54,'Awareness',38 UNION ALL
        SELECT 55,'Microplan',38 UNION ALL
        SELECT 47,'Motivation',37 UNION ALL
        SELECT 48,'Presence',37 UNION ALL
        SELECT 49,'Profile',37 UNION ALL
        SELECT 50,'Skills',37 UNION ALL
        SELECT 51,'Supervision',37 UNION ALL
        SELECT 46,'Missed Children by Reason',36 UNION ALL
        SELECT 43,'Access Approach',35 UNION ALL
        SELECT 44,'Inaccessible Children',35 UNION ALL
        SELECT 45,'Transit Point',35 UNION ALL
        SELECT 35,'Access',34 UNION ALL
        SELECT 36,'Coverage',34 UNION ALL
        SELECT 37,'FLW Capacity',34 UNION ALL
        SELECT 38,'FLW Performance',34 UNION ALL
        SELECT 39,'Impact',34 UNION ALL
        SELECT 40,'Polio+',34 UNION ALL
        SELECT 41,'Resources',34 UNION ALL
        SELECT 42,'Supply',34 UNION ALL
        SELECT 11,'KAP: Campaign Awareness',7 UNION ALL
        SELECT 12,'Missed Children: Missed',7 UNION ALL
        SELECT 13,'Missed Children: Seen',7 UNION ALL
        SELECT 14,'Missed Children: Unimmunized',7 UNION ALL
        SELECT 15,'Missed Children: Operations',7 UNION ALL
        SELECT 16,'Missed Children: Immunized',7 UNION ALL
        SELECT 17,'KAP: Source',7 UNION ALL
        SELECT 18,'KAP: Influence',7 UNION ALL
        SELECT 19,'Survey',7 UNION ALL
        SELECT 20,'Missed Children: Absence',7 UNION ALL
        SELECT 21,'Missed Children: Reasons',7 UNION ALL
        SELECT 22,'Missed Children: Refusal',7 UNION ALL
        SELECT 23,'Missed Children: Security',7 UNION ALL
        SELECT 3,'Newborn',2 UNION ALL
        SELECT 4,'Census',2 UNION ALL
        SELECT 8,'Missed Children',2 UNION ALL
        SELECT 9,'Campaign',2 UNION ALL
        SELECT 10,'Group',2 UNION ALL
        SELECT 5,'Outside',1 UNION ALL
        SELECT 6,'Redo',1 UNION ALL
        SELECT 7,'End Process',1;
        INSERT INTO indicator_to_tag
        (indicator_id, indicator_tag_id)
        SELECT 174,43 UNION ALL
        SELECT 201,43 UNION ALL
        SELECT 202,43 UNION ALL
        SELECT 203,43 UNION ALL
        SELECT 158,44 UNION ALL
        SELECT 434,44 UNION ALL
        SELECT 435,44 UNION ALL
        SELECT 436,44 UNION ALL
        SELECT 437,44 UNION ALL
        SELECT 438,44 UNION ALL
        SELECT 439,44 UNION ALL
        SELECT 440,44 UNION ALL
        SELECT 441,44 UNION ALL
        SELECT 442,44 UNION ALL
        SELECT 443,44 UNION ALL
        SELECT 444,44 UNION ALL
        SELECT 445,44 UNION ALL
        SELECT 446,44 UNION ALL
        SELECT 447,44 UNION ALL
        SELECT 448,44 UNION ALL
        SELECT 449,44 UNION ALL
        SELECT 450,44 UNION ALL
        SELECT 451,44 UNION ALL
        SELECT 175,45 UNION ALL
        SELECT 176,45 UNION ALL
        SELECT 177,45 UNION ALL
        SELECT 204,45 UNION ALL
        SELECT 224,45 UNION ALL
        SELECT 461,45 UNION ALL
        SELECT 21,46 UNION ALL
        SELECT 24,46 UNION ALL
        SELECT 55,46 UNION ALL
        SELECT 164,46 UNION ALL
        SELECT 165,46 UNION ALL
        SELECT 166,46 UNION ALL
        SELECT 167,46 UNION ALL
        SELECT 475,46 UNION ALL
        SELECT 46,47 UNION ALL
        SELECT 226,47 UNION ALL
        SELECT 463,47 UNION ALL
        SELECT 33,48 UNION ALL
        SELECT 34,48 UNION ALL
        SELECT 35,48 UNION ALL
        SELECT 178,48 UNION ALL
        SELECT 179,48 UNION ALL
        SELECT 206,48 UNION ALL
        SELECT 207,48 UNION ALL
        SELECT 37,49 UNION ALL
        SELECT 38,49 UNION ALL
        SELECT 40,49 UNION ALL
        SELECT 180,49 UNION ALL
        SELECT 208,49 UNION ALL
        SELECT 230,49 UNION ALL
        SELECT 239,49 UNION ALL
        SELECT 36,50 UNION ALL
        SELECT 41,50 UNION ALL
        SELECT 42,50 UNION ALL
        SELECT 49,50 UNION ALL
        SELECT 184,50 UNION ALL
        SELECT 209,50 UNION ALL
        SELECT 228,50 UNION ALL
        SELECT 185,51 UNION ALL
        SELECT 210,51 UNION ALL
        SELECT 189,52 UNION ALL
        SELECT 213,52 UNION ALL
        SELECT 214,52 UNION ALL
        SELECT 215,52 UNION ALL
        SELECT 25,53 UNION ALL
        SELECT 26,53 UNION ALL
        SELECT 187,53 UNION ALL
        SELECT 211,53 UNION ALL
        SELECT 29,54 UNION ALL
        SELECT 30,54 UNION ALL
        SELECT 27,55 UNION ALL
        SELECT 28,55 UNION ALL
        SELECT 222,55 UNION ALL
        SELECT 1,56 UNION ALL
        SELECT 69,56 UNION ALL
        SELECT 70,56 UNION ALL
        SELECT 159,56 UNION ALL
        SELECT 160,56 UNION ALL
        SELECT 431,57 UNION ALL
        SELECT 432,57 UNION ALL
        SELECT 433,57 UNION ALL
        SELECT 193,58 UNION ALL
        SELECT 218,58 UNION ALL
        SELECT 243,59 UNION ALL
        SELECT 244,59 UNION ALL
        SELECT 245,59 UNION ALL
        SELECT 192,60 UNION ALL
        SELECT 236,61 UNION ALL
        SELECT 191,62 UNION ALL
        SELECT 216,62 UNION ALL
        SELECT 217,62 UNION ALL
        SELECT 43,63 UNION ALL
        SELECT 44,63 UNION ALL
        SELECT 169,63 UNION ALL
        SELECT 31,64 UNION ALL
        SELECT 32,64 UNION ALL
        SELECT 233,64 UNION ALL
        SELECT 173,65 UNION ALL
        SELECT 198,65 UNION ALL
        SELECT 199,65 UNION ALL
        SELECT 472,65 UNION ALL
        SELECT 5,66 UNION ALL
        SELECT 51,66 UNION ALL
        SELECT 172,66 UNION ALL
        SELECT 194,66 UNION ALL
        SELECT 195,66 UNION ALL
        SELECT 196,66 UNION ALL
        SELECT 197,66 UNION ALL
        SELECT 219,66 UNION ALL
        SELECT 220,66 UNION ALL
        SELECT 221,66 UNION ALL
        SELECT 264,46 UNION ALL
        SELECT 251,46 UNION ALL
        SELECT 268,46 UNION ALL
        SELECT 349,11 UNION ALL
        SELECT 414,11 UNION ALL
        SELECT 277,11 UNION ALL
        SELECT 276,11 UNION ALL
        SELECT 286,18 UNION ALL
        SELECT 278,18 UNION ALL
        SELECT 280,18 UNION ALL
        SELECT 282,18 UNION ALL
        SELECT 284,18 UNION ALL
        SELECT 279,18 UNION ALL
        SELECT 281,18 UNION ALL
        SELECT 283,18 UNION ALL
        SELECT 285,18 UNION ALL
        SELECT 292,18 UNION ALL
        SELECT 289,18 UNION ALL
        SELECT 290,18 UNION ALL
        SELECT 287,18 UNION ALL
        SELECT 288,18 UNION ALL
        SELECT 293,18 UNION ALL
        SELECT 291,18 UNION ALL
        SELECT 294,18 UNION ALL
        SELECT 306,17 UNION ALL
        SELECT 317,17 UNION ALL
        SELECT 315,17 UNION ALL
        SELECT 312,17 UNION ALL
        SELECT 308,17 UNION ALL
        SELECT 311,17 UNION ALL
        SELECT 314,17 UNION ALL
        SELECT 310,17 UNION ALL
        SELECT 309,17 UNION ALL
        SELECT 316,17 UNION ALL
        SELECT 307,17 UNION ALL
        SELECT 313,17 UNION ALL
        SELECT 302,17 UNION ALL
        SELECT 305,17 UNION ALL
        SELECT 304,17 UNION ALL
        SELECT 299,17 UNION ALL
        SELECT 300,17 UNION ALL
        SELECT 301,17 UNION ALL
        SELECT 296,17 UNION ALL
        SELECT 303,17 UNION ALL
        SELECT 298,17 UNION ALL
        SELECT 295,17 UNION ALL
        SELECT 297,17 UNION ALL
        SELECT 246,20 UNION ALL
        SELECT 247,20 UNION ALL
        SELECT 248,20 UNION ALL
        SELECT 249,20 UNION ALL
        SELECT 250,20 UNION ALL
        SELECT 320,20 UNION ALL
        SELECT 326,20 UNION ALL
        SELECT 325,20 UNION ALL
        SELECT 327,20 UNION ALL
        SELECT 324,20 UNION ALL
        SELECT 323,20 UNION ALL
        SELECT 251,20 UNION ALL
        SELECT 269,16 UNION ALL
        SELECT 272,12 UNION ALL
        SELECT 267,15 UNION ALL
        SELECT 268,15 UNION ALL
        SELECT 319,15 UNION ALL
        SELECT 318,15 UNION ALL
        SELECT 265,21 UNION ALL
        SELECT 254,22 UNION ALL
        SELECT 255,22 UNION ALL
        SELECT 256,22 UNION ALL
        SELECT 257,22 UNION ALL
        SELECT 258,22 UNION ALL
        SELECT 259,22 UNION ALL
        SELECT 260,22 UNION ALL
        SELECT 261,22 UNION ALL
        SELECT 262,22 UNION ALL
        SELECT 263,22 UNION ALL
        SELECT 252,22 UNION ALL
        SELECT 253,22 UNION ALL
        SELECT 321,22 UNION ALL
        SELECT 328,22 UNION ALL
        SELECT 335,22 UNION ALL
        SELECT 338,22 UNION ALL
        SELECT 339,22 UNION ALL
        SELECT 331,22 UNION ALL
        SELECT 336,22 UNION ALL
        SELECT 333,22 UNION ALL
        SELECT 329,22 UNION ALL
        SELECT 334,22 UNION ALL
        SELECT 330,22 UNION ALL
        SELECT 332,22 UNION ALL
        SELECT 337,22 UNION ALL
        SELECT 264,22 UNION ALL
        SELECT 266,23 UNION ALL
        SELECT 322,23 UNION ALL
        SELECT 271,13 UNION ALL
        SELECT 270,14 UNION ALL
        SELECT 415,19 UNION ALL
        SELECT 416,19 UNION ALL
        SELECT 401,5 UNION ALL
        SELECT 400,5 UNION ALL
        SELECT 403,5 UNION ALL
        SELECT 402,5 UNION ALL
        SELECT 405,5 UNION ALL
        SELECT 404,5 UNION ALL
        SELECT 391,5 UNION ALL
        SELECT 274,5 UNION ALL
        SELECT 396,5 UNION ALL
        SELECT 397,5 UNION ALL
        SELECT 393,5 UNION ALL
        SELECT 409,5 UNION ALL
        SELECT 412,5 UNION ALL
        SELECT 413,5 UNION ALL
        SELECT 273,5 UNION ALL
        SELECT 407,5 UNION ALL
        SELECT 406,5 UNION ALL
        SELECT 394,5 UNION ALL
        SELECT 395,5 UNION ALL
        SELECT 392,5 UNION ALL
        SELECT 410,5 UNION ALL
        SELECT 411,5 UNION ALL
        SELECT 408,5 UNION ALL
        SELECT 398,5 UNION ALL
        SELECT 275,5 UNION ALL
        SELECT 399,5 UNION ALL
        SELECT 354,6 UNION ALL
        SELECT 373,6 UNION ALL
        SELECT 384,6 UNION ALL
        SELECT 360,6 UNION ALL
        SELECT 361,6 UNION ALL
        SELECT 362,6 UNION ALL
        SELECT 363,6 UNION ALL
        SELECT 364,6 UNION ALL
        SELECT 356,6 UNION ALL
        SELECT 357,6 UNION ALL
        SELECT 358,6 UNION ALL
        SELECT 359,6 UNION ALL
        SELECT 371,6 UNION ALL
        SELECT 355,6 UNION ALL
        SELECT 370,6 UNION ALL
        SELECT 374,6 UNION ALL
        SELECT 385,6 UNION ALL
        SELECT 386,6 UNION ALL
        SELECT 341,6 UNION ALL
        SELECT 343,6 UNION ALL
        SELECT 342,6 UNION ALL
        SELECT 340,6 UNION ALL
        SELECT 344,6 UNION ALL
        SELECT 350,6 UNION ALL
        SELECT 352,6 UNION ALL
        SELECT 351,6 UNION ALL
        SELECT 366,6 UNION ALL
        SELECT 367,6 UNION ALL
        SELECT 369,6 UNION ALL
        SELECT 346,6 UNION ALL
        SELECT 348,6 UNION ALL
        SELECT 347,6 UNION ALL
        SELECT 345,6 UNION ALL
        SELECT 379,6 UNION ALL
        SELECT 377,6 UNION ALL
        SELECT 381,6 UNION ALL
        SELECT 376,6 UNION ALL
        SELECT 378,6 UNION ALL
        SELECT 380,6 UNION ALL
        SELECT 353,6 UNION ALL
        SELECT 365,6 UNION ALL
        SELECT 368,6 UNION ALL
        SELECT 372,6 UNION ALL
        SELECT 375,6 UNION ALL
        SELECT 382,6 UNION ALL
        SELECT 383,6 UNION ALL
        SELECT 387,6 UNION ALL
        SELECT 388,6 UNION ALL
        SELECT 390,6 UNION ALL
        SELECT 91,4 UNION ALL
        SELECT 74,9 UNION ALL
        SELECT 88,9 UNION ALL
        SELECT 79,9 UNION ALL
        SELECT 80,9 UNION ALL
        SELECT 86,9 UNION ALL
        SELECT 77,9 UNION ALL
        SELECT 78,9 UNION ALL
        SELECT 87,4 UNION ALL
        SELECT 85,4 UNION ALL
        SELECT 84,4 UNION ALL
        SELECT 93,4 UNION ALL
        SELECT 94,4 UNION ALL
        SELECT 75,4 UNION ALL
        SELECT 92,4 UNION ALL
        SELECT 90,4 UNION ALL
        SELECT 76,8 UNION ALL
        SELECT 103,8 UNION ALL
        SELECT 102,8 UNION ALL
        SELECT 99,8 UNION ALL
        SELECT 98,8 UNION ALL
        SELECT 124,8 UNION ALL
        SELECT 123,8 UNION ALL
        SELECT 113,8 UNION ALL
        SELECT 114,8 UNION ALL
        SELECT 97,8 UNION ALL
        SELECT 96,8 UNION ALL
        SELECT 116,8 UNION ALL
        SELECT 115,8 UNION ALL
        SELECT 100,8 UNION ALL
        SELECT 101,8 UNION ALL
        SELECT 130,8 UNION ALL
        SELECT 131,8 UNION ALL
        SELECT 120,8 UNION ALL
        SELECT 121,8 UNION ALL
        SELECT 138,8 UNION ALL
        SELECT 139,8 UNION ALL
        SELECT 118,8 UNION ALL
        SELECT 117,8 UNION ALL
        SELECT 146,8 UNION ALL
        SELECT 145,8 UNION ALL
        SELECT 106,8 UNION ALL
        SELECT 105,8 UNION ALL
        SELECT 147,8 UNION ALL
        SELECT 148,8 UNION ALL
        SELECT 132,8 UNION ALL
        SELECT 133,8 UNION ALL
        SELECT 143,8 UNION ALL
        SELECT 142,8 UNION ALL
        SELECT 119,8 UNION ALL
        SELECT 122,8 UNION ALL
        SELECT 108,8 UNION ALL
        SELECT 107,8 UNION ALL
        SELECT 128,8 UNION ALL
        SELECT 129,8 UNION ALL
        SELECT 110,8 UNION ALL
        SELECT 109,8 UNION ALL
        SELECT 140,8 UNION ALL
        SELECT 141,8 UNION ALL
        SELECT 137,8 UNION ALL
        SELECT 136,8 UNION ALL
        SELECT 83,3 UNION ALL
        SELECT 89,3 UNION ALL
        SELECT 82,3 UNION ALL
        SELECT 81,3 UNION ALL
        SELECT 112,10 UNION ALL
        SELECT 111,10 UNION ALL
        SELECT 127,10 UNION ALL
        SELECT 126,10 UNION ALL
        SELECT 149,10 UNION ALL
        SELECT 104,10 UNION ALL
        SELECT 134,10 UNION ALL
        SELECT 125,10 UNION ALL
        SELECT 150,10 UNION ALL
        SELECT 151,10 UNION ALL
        SELECT 144,10 UNION ALL
        SELECT 152,10 UNION ALL
        SELECT 135,10 UNION ALL
        SELECT 95,10;


        -- CAMPAIGNS --

        INSERT INTO campaign
        (id, start_date,end_date,slug,campaign_type_id, office_id, created_at)

        -- to do this in excel... :) --
        -- CONCATENATE("SELECT ",A1,",'",TEXT(B1,"mm/dd/yy"),"','",TEXT(B1,"mm/dd/yy"),"','",D1,"' UNION ALL")

        SELECT id, CAST(x.start_date AS DATE),CAST(x.end_date as date),x.slug, 1,1,now() FROM (
        SELECT 99 as id,'11/01/13' as start_date,'11/01/13' as end_date,'nigeria-november-2013'  as slug UNION ALL
        SELECT 101,'09/01/13','09/01/13','nigeria-september-2013' UNION ALL
        SELECT 102,'03/01/12','03/01/12','nigeria-march-2012' UNION ALL
        SELECT 103,'06/01/12','06/01/12','nigeria-june-2012' UNION ALL
        SELECT 104,'08/01/14','08/01/14','nigeria-august-2014' UNION ALL
        SELECT 105,'03/01/13','03/01/13','nigeria-march-2013' UNION ALL
        SELECT 106,'10/01/13','10/01/13','nigeria-october-2013' UNION ALL
        SELECT 107,'05/01/13','05/01/13','nigeria-may-2013' UNION ALL
        SELECT 108,'03/01/14','03/01/14','nigeria-march-2014' UNION ALL
        SELECT 109,'02/01/13','02/01/13','nigeria-february-2013' UNION ALL
        SELECT 110,'12/01/12','12/01/12','nigeria-december-2012' UNION ALL
        SELECT 111,'06/01/14','06/01/14','nigeria-june-2014' UNION ALL
        SELECT 112,'12/01/13','12/01/13','nigeria-december-2013' UNION ALL
        SELECT 113,'09/01/12','09/01/12','nigeria-september-2012' UNION ALL
        SELECT 114,'04/01/13','04/01/13','nigeria-april-2013' UNION ALL
        SELECT 115,'04/01/14','04/01/14','nigeria-april-2014' UNION ALL
        SELECT 116,'06/01/13','06/01/13','nigeria-june-2013' UNION ALL
        SELECT 117,'01/01/14','01/01/14','nigeria-january-2014' UNION ALL
        SELECT 118,'01/01/12','01/01/12','nigeria-january-2012' UNION ALL
        SELECT 119,'08/01/12','08/01/12','nigeria-august-2012' UNION ALL
        SELECT 120,'01/01/13','01/01/13','nigeria-january-2013' UNION ALL
        SELECT 121,'10/01/12','10/01/12','nigeria-october-2012' UNION ALL
        SELECT 122,'10/01/14','10/01/14','nigeria-october-2014' UNION ALL
        SELECT 123,'08/01/13','08/01/13','nigeria-august-2013' UNION ALL
        SELECT 124,'07/01/14','07/01/14','nigeria-july-2014' UNION ALL
        SELECT 125,'05/01/14','05/01/14','nigeria-may-2014' UNION ALL
        SELECT 126,'11/01/12','11/01/12','nigeria-november-2012' UNION ALL
        SELECT 127,'07/01/12','07/01/12','nigeria-july-2012' UNION ALL
        SELECT 128,'09/01/14','09/01/14','nigeria-september-2014' UNION ALL
        SELECT 129,'04/01/12','04/01/12','nigeria-april-2012' UNION ALL
        SELECT 130,'02/01/14','02/01/14','nigeria-february-2014' UNION ALL
        SELECT 131,'07/01/13','07/01/13','nigeria-july-2013' UNION ALL
        SELECT 132,'05/01/12','05/01/12','nigeria-may-2012' UNION ALL
        SELECT 100,'11/01/14','11/01/14','nigeria-november-2014' UNION ALL
        SELECT 201,'12/01/14','12/01/14','nigeria-2014-12-01' UNION ALL
        SELECT 210,'01/01/15','01/01/15','nigeria-2015-01-01' UNION ALL
        SELECT 211,'02/01/15','02/01/15','nigeria-2015-02-01' UNION ALL
        SELECT 212,'03/01/15','03/01/15','nigeria-2015-03-01' UNION ALL
        SELECT 216,'02/01/12','02/01/12','nigeria-2012-02-01' UNION ALL
        SELECT 221,'04/01/15','04/01/15','nigeria-2015-04-01' UNION ALL
        SELECT 222,'05/01/15','05/01/15','nigeria-2015-05-01' UNION ALL
        SELECT 223,'06/01/15','06/01/15','nigeria-2015-06-01'

        )x;

        -- source_object_map --
        INSERT INTO source_object_map
        (master_object_id, source_object_code, content_type, mapped_by_id)

        SELECT *,1 FROM (
        SELECT * FROM (
        SELECT 32 as master_object_id ,'Number of Unicef polio positions in their posts in PBR-approved structures'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 31 as master_object_id ,'Target number of Unicef polio positions in PBR-approved structures'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 24 as master_object_id ,'Number of children missed due to other reasons'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 25 as master_object_id ,'Number of refusals before re-visit'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 26 as master_object_id ,'Number of refusals after re-visit'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 35 as master_object_id ,'Number of target social mobilizers'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 40 as master_object_id ,'Number of female social mobilizers'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 67 as master_object_id ,'Percentage of States/Regions with OPV supply arriving at state/region level in sufficient time before campaign'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 418 as master_object_id ,'YoungstRI'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 420 as master_object_id ,'RCorctCAT'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 417 as master_object_id ,'TotalYoungest'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 421 as master_object_id ,'RIncorect'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 415 as master_object_id ,'HHvisitedTEAMS'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 423 as master_object_id ,'RXCorctCAT'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 422 as master_object_id ,'RXAssessMrk'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 424 as master_object_id ,'RXIncorect'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 269 as master_object_id ,'Sum of Marked0to59'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 270 as master_object_id ,'Sum of UnImmun0to59'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 38 as master_object_id ,'TOTAL teams Checked'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 34 as master_object_id ,'# HR areas (Clusters) with social mobilizers'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 35 as master_object_id ,' # target social mobilizers'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 29 as master_object_id ,'# caregivers'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 25 as master_object_id ,'# refusals before re-visit'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 28 as master_object_id ,'# Microplans incoroporating social data'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 44 as master_object_id ,'Amount committed'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 53 as master_object_id ,'# districts having NO stock-outs of OPV'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 37 as master_object_id ,'# teams w/ at least one female worker'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 38 as master_object_id ,'# teams'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 62 as master_object_id ,'# w/ capacity'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 33 as master_object_id ,' # of HR areas (clusters) targeted  '  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 27 as master_object_id ,'# Microplans in LPD'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 24 as master_object_id ,'Other reasons'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 26 as master_object_id ,'# refusals after re-visit'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 40 as master_object_id ,'# female social mobilizers'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 55 as master_object_id ,'# of targeted under-five children'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 43 as master_object_id ,'Amount TOTAL FRR funds'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 36 as master_object_id ,'# in place'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 5 as master_object_id ,'# vaccine doses used'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 34 as master_object_id ,'# HR areas with social mobilizers'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 32 as master_object_id ,'Number of core polio communication personnel in place in a country programme'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 27 as master_object_id ,'# Microplans in High Risk District'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 41 as master_object_id ,'# front line workers'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 31 as master_object_id ,'Target number of core polio personnel in place in a country programme'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 93 as master_object_id ,'CensusNewBornsF'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 49 as master_object_id ,'# trained on RI in past 6 mos.'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 51 as master_object_id ,'# children vaccined'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 41 as master_object_id ,' # front line workers'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 31 as master_object_id ,'Target core polio personnel in place in a country programme'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 30 as master_object_id ,'# aware'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 33 as master_object_id ,' # of HR areas targeted  '  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 35 as master_object_id ,'Total # of targetted social mobilizers'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 35 as master_object_id ,'# target social mobilizers'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 49 as master_object_id ,'# trained on RI in past 6 months.'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 31 as master_object_id ,'Target core polio communication personnel in place in a country programme'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 38 as master_object_id ,' # teams'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 42 as master_object_id ,'# workers w/ IPC skills'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 32 as master_object_id ,'Number of core polio personnel in place in a country programme'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 94 as master_object_id ,'CensusNewBornsM'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 62 as master_object_id ,'# health facilities w/ capacity'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 83 as master_object_id ,'Tot_Newborns'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 46 as master_object_id ,'# received payment timely'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 62 as master_object_id ,'% w/ capacity'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 85 as master_object_id ,'Census2_11MoF'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 31 as master_object_id ,'Target # of core polio communication'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 84 as master_object_id ,'Census2_11MoM'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 32 as master_object_id ,'# of core polio communication personnel in place'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 33 as master_object_id ,'# of HR areas targeted'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 69 as master_object_id ,'Number of cases of cVDPV2'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 162 as master_object_id ,'Number of cases of iVDPV2'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 70 as master_object_id ,'Number of cases of WPV1'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 160 as master_object_id ,'Number of cases of WPV3'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 159 as master_object_id ,'Number of cases of aVDPV2'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 161 as master_object_id ,'Number of cases of WPV1WPV3'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 31 as master_object_id ,'Target number of core polio communications in place'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 40 as master_object_id ,'Number of social mobilisers who are female'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 38 as master_object_id ,'# of teams'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 90 as master_object_id ,'Tot_2_11Months'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 31 as master_object_id ,'Target number of core polio communication positions'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 28 as master_object_id ,'# Microplans incorporating social data'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 32 as master_object_id ,'# of core polio communication in place'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 35 as master_object_id ,'Target number of social mobilisers'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 21 as master_object_id ,'All missed children'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 46 as master_object_id ,'Number of social mobilisers who were paid on time'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 91 as master_object_id ,'Census12_59MoF'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 36 as master_object_id ,'Number of social mobilisers in place'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 56 as master_object_id ,'# of subregional units'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 31 as master_object_id ,'Target # of core polio communication '  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 46 as master_object_id ,'Number of social mobilizers who were paid on time'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 46 as master_object_id ,'Number of social mobilizers paid on time'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 36 as master_object_id ,'Number of social mobilizers in place'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 43 as master_object_id ,'Amount FRR'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 46 as master_object_id ,'# of social mobilizers who received payment on time'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 67 as master_object_id ,'% with OPV arriving in sufficient time'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 51 as master_object_id ,'# of children vaccined'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 35 as master_object_id ,'Target # of social mobilizers'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 36 as master_object_id ,'# of social mobilizers in place'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 34 as master_object_id ,'# of HR areas with social mobilizers'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 57 as master_object_id ,'# of subregional units where OPV arrived in sufficient time'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 87 as master_object_id ,'Census12_59MoM'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 46 as master_object_id ,'# of social mobilizers paid on time'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 40 as master_object_id ,'# of female social mobilizers'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 35 as master_object_id ,'Target number of social mobilizers'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 37 as master_object_id ,'# polio teams w/ at least one female worker'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 263 as master_object_id ,'NOimmReas19'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 92 as master_object_id ,'Tot_12_59Months'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 416 as master_object_id ,'ZeroDose'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 257 as master_object_id ,'NOimmReas13'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 256 as master_object_id ,'NOimmReas12'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 255 as master_object_id ,'NOimmReas11'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 254 as master_object_id ,'NOimmReas10'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 261 as master_object_id ,'NOimmReas17'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 260 as master_object_id ,'NOimmReas16'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 295 as master_object_id ,'STannounc'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 270 as master_object_id ,'UnImmun0to59'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 246 as master_object_id ,'NOimmReas3'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 268 as master_object_id ,'NOimmReas2'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 267 as master_object_id ,'NOimmReas1'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 250 as master_object_id ,'NOimmReas7'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 249 as master_object_id ,'NOimmReas6'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 75 as master_object_id ,'Tot_Census'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 247 as master_object_id ,'NOimmReas4'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 262 as master_object_id ,'NOimmReas18'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 82 as master_object_id ,'VaxNewBornsF'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 81 as master_object_id ,'VaxNewBornsM'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 296 as master_object_id ,'SRadio'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 89 as master_object_id ,'Tot_VaxNewBorn'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 299 as master_object_id ,'SMosque'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 298 as master_object_id ,'SReiliglead'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 303 as master_object_id ,'SRelative'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 297 as master_object_id ,'STradlead'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 77 as master_object_id ,'Vax2_11MoF'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 302 as master_object_id ,'Sbanner'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 305 as master_object_id ,'Scommmob'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 277 as master_object_id ,'SNOTAWARE'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 266 as master_object_id ,'NOimmReas20'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 248 as master_object_id ,'NOimmReas5'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 300 as master_object_id ,'SNewspaper'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 78 as master_object_id ,'Vax2_11MoM'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 86 as master_object_id ,'Tot_Vax2_11Mo'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 279 as master_object_id ,'Influence5'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 284 as master_object_id ,'Influence4'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 283 as master_object_id ,'Influence7'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 281 as master_object_id ,'Influence6'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 278 as master_object_id ,'Influence1'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 80 as master_object_id ,'Vax12_59MoF'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 282 as master_object_id ,'Influence3'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 280 as master_object_id ,'Influence2'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 79 as master_object_id ,'Vax12_59MoM'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 88 as master_object_id ,'Tot_Vax12_59Mo'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 258 as master_object_id ,'NOimmReas14'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 285 as master_object_id ,'Influence8'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 414 as master_object_id ,'HHsampled'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 74 as master_object_id ,'Tot_Vax'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 76 as master_object_id ,'Tot_Missed'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 259 as master_object_id ,'NOimmReas15'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 253 as master_object_id ,'NOimmReas9'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 269 as master_object_id ,'Marked0to59'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 252 as master_object_id ,'NOimmReas8'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 304 as master_object_id ,'SHworker'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 301 as master_object_id ,'SPoster'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 382 as master_object_id ,'ReasonNotGiven'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 375 as master_object_id ,'PoliticalDifferences'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 370 as master_object_id ,'NotImmRedo'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 386 as master_object_id ,'SettlementsRedo'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 390 as master_object_id ,'TargetRedo'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 352 as master_object_id ,'ChildNCShool'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 341 as master_object_id ,'COMImmRedo'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 368 as master_object_id ,'NoNeedFelt'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 363 as master_object_id ,'IMMSCRelNC'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 350 as master_object_id ,'ChildAbsent'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 354 as master_object_id ,'COMImmRedoABSENT'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 362 as master_object_id ,'IMMSCOtherNC'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 376 as master_object_id ,'Reason1ABS'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 351 as master_object_id ,'ChildNCOther'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 359 as master_object_id ,'IMMOTTradNC'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 367 as master_object_id ,'NoNCShools'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 377 as master_object_id ,'Reason2ABS'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 355 as master_object_id ,'HHRevisited'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 342 as master_object_id ,'RELImmRedo'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 374 as master_object_id ,'OTRevisited'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 385 as master_object_id ,'SCRevisited'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 360 as master_object_id ,'ImmRedoABSENT'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 369 as master_object_id ,'NoNOCOther'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 373 as master_object_id ,'OTHERImRedoABSENT'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 379 as master_object_id ,'Reason4ABS'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 389 as master_object_id ,'MissedRedo'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 353 as master_object_id ,'ChildSick'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 371 as master_object_id ,'NotImmRedoABSENT'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 381 as master_object_id ,'Reason6ABS'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 388 as master_object_id ,'UnhappyWith'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 361 as master_object_id ,'IMMSCCommNC'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 419 as master_object_id ,'RAssessMrk'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 380 as master_object_id ,'Reason5ABS'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 365 as master_object_id ,'NoCaregiver'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 384 as master_object_id ,'RELImmRedoABSENT'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 357 as master_object_id ,'IMMOTOtherNC'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 364 as master_object_id ,'IMMSCTradNC'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 358 as master_object_id ,'IMMOTRelNC'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 366 as master_object_id ,'NoHHRedo'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 378 as master_object_id ,'Reason3ABS'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 340 as master_object_id ,'ImmRedo'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 356 as master_object_id ,'IMMOTCommNC'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 343 as master_object_id ,'OTHERImRedo'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 383 as master_object_id ,'ReligiousBelief'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 344 as master_object_id ,'NonCompliance'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 372 as master_object_id ,'OpvSafety'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 387 as master_object_id ,'TooManyRounds'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 402 as master_object_id ,'0to23mth Seen'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 403 as master_object_id ,'0to23mth notMarked'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 405 as master_object_id ,'24to59mth notMarked'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 275 as master_object_id ,'TOTAL Seen'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 395 as master_object_id ,'totSeet2'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 392 as master_object_id ,'totSeet3'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 394 as master_object_id ,'totSeet1'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 411 as master_object_id ,'totSeet6'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 408 as master_object_id ,'totSeet4'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 410 as master_object_id ,'totSeet5'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 400 as master_object_id ,'0to9mth Seen'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 397 as master_object_id ,'totMist2'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 393 as master_object_id ,'totMist3'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 396 as master_object_id ,'totMist1'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 413 as master_object_id ,'totMist6'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 273 as master_object_id ,'TOTAL Notmarked'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 409 as master_object_id ,'totMist4'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 412 as master_object_id ,'totMist5'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 399 as master_object_id ,'Unvaccinated this round'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 404 as master_object_id ,'24to59mth Seen'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 398 as master_object_id ,'numberof Locations'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 401 as master_object_id ,'0to9mth notMarked'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 161 as master_object_id ,'Number of cases of W1W3'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 451 as master_object_id ,'Reason for inaccessible children - No reason provided'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 441 as master_object_id ,'Political issues'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 440 as master_object_id ,'Environment issues'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 439 as master_object_id ,'Management issues'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 438 as master_object_id ,'Security Operations / Incidents'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 437 as master_object_id ,'Militant / Anti-Govt Elements'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 436 as master_object_id ,'Crime'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 435 as master_object_id ,'Local community not supportive'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 434 as master_object_id ,'Perception of fear'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 198 as master_object_id ,'Number of functional active cold chain equipment in the district'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 221 as master_object_id ,'Number of HRDs that have polio vaccine wastage rate in SIAs between 5 and 15%'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 220 as master_object_id ,'Vaccine wastage rate'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 36 as master_object_id ,'Number of social  mobilizers in place'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 433 as master_object_id ,'d4'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 432 as master_object_id ,'d1_3'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 431 as master_object_id ,'d0'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 69 as master_object_id ,'cVDPV2'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 70 as master_object_id ,'WPV1'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 70 as master_object_id ,'Number of cases of WPV 1'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 243 as master_object_id ,'Number of children 12 months and under'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 244 as master_object_id ,'Number of children under 12 months who received DPT3 or Penta3'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 177 as master_object_id ,'# of children vaccinated at transit points last month'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 158 as master_object_id ,'Number of children missed due to all access issues'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 43 as master_object_id ,'Amount total requested FRR funds'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 44 as master_object_id ,'Amount FRR funds committed'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 217 as master_object_id ,'Number of RI sessions monitored'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 216 as master_object_id ,'Number of RI sessions monitored having stockouts of any vaccine in the last month'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 195 as master_object_id ,'Number of high risk districts'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 218 as master_object_id ,'Number of HR districts with locations where OPV is delivered together with any other polio-funded services demanded by the community'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 192 as master_object_id ,'Number of RI defaulters mobilized by social mobilizers last month (with accessibility breakdown)'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 29 as master_object_id ,'Number of caregivers in HR districts'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 197 as master_object_id ,'# of HRD which reported on balance SIA vaccine stocks after last SIA round'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 199 as master_object_id ,'Total number of all active cold chain equipment in the district'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 51 as master_object_id ,'Number of children vaccinated in HRD'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 5 as master_object_id ,'Number of vaccine doses used in HRD'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 196 as master_object_id ,'HR District did not receive polio vaccine supply at least 3 days before the planned start date of campaign (yes/no)'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 210 as master_object_id ,'Number of social mobilizers who received on-the-job supervision during their last working week'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 209 as master_object_id ,'Number of SMs trained or refreshed with the integrated health package in the last 6 months'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 38 as master_object_id ,'Number of vaccination teams'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 208 as master_object_id ,'Number of vaccination teams with at least 1 member from the local community'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 207 as master_object_id ,'Target # of social mobilizers and supervisors'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 206 as master_object_id ,'Number of SMs and supervisors in place'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 33 as master_object_id ,'Number of HR sub-districts'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 34 as master_object_id ,'Number of HR sub-districts with at least 1 permanent SM'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 66 as master_object_id ,'# health fcilities having NO stock-outs of OPV'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 244 as master_object_id ,'# children received Penta3'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 45 as master_object_id ,'Amount FRR updated amount'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 46 as master_object_id ,'# received payment on time'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 38 as master_object_id ,' # polio teams'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 36 as master_object_id ,'# social mobilizers in place'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 31 as master_object_id ,'Target # of core polio communication personnel'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 46 as master_object_id ,'Number of social mobilizers who received timely payment for last campaign/month''s salary'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 42 as master_object_id ,'Number of vaccinators and SMs operating in HRDs trained on professional IPC package in last 6 months'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 37 as master_object_id ,'Number of vaccination teams with at least 1 female member'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 42 as master_object_id ,'Number of vaccinators and SMs operating in HRD who have been trained on professional Inter Personal Communication packaged in the last 6 months'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 41 as master_object_id ,'Number of vaccinators and SMs'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 55 as master_object_id ,'Number of children targeted in high-risk districts'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 37 as master_object_id ,'Number of vaccination teams with at least one female'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 41 as master_object_id ,'Number of vaccinators and social mobilizers'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 95 as master_object_id ,'spec_grp_choice'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 208 as master_object_id ,'TSettle'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 214 as master_object_id ,'Number of absences after re-visit'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 213 as master_object_id ,'Number of absences before re-visit'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 432 as master_object_id ,'Number of non-polio AFP cases with 1-3 doses of OPV'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 431 as master_object_id ,'Number of non-polio AFP cases with zero doses of OPV'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 433 as master_object_id ,'Number of non-polio AFP cases with 4+ doses of OPV'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 70 as master_object_id ,'Number of WPV1 cases'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 69 as master_object_id ,'Number of cVDPV2 cases'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 203 as master_object_id ,'Is an access-challenged district'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 204 as master_object_id ,'Total number of LT vaccination transit points planned by the programme'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 51 as master_object_id ,'Number of children vaccined in HRD'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 33 as master_object_id ,'Number of high risk sub-districts'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 46 as master_object_id ,'Number of social mobilizers receiving timely payment for last campaign'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 207 as master_object_id ,'Target number of social mobilizers and supervisors'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 34 as master_object_id ,'Number of high risk sub-districts covered by at least 1 social mobilizer'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 177 as master_object_id ,'Number of children vaccinated at transit points last month'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 38 as master_object_id ,'# of vaccination teams in HRA'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 202 as master_object_id ,'Is an access-challenged district that has a specific access approach identified'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 175 as master_object_id ,'Number of established LT vaccination transit points'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 463 as master_object_id ,'number of social mobilisers participating the telephone survey'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 209 as master_object_id ,'Number of social mobilizers trained or refreshed with the integrated health package in the last 6 months'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 221 as master_object_id ,'Is an HRD that has polio vaccine wastage rate in SIAs between 5 and 15%'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 196 as master_object_id ,'HR district did NOT receive polio vaccine supply at least 3 days before the planned start date of campaign'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 206 as master_object_id ,'Number of social mobilizers and supervisors in place'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 176 as master_object_id ,'Number of established LT vaccination transit points with a dedicated social mobilizer'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 195 as master_object_id ,'Is a high risk district'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 203 as master_object_id ,'Is an access-challenged district (Yes/No)'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 202 as master_object_id ,'Has a specific access approach identified (Yes/No)'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 244 as master_object_id ,'# of children who received Penta 3'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 243 as master_object_id ,'# of children 7-12 months old'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 27 as master_object_id ,'# of micro plans reviewed'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 197 as master_object_id ,'District reported balance of SIA vaccine stocks (Yes/No)'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 208 as master_object_id ,'Number of vaccination teams with at least one member from local community'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 158 as master_object_id ,'Number of children missed due to all access reasons'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 440 as master_object_id ,'Reason for inaccessible children - Environment issues'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 436 as master_object_id ,'Reason for inaccessible children - Crime'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 437 as master_object_id ,'Reason for inaccessible children - Militant / Anti-Govt Elements'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 439 as master_object_id ,'Reason for inaccessible children - Management issues'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 435 as master_object_id ,'Reason for inaccessible children - Local community not supportive'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 438 as master_object_id ,'Reason for inaccessible children - Security Operations / Incidents'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 434 as master_object_id ,'Reason for inaccessible children - Perception of fear'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 199 as master_object_id ,'Total number of all active cold chain equipment in district'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 26 as master_object_id ,'Number of refusals afte re-visit'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 27 as master_object_id ,'Number of microplans reviewed'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 41 as master_object_id ,'Number of vaccinators'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 42 as master_object_id ,'Number of vaccinators trained on IPC skills'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 199 as master_object_id ,'# of health facilities'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 55 as master_object_id ,'Number of targeted children in HRA'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 198 as master_object_id ,'# of high-risk districts with 90% of active cold chain equipments functional'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 28 as master_object_id ,'Number of Microplans incoroporating social data'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 204 as master_object_id ,'# of identfied/planned target points'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 207 as master_object_id ,'Number of planned SM and supervisors'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 55 as master_object_id ,'# of target children'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 196 as master_object_id ,'District DID NOT receiv OPV 3 days before campaign'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 214 as master_object_id ,'# absences after re-visit'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 213 as master_object_id ,'# of absences before re-visit'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 25 as master_object_id ,'# of refusals before re-visit'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 33 as master_object_id ,'Number of clusters (sub-district units)'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 221 as master_object_id ,'district wastage rate between 5 - 15%'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 470 as master_object_id ,'# of children missed due to access issues'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 40 as master_object_id ,'# of female SMs in place'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 46 as master_object_id ,'Number of social mobilizers who received timely payment'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 175 as master_object_id ,'# of established transit points'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 177 as master_object_id ,'# of children vaccinated at TP'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 220 as master_object_id ,'% wastage'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 463 as master_object_id ,'Number of social mobilizers responding telephone survey'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 37 as master_object_id ,'# vaccination teams with at least one female '  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 195 as master_object_id ,'District is high-risk'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 36 as master_object_id ,'# of SMs in place'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 350 as master_object_id ,'# of children missed due to absence'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 208 as master_object_id ,'# vaccination teams with at least one member from local community'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 176 as master_object_id ,'# of established transit points with social mobiliser'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 34 as master_object_id ,'Number of clusters covered by SMs'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 112 as master_object_id ,'group_msd_chd-msd_poldiffsf'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 125 as master_object_id ,'group_spec_events-spec_newborn'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 141 as master_object_id ,'group_msd_chd-msd_toomanyroundsm'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 143 as master_object_id ,'group_msd_chd-msd_poliouncommonf'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 132 as master_object_id ,'group_msd_chd-msd_poliohascuref'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 124 as master_object_id ,'group_msd_chd-msd_playgroundf'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 98 as master_object_id ,'group_msd_chd-msd_marketm'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 135 as master_object_id ,'group_spec_events-spec_zerodose'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 109 as master_object_id ,'group_msd_chd-msd_soceventm'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 131 as master_object_id ,'group_msd_chd-msd_familymovedm'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 106 as master_object_id ,'group_msd_chd-msd_noplusesf'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 130 as master_object_id ,'group_msd_chd-msd_familymovedf'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 118 as master_object_id ,'group_msd_chd-msd_noconsentf'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 129 as master_object_id ,'group_msd_chd-msd_sideeffectsm'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 146 as master_object_id ,'group_msd_chd-msd_nogovtservicesf'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 127 as master_object_id ,'group_msd_chd-tot_missed_check'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 142 as master_object_id ,'group_msd_chd-msd_poliouncommonm'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 119 as master_object_id ,'group_msd_chd-msd_relbeliefsf'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 103 as master_object_id ,'group_msd_chd-msd_agedoutf'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 136 as master_object_id ,'group_msd_chd-msd_unhappywteamm'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 99 as master_object_id ,'group_msd_chd-msd_marketf'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 145 as master_object_id ,'group_msd_chd-msd_nogovtservicesm'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 150 as master_object_id ,'group_spec_events-spec_otherdisease'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 97 as master_object_id ,'group_msd_chd-msd_farmf'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 152 as master_object_id ,'group_spec_events-spec_vcmattendedncer'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 149 as master_object_id ,'group_spec_events-spec_cmamreferral'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 138 as master_object_id ,'group_msd_chd-msd_hhnotvisitedf'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 111 as master_object_id ,'group_msd_chd-msd_poldiffsm'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 96 as master_object_id ,'group_msd_chd-msd_farmm'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 102 as master_object_id ,'group_msd_chd-msd_agedoutm'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 144 as master_object_id ,'group_spec_events-spec_rireferral'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 120 as master_object_id ,'group_msd_chd-msd_nofeltneedf'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 114 as master_object_id ,'group_msd_chd-msd_childdiedm'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 110 as master_object_id ,'group_msd_chd-msd_soceventf'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 141 as master_object_id ,'group_msd_chd-msd_toomanyroundsf'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 139 as master_object_id ,'group_msd_chd-msd_hhnotvisitedm'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 134 as master_object_id ,'group_spec_events-spec_mslscase'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 104 as master_object_id ,'group_spec_events-spec_fic'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 133 as master_object_id ,'group_msd_chd-msd_poliohascurem'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 108 as master_object_id ,'group_msd_chd-msd_securityf'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 126 as master_object_id ,'group_spec_events-spec_afpcase'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 122 as master_object_id ,'group_msd_chd-msd_relbeliefsm'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 76 as master_object_id ,'tot_missed'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 113 as master_object_id ,'group_msd_chd-msd_childdiedf'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 137 as master_object_id ,'group_msd_chd-msd_unhappywteamf'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 101 as master_object_id ,'group_msd_chd-msd_schoolm'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 147 as master_object_id ,'group_msd_chd-msd_otherprotectionf'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 107 as master_object_id ,'group_msd_chd-msd_securitym'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 148 as master_object_id ,'group_msd_chd-msd_otherprotectionm'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 123 as master_object_id ,'group_msd_chd-msd_playgroundm'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 100 as master_object_id ,'group_msd_chd-msd_schoolf'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 115 as master_object_id ,'group_msd_chd-msd_childsickm'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 116 as master_object_id ,'group_msd_chd-msd_childsickf'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 105 as master_object_id ,'group_msd_chd-msd_noplusesm'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 128 as master_object_id ,'group_msd_chd-msd_sideeffectsf'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 121 as master_object_id ,'group_msd_chd-msd_nofeltneedm'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 151 as master_object_id ,'group_spec_events-spec_pregnantmother'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 117 as master_object_id ,'group_msd_chd-msd_noconsentm'  as source_object_code,'indicator' as content_type UNION ALL
        SELECT 55 as master_object_id ,'Number of target children'  as source_object_code,'indicator' as content_type
        ) ind
        WHERE EXISTS ( SELECT 1 FROM indicator i where ind.master_object_id = i.id)

        UNION ALL

        SELECT * FROM (
        SELECT 99 as master_object_id ,'Nigeria November 2013'  as source_object_code,'campaign' as content_type UNION ALL
        SELECT 100 as master_object_id ,'Nigeria November 2014'  as source_object_code,'campaign' as content_type UNION ALL
        SELECT 101 as master_object_id ,'Nigeria September 2013'  as source_object_code,'campaign' as content_type UNION ALL
        SELECT 102 as master_object_id ,'Nigeria March 2012'  as source_object_code,'campaign' as content_type UNION ALL
        SELECT 103 as master_object_id ,'Nigeria June 2012'  as source_object_code,'campaign' as content_type UNION ALL
        SELECT 104 as master_object_id ,'Nigeria August 2014'  as source_object_code,'campaign' as content_type UNION ALL
        SELECT 105 as master_object_id ,'Nigeria March 2013'  as source_object_code,'campaign' as content_type UNION ALL
        SELECT 106 as master_object_id ,'Nigeria October 2013'  as source_object_code,'campaign' as content_type UNION ALL
        SELECT 107 as master_object_id ,'Nigeria May 2013'  as source_object_code,'campaign' as content_type UNION ALL
        SELECT 108 as master_object_id ,'Nigeria March 2014'  as source_object_code,'campaign' as content_type UNION ALL
        SELECT 109 as master_object_id ,'Nigeria February 2013'  as source_object_code,'campaign' as content_type UNION ALL
        SELECT 110 as master_object_id ,'Nigeria December 2012'  as source_object_code,'campaign' as content_type UNION ALL
        SELECT 111 as master_object_id ,'Nigeria June 2014'  as source_object_code,'campaign' as content_type UNION ALL
        SELECT 112 as master_object_id ,'Nigeria December 2013'  as source_object_code,'campaign' as content_type UNION ALL
        SELECT 113 as master_object_id ,'Nigeria September 2012'  as source_object_code,'campaign' as content_type UNION ALL
        SELECT 114 as master_object_id ,'Nigeria April 2013'  as source_object_code,'campaign' as content_type UNION ALL
        SELECT 115 as master_object_id ,'Nigeria April 2014'  as source_object_code,'campaign' as content_type UNION ALL
        SELECT 116 as master_object_id ,'Nigeria June 2013'  as source_object_code,'campaign' as content_type UNION ALL
        SELECT 117 as master_object_id ,'Nigeria January 2014'  as source_object_code,'campaign' as content_type UNION ALL
        SELECT 118 as master_object_id ,'Nigeria January 2012'  as source_object_code,'campaign' as content_type UNION ALL
        SELECT 119 as master_object_id ,'Nigeria August 2012'  as source_object_code,'campaign' as content_type UNION ALL
        SELECT 120 as master_object_id ,'Nigeria January 2013'  as source_object_code,'campaign' as content_type UNION ALL
        SELECT 121 as master_object_id ,'Nigeria October 2012'  as source_object_code,'campaign' as content_type UNION ALL
        SELECT 122 as master_object_id ,'Nigeria October 2014'  as source_object_code,'campaign' as content_type UNION ALL
        SELECT 123 as master_object_id ,'Nigeria August 2013'  as source_object_code,'campaign' as content_type UNION ALL
        SELECT 124 as master_object_id ,'Nigeria July 2014'  as source_object_code,'campaign' as content_type UNION ALL
        SELECT 125 as master_object_id ,'Nigeria May 2014'  as source_object_code,'campaign' as content_type UNION ALL
        SELECT 126 as master_object_id ,'Nigeria November 2012'  as source_object_code,'campaign' as content_type UNION ALL
        SELECT 127 as master_object_id ,'Nigeria July 2012'  as source_object_code,'campaign' as content_type UNION ALL
        SELECT 128 as master_object_id ,'Nigeria September 2014'  as source_object_code,'campaign' as content_type UNION ALL
        SELECT 129 as master_object_id ,'Nigeria April 2012'  as source_object_code,'campaign' as content_type UNION ALL
        SELECT 130 as master_object_id ,'Nigeria February 2014'  as source_object_code,'campaign' as content_type UNION ALL
        SELECT 131 as master_object_id ,'Nigeria July 2013'  as source_object_code,'campaign' as content_type UNION ALL
        SELECT 132 as master_object_id ,'Nigeria May 2012'  as source_object_code,'campaign' as content_type UNION ALL
        SELECT 133 as master_object_id ,'Afghanistan July 2012'  as source_object_code,'campaign' as content_type UNION ALL
        SELECT 134 as master_object_id ,'Afghanistan November 2012'  as source_object_code,'campaign' as content_type UNION ALL
        SELECT 135 as master_object_id ,'Afghanistan December 2012'  as source_object_code,'campaign' as content_type UNION ALL
        SELECT 136 as master_object_id ,'Afghanistan September 2013'  as source_object_code,'campaign' as content_type UNION ALL
        SELECT 137 as master_object_id ,'Afghanistan February 2014'  as source_object_code,'campaign' as content_type UNION ALL
        SELECT 138 as master_object_id ,'Afghanistan March 2013'  as source_object_code,'campaign' as content_type UNION ALL
        SELECT 139 as master_object_id ,'Afghanistan June 2014'  as source_object_code,'campaign' as content_type UNION ALL
        SELECT 140 as master_object_id ,'Afghanistan September 2012'  as source_object_code,'campaign' as content_type UNION ALL
        SELECT 141 as master_object_id ,'Afghanistan October 2012'  as source_object_code,'campaign' as content_type UNION ALL
        SELECT 143 as master_object_id ,'Afghanistan June 2013'  as source_object_code,'campaign' as content_type UNION ALL
        SELECT 144 as master_object_id ,'Afghanistan September 2014'  as source_object_code,'campaign' as content_type UNION ALL
        SELECT 145 as master_object_id ,'Afghanistan November 2013'  as source_object_code,'campaign' as content_type UNION ALL
        SELECT 146 as master_object_id ,'Afghanistan May 2012'  as source_object_code,'campaign' as content_type UNION ALL
        SELECT 147 as master_object_id ,'Afghanistan August 2013'  as source_object_code,'campaign' as content_type UNION ALL
        SELECT 148 as master_object_id ,'Afghanistan February 2012'  as source_object_code,'campaign' as content_type UNION ALL
        SELECT 149 as master_object_id ,'Afghanistan August 2012'  as source_object_code,'campaign' as content_type UNION ALL
        SELECT 150 as master_object_id ,'Afghanistan May 2014'  as source_object_code,'campaign' as content_type UNION ALL
        SELECT 151 as master_object_id ,'Afghanistan July 2013'  as source_object_code,'campaign' as content_type UNION ALL
        SELECT 152 as master_object_id ,'Afghanistan August 2014'  as source_object_code,'campaign' as content_type UNION ALL
        SELECT 153 as master_object_id ,'Afghanistan January 2014'  as source_object_code,'campaign' as content_type UNION ALL
        SELECT 154 as master_object_id ,'Afghanistan March 2012'  as source_object_code,'campaign' as content_type UNION ALL
        SELECT 156 as master_object_id ,'Afghanistan January 2012'  as source_object_code,'campaign' as content_type UNION ALL
        SELECT 157 as master_object_id ,'Afghanistan March 2014'  as source_object_code,'campaign' as content_type UNION ALL
        SELECT 158 as master_object_id ,'Afghanistan December 2013'  as source_object_code,'campaign' as content_type UNION ALL
        SELECT 159 as master_object_id ,'Afghanistan October 2013'  as source_object_code,'campaign' as content_type UNION ALL
        SELECT 160 as master_object_id ,'Afghanistan January 2013'  as source_object_code,'campaign' as content_type UNION ALL
        SELECT 161 as master_object_id ,'Afghanistan February 2013'  as source_object_code,'campaign' as content_type UNION ALL
        SELECT 162 as master_object_id ,'Afghanistan June 2012'  as source_object_code,'campaign' as content_type UNION ALL
        SELECT 163 as master_object_id ,'Pakistan February 2014'  as source_object_code,'campaign' as content_type UNION ALL
        SELECT 164 as master_object_id ,'Pakistan November 2013'  as source_object_code,'campaign' as content_type UNION ALL
        SELECT 165 as master_object_id ,'Pakistan August 2013'  as source_object_code,'campaign' as content_type UNION ALL
        SELECT 166 as master_object_id ,'Pakistan June 2013'  as source_object_code,'campaign' as content_type UNION ALL
        SELECT 167 as master_object_id ,'Pakistan January 2014'  as source_object_code,'campaign' as content_type UNION ALL
        SELECT 168 as master_object_id ,'Pakistan December 2013'  as source_object_code,'campaign' as content_type UNION ALL
        SELECT 169 as master_object_id ,'Pakistan May 2013'  as source_object_code,'campaign' as content_type UNION ALL
        SELECT 170 as master_object_id ,'Pakistan July 2013'  as source_object_code,'campaign' as content_type UNION ALL
        SELECT 171 as master_object_id ,'Pakistan July 2014'  as source_object_code,'campaign' as content_type UNION ALL
        SELECT 172 as master_object_id ,'Pakistan October 2013'  as source_object_code,'campaign' as content_type UNION ALL
        SELECT 173 as master_object_id ,'Pakistan April 2013'  as source_object_code,'campaign' as content_type UNION ALL
        SELECT 174 as master_object_id ,'Pakistan June 2014'  as source_object_code,'campaign' as content_type UNION ALL
        SELECT 175 as master_object_id ,'Pakistan May 2014'  as source_object_code,'campaign' as content_type UNION ALL
        SELECT 176 as master_object_id ,'Pakistan March 2014'  as source_object_code,'campaign' as content_type UNION ALL
        SELECT 177 as master_object_id ,'Pakistan April 2014'  as source_object_code,'campaign' as content_type UNION ALL
        SELECT 178 as master_object_id ,'Pakistan August 2014'  as source_object_code,'campaign' as content_type UNION ALL
        SELECT 179 as master_object_id ,'Pakistan September 2013'  as source_object_code,'campaign' as content_type UNION ALL
        SELECT 106 as master_object_id ,'Nigeria 2013.10'  as source_object_code,'campaign' as content_type UNION ALL
        SELECT 112 as master_object_id ,'Nigeria 2013.12'  as source_object_code,'campaign' as content_type UNION ALL
        SELECT 120 as master_object_id ,'Nigeria 2013.1'  as source_object_code,'campaign' as content_type UNION ALL
        SELECT 105 as master_object_id ,'Nigeria 2013.3'  as source_object_code,'campaign' as content_type UNION ALL
        SELECT 109 as master_object_id ,'Nigeria 2013.2'  as source_object_code,'campaign' as content_type UNION ALL
        SELECT 107 as master_object_id ,'Nigeria 2013.5'  as source_object_code,'campaign' as content_type UNION ALL
        SELECT 114 as master_object_id ,'Nigeria 2013.4'  as source_object_code,'campaign' as content_type UNION ALL
        SELECT 131 as master_object_id ,'Nigeria 2013.7'  as source_object_code,'campaign' as content_type UNION ALL
        SELECT 116 as master_object_id ,'Nigeria 2013.6'  as source_object_code,'campaign' as content_type UNION ALL
        SELECT 101 as master_object_id ,'Nigeria 2013.9'  as source_object_code,'campaign' as content_type UNION ALL
        SELECT 123 as master_object_id ,'Nigeria 2013.8'  as source_object_code,'campaign' as content_type UNION ALL
        SELECT 180 as master_object_id ,'Pakistan 2014.9'  as source_object_code,'campaign' as content_type UNION ALL
        SELECT 178 as master_object_id ,'Pakistan 2014.8'  as source_object_code,'campaign' as content_type UNION ALL
        SELECT 171 as master_object_id ,'Pakistan 2014.7'  as source_object_code,'campaign' as content_type UNION ALL
        SELECT 174 as master_object_id ,'Pakistan 2014.6'  as source_object_code,'campaign' as content_type UNION ALL
        SELECT 175 as master_object_id ,'Pakistan 2014.5'  as source_object_code,'campaign' as content_type UNION ALL
        SELECT 177 as master_object_id ,'Pakistan 2014.4'  as source_object_code,'campaign' as content_type UNION ALL
        SELECT 176 as master_object_id ,'Pakistan 2014.3'  as source_object_code,'campaign' as content_type UNION ALL
        SELECT 163 as master_object_id ,'Pakistan 2014.2'  as source_object_code,'campaign' as content_type UNION ALL
        SELECT 167 as master_object_id ,'Pakistan 2014.1'  as source_object_code,'campaign' as content_type UNION ALL
        SELECT 181 as master_object_id ,'Pakistan 2012.1'  as source_object_code,'campaign' as content_type UNION ALL
        SELECT 182 as master_object_id ,'Pakistan 2012.3'  as source_object_code,'campaign' as content_type UNION ALL
        SELECT 183 as master_object_id ,'Pakistan 2012.2'  as source_object_code,'campaign' as content_type UNION ALL
        SELECT 184 as master_object_id ,'Pakistan 2012.5'  as source_object_code,'campaign' as content_type UNION ALL
        SELECT 185 as master_object_id ,'Pakistan 2012.4'  as source_object_code,'campaign' as content_type UNION ALL
        SELECT 186 as master_object_id ,'Pakistan 2012.7'  as source_object_code,'campaign' as content_type UNION ALL
        SELECT 187 as master_object_id ,'Pakistan 2012.6'  as source_object_code,'campaign' as content_type UNION ALL
        SELECT 188 as master_object_id ,'Pakistan 2012.9'  as source_object_code,'campaign' as content_type UNION ALL
        SELECT 189 as master_object_id ,'Pakistan 2012.8'  as source_object_code,'campaign' as content_type UNION ALL
        SELECT 137 as master_object_id ,'Afghanistan 2014.2'  as source_object_code,'campaign' as content_type UNION ALL
        SELECT 144 as master_object_id ,'Afghanistan 2014.9'  as source_object_code,'campaign' as content_type UNION ALL
        SELECT 152 as master_object_id ,'Afghanistan 2014.8'  as source_object_code,'campaign' as content_type UNION ALL
        SELECT 134 as master_object_id ,'Afghanistan 2012.11'  as source_object_code,'campaign' as content_type UNION ALL
        SELECT 141 as master_object_id ,'Afghanistan 2012.10'  as source_object_code,'campaign' as content_type UNION ALL
        SELECT 153 as master_object_id ,'Afghanistan 2014.1'  as source_object_code,'campaign' as content_type UNION ALL
        SELECT 135 as master_object_id ,'Afghanistan 2012.12'  as source_object_code,'campaign' as content_type UNION ALL
        SELECT 139 as master_object_id ,'Afghanistan 2014.6'  as source_object_code,'campaign' as content_type UNION ALL
        SELECT 150 as master_object_id ,'Afghanistan 2014.5'  as source_object_code,'campaign' as content_type UNION ALL
        SELECT 190 as master_object_id ,'Afghanistan 2014.4'  as source_object_code,'campaign' as content_type UNION ALL
        SELECT 173 as master_object_id ,'Pakistan 2013.4'  as source_object_code,'campaign' as content_type UNION ALL
        SELECT 169 as master_object_id ,'Pakistan 2013.5'  as source_object_code,'campaign' as content_type UNION ALL
        SELECT 166 as master_object_id ,'Pakistan 2013.6'  as source_object_code,'campaign' as content_type UNION ALL
        SELECT 170 as master_object_id ,'Pakistan 2013.7'  as source_object_code,'campaign' as content_type UNION ALL
        SELECT 191 as master_object_id ,'Pakistan 2013.1'  as source_object_code,'campaign' as content_type UNION ALL
        SELECT 192 as master_object_id ,'Pakistan 2013.2'  as source_object_code,'campaign' as content_type UNION ALL
        SELECT 193 as master_object_id ,'Pakistan 2013.3'  as source_object_code,'campaign' as content_type UNION ALL
        SELECT 165 as master_object_id ,'Pakistan 2013.8'  as source_object_code,'campaign' as content_type UNION ALL
        SELECT 179 as master_object_id ,'Pakistan 2013.9'  as source_object_code,'campaign' as content_type UNION ALL
        SELECT 130 as master_object_id ,'Nigeria 2014.2'  as source_object_code,'campaign' as content_type UNION ALL
        SELECT 108 as master_object_id ,'Nigeria 2014.3'  as source_object_code,'campaign' as content_type UNION ALL
        SELECT 111 as master_object_id ,'Nigeria 2014.6'  as source_object_code,'campaign' as content_type UNION ALL
        SELECT 124 as master_object_id ,'Nigeria 2014.7'  as source_object_code,'campaign' as content_type UNION ALL
        SELECT 115 as master_object_id ,'Nigeria 2014.4'  as source_object_code,'campaign' as content_type UNION ALL
        SELECT 125 as master_object_id ,'Nigeria 2014.5'  as source_object_code,'campaign' as content_type UNION ALL
        SELECT 104 as master_object_id ,'Nigeria 2014.8'  as source_object_code,'campaign' as content_type UNION ALL
        SELECT 110 as master_object_id ,'Nigeria 2012.12'  as source_object_code,'campaign' as content_type UNION ALL
        SELECT 121 as master_object_id ,'Nigeria 2012.10'  as source_object_code,'campaign' as content_type UNION ALL
        SELECT 126 as master_object_id ,'Nigeria 2012.11'  as source_object_code,'campaign' as content_type UNION ALL
        SELECT 160 as master_object_id ,'Afghanistan 2013.1'  as source_object_code,'campaign' as content_type UNION ALL
        SELECT 161 as master_object_id ,'Afghanistan 2013.2'  as source_object_code,'campaign' as content_type UNION ALL
        SELECT 138 as master_object_id ,'Afghanistan 2013.3'  as source_object_code,'campaign' as content_type UNION ALL
        SELECT 119 as master_object_id ,'Nigeria 2012.8'  as source_object_code,'campaign' as content_type UNION ALL
        SELECT 113 as master_object_id ,'Nigeria 2012.9'  as source_object_code,'campaign' as content_type UNION ALL
        SELECT 143 as master_object_id ,'Afghanistan 2013.6'  as source_object_code,'campaign' as content_type UNION ALL
        SELECT 151 as master_object_id ,'Afghanistan 2013.7'  as source_object_code,'campaign' as content_type UNION ALL
        SELECT 129 as master_object_id ,'Nigeria 2012.4'  as source_object_code,'campaign' as content_type UNION ALL
        SELECT 132 as master_object_id ,'Nigeria 2012.5'  as source_object_code,'campaign' as content_type UNION ALL
        SELECT 103 as master_object_id ,'Nigeria 2012.6'  as source_object_code,'campaign' as content_type UNION ALL
        SELECT 127 as master_object_id ,'Nigeria 2012.7'  as source_object_code,'campaign' as content_type UNION ALL
        SELECT 118 as master_object_id ,'Nigeria 2012.1'  as source_object_code,'campaign' as content_type UNION ALL
        SELECT 102 as master_object_id ,'Nigeria 2012.3'  as source_object_code,'campaign' as content_type UNION ALL
        SELECT 194 as master_object_id ,'Pakistan 2012.11'  as source_object_code,'campaign' as content_type UNION ALL
        SELECT 195 as master_object_id ,'Pakistan 2012.10'  as source_object_code,'campaign' as content_type UNION ALL
        SELECT 196 as master_object_id ,'Pakistan 2012.12'  as source_object_code,'campaign' as content_type UNION ALL
        SELECT 140 as master_object_id ,'Afghanistan 2012.9'  as source_object_code,'campaign' as content_type UNION ALL
        SELECT 149 as master_object_id ,'Afghanistan 2012.8'  as source_object_code,'campaign' as content_type UNION ALL
        SELECT 146 as master_object_id ,'Afghanistan 2012.5'  as source_object_code,'campaign' as content_type UNION ALL
        SELECT 133 as master_object_id ,'Afghanistan 2012.7'  as source_object_code,'campaign' as content_type UNION ALL
        SELECT 162 as master_object_id ,'Afghanistan 2012.6'  as source_object_code,'campaign' as content_type UNION ALL
        SELECT 156 as master_object_id ,'Afghanistan 2012.1'  as source_object_code,'campaign' as content_type UNION ALL
        SELECT 154 as master_object_id ,'Afghanistan 2012.3'  as source_object_code,'campaign' as content_type UNION ALL
        SELECT 148 as master_object_id ,'Afghanistan 2012.2'  as source_object_code,'campaign' as content_type UNION ALL
        SELECT 168 as master_object_id ,'Pakistan 2013.12'  as source_object_code,'campaign' as content_type UNION ALL
        SELECT 172 as master_object_id ,'Pakistan 2013.10'  as source_object_code,'campaign' as content_type UNION ALL
        SELECT 164 as master_object_id ,'Pakistan 2013.11'  as source_object_code,'campaign' as content_type UNION ALL
        SELECT 147 as master_object_id ,'Afghanistan 2013.8'  as source_object_code,'campaign' as content_type UNION ALL
        SELECT 136 as master_object_id ,'Afghanistan 2013.9'  as source_object_code,'campaign' as content_type UNION ALL
        SELECT 158 as master_object_id ,'Afghanistan 2013.12'  as source_object_code,'campaign' as content_type UNION ALL
        SELECT 159 as master_object_id ,'Afghanistan 2013.10'  as source_object_code,'campaign' as content_type UNION ALL
        SELECT 145 as master_object_id ,'Afghanistan 2013.11'  as source_object_code,'campaign' as content_type UNION ALL
        SELECT 115 as master_object_id ,'Tue Apr 01 00:00:00 UTC 2014'  as source_object_code,'campaign' as content_type UNION ALL
        SELECT 201 as master_object_id ,'Mon Dec 01 00:00:00 UTC 2014'  as source_object_code,'campaign' as content_type UNION ALL
        SELECT 111 as master_object_id ,'Sun Jun 01 00:00:00 UTC 2014'  as source_object_code,'campaign' as content_type UNION ALL
        SELECT 201 as master_object_id ,'41974'  as source_object_code,'campaign' as content_type UNION ALL
        SELECT 207 as master_object_id ,'Pakistan January 2015'  as source_object_code,'campaign' as content_type UNION ALL
        SELECT 208 as master_object_id ,'Pakistan February 2015'  as source_object_code,'campaign' as content_type UNION ALL
        SELECT 206 as master_object_id ,'Afghanistan February 2015'  as source_object_code,'campaign' as content_type UNION ALL
        SELECT 211 as master_object_id ,'Nigeria February 2015'  as source_object_code,'campaign' as content_type UNION ALL
        SELECT 210 as master_object_id ,'Nigeria January 2015'  as source_object_code,'campaign' as content_type UNION ALL
        SELECT 214 as master_object_id ,'Pakistan March 2015'  as source_object_code,'campaign' as content_type UNION ALL
        SELECT 213 as master_object_id ,'Afghanistan March 2015'  as source_object_code,'campaign' as content_type UNION ALL
        SELECT 209 as master_object_id ,'Afghanistan January 2015'  as source_object_code,'campaign' as content_type UNION ALL
        SELECT 212 as master_object_id ,'Nigeria March 2015'  as source_object_code,'campaign' as content_type UNION ALL
        SELECT 142 as master_object_id ,'Afghanistan April 2013'  as source_object_code,'campaign' as content_type UNION ALL
        SELECT 155 as master_object_id ,'Afghanistan May 2013'  as source_object_code,'campaign' as content_type UNION ALL
        SELECT 216 as master_object_id ,'Nigeria February 2012'  as source_object_code,'campaign' as content_type UNION ALL
        SELECT 215 as master_object_id ,'Afghanistan April 2012'  as source_object_code,'campaign' as content_type UNION ALL
        SELECT 210 as master_object_id ,'Nigeria Jan 2015'  as source_object_code,'campaign' as content_type UNION ALL
        SELECT 212 as master_object_id ,'Nigeria Mar 1, 2015'  as source_object_code,'campaign' as content_type UNION ALL
        SELECT 223 as master_object_id ,'nigeria-2015-06-01'  as source_object_code,'campaign' as content_type UNION ALL
        SELECT 197 as master_object_id ,'Pakistan December 2014'  as source_object_code,'campaign' as content_type UNION ALL
        SELECT 200 as master_object_id ,'Afghanistan December 2014'  as source_object_code,'campaign' as content_type UNION ALL
        SELECT 190 as master_object_id ,'Afghanistan April 2014'  as source_object_code,'campaign' as content_type UNION ALL
        SELECT 198 as master_object_id ,'Afghanistan October 2014'  as source_object_code,'campaign' as content_type UNION ALL
        SELECT 201 as master_object_id ,'Nigeria December 2014'  as source_object_code,'campaign' as content_type UNION ALL
        SELECT 202 as master_object_id ,'Afghanistan November 2014'  as source_object_code,'campaign' as content_type UNION ALL
        SELECT 199 as master_object_id ,'Afghanistan July 2014'  as source_object_code,'campaign' as content_type UNION ALL
        SELECT 203 as master_object_id ,'Pakistan November 2014'  as source_object_code,'campaign' as content_type UNION ALL
        SELECT 204 as master_object_id ,'Pakistan October 2014'  as source_object_code,'campaign' as content_type UNION ALL
        SELECT 180 as master_object_id ,'Pakistan September 2014'  as source_object_code,'campaign' as content_type UNION ALL
        SELECT 171 as master_object_id ,'Pakistan Jul 2014'  as source_object_code,'campaign' as content_type UNION ALL
        SELECT 199 as master_object_id ,'Afghanistan Jul 2014'  as source_object_code,'campaign' as content_type UNION ALL
        SELECT 124 as master_object_id ,'Nigeria Jul 2014'  as source_object_code,'campaign' as content_type UNION ALL
        SELECT 163 as master_object_id ,'Paksitan February 2014'  as source_object_code,'campaign' as content_type UNION ALL
        SELECT 150 as master_object_id ,'Afganistan May 2014'  as source_object_code,'campaign' as content_type UNION ALL
        SELECT 191 as master_object_id ,'Pakistan January 2013'  as source_object_code,'campaign' as content_type UNION ALL
        SELECT 188 as master_object_id ,'Pakistan September 2012'  as source_object_code,'campaign' as content_type UNION ALL
        SELECT 189 as master_object_id ,'Pakistan August 2012'  as source_object_code,'campaign' as content_type UNION ALL
        SELECT 195 as master_object_id ,'Pakistan October 2012'  as source_object_code,'campaign' as content_type UNION ALL
        SELECT 194 as master_object_id ,'Pakistan November 2012'  as source_object_code,'campaign' as content_type UNION ALL
        SELECT 187 as master_object_id ,'Pakistan June 2012'  as source_object_code,'campaign' as content_type UNION ALL
        SELECT 181 as master_object_id ,'Pakistan January 2012'  as source_object_code,'campaign' as content_type UNION ALL
        SELECT 186 as master_object_id ,'Pakistan July 2012'  as source_object_code,'campaign' as content_type UNION ALL
        SELECT 192 as master_object_id ,'Pakistan February 2013'  as source_object_code,'campaign' as content_type UNION ALL
        SELECT 184 as master_object_id ,'Pakistan May 2012'  as source_object_code,'campaign' as content_type UNION ALL
        SELECT 183 as master_object_id ,'Pakistan February 2012'  as source_object_code,'campaign' as content_type UNION ALL
        SELECT 182 as master_object_id ,'Pakistan March 2012'  as source_object_code,'campaign' as content_type UNION ALL
        SELECT 193 as master_object_id ,'Pakistan March 2013'  as source_object_code,'campaign' as content_type UNION ALL
        SELECT 196 as master_object_id ,'Pakistan December 2012'  as source_object_code,'campaign' as content_type UNION ALL
        SELECT 185 as master_object_id ,'Pakistan April 2012'  as source_object_code,'campaign' as content_type
        )c
        WHERE EXISTS ( SELECT 1 FROM campaign camp where c.master_object_id = camp.id)

        )x;

        INSERT INTO source_object_map (master_object_id, source_object_code, mapped_by_id, content_type)
        SELECT
            c.id
            , c.slug
            , 1
            , 'campaign'
        FROM campaign c WHERE NOT EXISTS (
            SELECT 1 FROM source_object_map m
            WHERE m.source_object_code = c.slug
            );
    """)

    ]
