# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('datapoints', '0005_load_ng_regions'),
    ]

    operations = [

        migrations.RunSQL("""


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

        -- CAMPAIGNS --

        INSERT INTO campaign
        (start_date,end_date,slug,campaign_type_id, office_id, created_at)

        SELECT CAST(the_date AS DATE), CAST(the_date AS DATE),the_slug,ct.id,o.id, now() FROM (
        SELECT '2014-08-01' as the_date,'nigeria-august-2014' as the_slug UNION ALL
        SELECT '2014-03-01','nigeria-march-2014' UNION ALL
        SELECT '2014-06-01','nigeria-june-2014' UNION ALL
        SELECT '2014-04-01','nigeria-april-2014' UNION ALL
        SELECT '2014-10-01','nigeria-october-2014' UNION ALL
        SELECT '2014-07-01','nigeria-july-2014' UNION ALL
        SELECT '2014-05-01','nigeria-may-2014' UNION ALL
        SELECT '2014-09-01','nigeria-september-2014' UNION ALL
        SELECT '2014-02-01','nigeria-february-2014' UNION ALL
        SELECT '2014-11-01','nigeria-november-2014' UNION ALL
        SELECT '2014-12-01','nigeria-2014-12-01' UNION ALL
        SELECT '2015-01-01','nigeria-2015-01-01' UNION ALL
        SELECT '2015-02-01','nigeria-2015-02-01' UNION ALL
        SELECT '2015-03-01','nigeria-2015-03-01' UNION ALL
        SELECT '2015-06-01','nigeria-2015-06-01'
        )x
        INNER JOIN office o
        ON o.name = 'Nigeria'
        INNER JOIN campaign_type ct
        ON ct.name = 'National Immunization Days (NID)';
        """)
    ]
