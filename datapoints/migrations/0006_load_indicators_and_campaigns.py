# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('datapoints', '0005_load_ng_regions'),
    ]

    operations = [

        migrations.RunSQL("""
	insert into indicator
	(id, name,description,slug,short_name,is_reported,created_at)

	SELECT id, name,description,LEFT(slug,50),short_name,CAST(0 AS BOOLEAN),now()
	FROM (

        SELECT 461 as id, '# of established LT vaccination transit points vs. total # identified by the programme' as name,'# of established LT vaccination transit points vs. total # identified by the programme' as description,'of-established-lt-vaccination-transit-points-vs-total-identified-by-the-programme' as slug,'# of established LT vaccination transit points vs. total # identified by the programme' as short_name UNION ALL
        SELECT 462, 'Number of regions sampled','The total number of regions sampled.','number-of-regions-sampled','# regions sampled' UNION ALL
        SELECT 41, 'Number of vaccinators','Number of vaccinators','number-of-front-line-workers','Number of vaccinators' UNION ALL
        SELECT 159, 'Number of aVDPV2 cases','Number of aVDPV2 cases','number-of-avdpv2-cases','Number of aVDPV2 cases' UNION ALL
        SELECT 162, 'Number of iVDPV cases','Number of iVDPV cases','number-of-ivdpv-cases','Number of iVDPV cases' UNION ALL
        SELECT 32, 'Number of Unicef polio positions in their posts in PBR-approved structures','Number of Unicef polio positions in their posts in PBR-approved structures','number-of-polio-communication-positions-in-place','Number of Unicef polio positions in their posts in PBR' UNION ALL
        SELECT 31, 'Target number of Unicef polio positions in PBR-approved structures','Target number of Unicef polio positions in PBR-approved structures','target-number-of-polio-communication-positions','Target number of Unicef polio positions in PBR-approv' UNION ALL
        SELECT 21, 'Number of all missed children','Number of all missed children','number-of-all-missed-children','All missed children' UNION ALL
        SELECT 24, 'Number of children missed due to other reasons','Number of children missed due to other reasons','number-of-children-missed-due-to-other-reasons','Missed due to other reasons' UNION ALL
        SELECT 25, 'Number of refusals before re-visit','Number of refusals before re-visit','number-of-refusals-before-re-visit-2','Refusals before re-visit' UNION ALL
        SELECT 26, 'Number of refusals after re-visit','Number of refusals after re-visit','number-of-refusals-after-re-visit-2','Refusals after re-visit' UNION ALL
        SELECT 27, 'Number of microplans in high risk districts','Number of microplans in high risk districts','number-of-microplans-in-high-risk-district','Microplans in High Risk Disrict' UNION ALL
        SELECT 30, 'Number of caregivers aware of polio campaigns','Number of caregivers aware of polio campaigns','number-of-caregivers-aware-of-polio-campaigns','Number of caregivers aware' UNION ALL
        SELECT 28, 'Number of microplans in high risk districts incorporating social data','Number of microplans in high risk districts Incorporating social data','number-of-microplans-in-high-risk-districts-incorporating-social-data','Microplans incorporating social data' UNION ALL
        SELECT 35, 'Number of target social mobilizers','Number of target social mobilizers','number-of-target-social-mobilizers','Number of target social mobilizers' UNION ALL
        SELECT 40, 'Number of female social mobilizers','Number of female social mobilizers','number-of-female-social-mobilizers','Number of female social mobilizers' UNION ALL
        SELECT 45, 'FRR updated quarterly','FRR updated quarterly','frr-updated-quarterly','FRR updated quarterly' UNION ALL
        SELECT 46, 'Number of social mobilizers receiving timely payment for last campaign','Number of social mobilizers receiving timely payment for last campaign','number-of-social-mobilizers-receiving-timely-payment-for-last-campaign','Number of social mobilizers receiving timely payment' UNION ALL
        SELECT 34, 'Number of high risk sub-districts covered by at least 1 social mobilizer','Number of high risk sub-districts covered by at least 1 social mobilizer','number-of-high-risk-areas-with-social-mobilizers-2','Number of high risk sub-districts w social mobilizers' UNION ALL
        SELECT 43, 'Amount total requested FRR funds','Amount total requested FRR funds','amount-total-frr-funds','Amount total requested FRR funds' UNION ALL
        SELECT 38, 'Number of vaccination teams','Number of vaccination teams','number-of-teams','Number of vaccination teams' UNION ALL
        SELECT 36, 'Number of social mobilizers in place','Number of social mobilizers in place','number-of-target-social-mobilizers-in-place','Number of social mobilizers in place' UNION ALL
        SELECT 29, 'Number of caregivers in high risk districts','Number of caregivers in high risk districts','number-of-caregivers','Number of caregivers in high risk districts' UNION ALL
        SELECT 44, 'Amount FRR funds committed','Amount FRR funds committed ','amount-frr-funds-committed','Amount FRR funds committed ' UNION ALL
        SELECT 49, 'Number of social mobilizers trained on RI in past 6 mo','Number of social mobilizers trained on RI in past 6 mo','number-of-social-mobilizers-trained-on-ri-in-past-6-mo','Number of social mobilizers trained on RI in past 6 mo' UNION ALL
        SELECT 93, 'ODK - Census  Newborns Female','censusnewbornsf','censusnewbornsf','ODK - Census  Newborns Female' UNION ALL
        SELECT 112, 'ODK - group_msd_chd_msd_poldiffsf','group_msd_chd_msd_poldiffsf','group-msd-chd-msd-poldiffsf','ODK - group_msd_chd_msd_poldiffsf' UNION ALL
        SELECT 42, 'Number of vaccinators operating in HRDs trained on professional IPC package in last 6 months','Number of vaccinators operating in HRDs trained on professional IPC package in last 6 months','number-of-front-line-workers-with-ipc-skills','# vaccinators in HRDs trained on IPC in last 6 mo' UNION ALL
        SELECT 1, 'Polio Cases YTDYYYY','Polio Cases YTDYYYY','polio-cases-ytd','Polio Cases YTDYYYY' UNION ALL
        SELECT 53, 'Number of districts having NO stockouts of OPV','Number of districts having NO stockouts of OPV','number-of-districts-having-no-stockouts-of-opv','Number of districts having NO stockouts of OPV' UNION ALL
        SELECT 463, 'number of social mobilisers participating the telephone survey','number of social mobilisers participating the telephone survey','number-of-social-mobilisers-participating-the-telephone-survey','number of social mobilisers participating the telephone survey' UNION ALL
        SELECT 56, 'Number of sub-regional units','Number of sub-regional units','number-of-sub-regional-units','Number of sub-regional units' UNION ALL
        SELECT 57, 'Number of sub-regional units where OPV arrived in sufficient time','Number of sub-regional units where OPV arrived in sufficient time','number-of-sub-regional-units-where-opv-arrived-in-sufficient-time','Number of sub-regional units where OPV arrived in time' UNION ALL
        SELECT 70, 'Number of WPV1 cases','Number of WPV1 cases','number-of-wpv-cases','Number of WPV1 cases' UNION ALL
        SELECT 62, 'Number of health facilities w/ capacity','Number of health facilities w/ capacity','number-of-health-facilities-w-capacity','Number of health facilities w/ capacity' UNION ALL
        SELECT 66, 'Number of health facilities having NO stock-outs of OPV','Number of health facilities having NO stock-outs of OPV','number-of-health-facilities-having-no-stock-outs-of-opv','Number of health facilities having NO stock-outs of OPV' UNION ALL
        SELECT 176, 'Number of established LT vaccination transit points with a dedicated social mobilizer','Number of established LT vaccination transit points with a dedicated social mobilizer','1number-of-established-lt-vaccination-transit-points-with-a-dedicated-social-mobilizer','LT Transit Points with SM' UNION ALL
        SELECT 67, 'Percentage of States/Regions with OPV supply arriving at state/region level in sufficient time before campaign','Percentage of States/Regions with OPV supply arriving at state/region level in sufficient time before campaign','percentage-of-statesregions-with-opv-supply-arriving-at-stateregion-level-in-sufficient-time-before-campaign','Percentage of States/Regions with OPV supply arriving a' UNION ALL
        SELECT 470, 'Number of children missed due to all access issues (TEMP)','TEMPORARY INDICATOR','number-of-children-missed-due-to-all-access-issues','Inaccessible Children (TEMP)' UNION ALL
        SELECT 69, 'Number of cVDPV2 cases','Number of cVDPV2 cases','number-of-cvdpv-cases','Number of cVDPV2 cases' UNION ALL
        SELECT 160, 'Number of WPV3 cases','Number of WPV3 cases','number-of-wpv3-cases','Number of WPV3 cases' UNION ALL
        SELECT 161, 'Number of WPV1WPV3 cases','Number of WPV1WPV3 cases','number-of-wpv1wpv3-cases','Number of WPV1WPV3 cases' UNION ALL
        SELECT 51, 'Number of children vaccinated in HRD','Number of children vaccinated in HRD','number-of-children-vaccinated','Number of children vaccinated in HRD' UNION ALL
        SELECT 177, 'Number of children vaccinated at transit points last month','Number of children vaccinated at transit points last month','number-of-children-vaccinated-at-transit-points-last-month','# of children vaccinated at transit points last month' UNION ALL
        SELECT 175, 'Number of established LT vaccination transit points','Number of established LT vaccination transit points ','shed-lt-vaccination-transit-points','LT Transit Points' UNION ALL
        SELECT 95, 'ODK - spec_grp_choice','spec_grp_choice','spec-grp-choice','ODK - spec_grp_choice' UNION ALL
        SELECT 169, 'FRR Funding Level','Percent of FRR funded for the next 6 months','percent-of-frr-funded-for-the-next-6-months','Funding' UNION ALL
        SELECT 192, 'Routine Immunization Defaulter Tracking','Number of routine immunization defaulters tracked and mobilized by SMs last month','number-of-ri-defaulters-mobilized-by-sms-last-month','RI Defaulter Tracking' UNION ALL
        SELECT 179, 'Social Mobilisers and Their Supervisors in Place','Proportion of target social mobilisers and their supervisors in place','percent-of-target-social-mobilizers-and-supervisors-in-place','Mobilisers in Place' UNION ALL
        SELECT 172, 'District OPV Stock Balance Reporting','Percent of high risk districts which reported on balance of SIA vaccine stock after last SIA round','percent-of-high-risk-districts-which-reported-on-balance-of-sia-vaccine-stock-after-last-sia-round','Stock Balance Reporting' UNION ALL
        SELECT 196, 'HR district did NOT receive polio vaccine supply at least 3 days before the planned start date of campaign (1 = yes, 0 = no)','HR district did NOT receive polio vaccine supply at least 3 days before the planned start date of campaign (1 = yes, 0 = no)','hr-district-did-not-receive-polio-vaccine-supply-at-least-3-days-before-the-planned-start-date-of-campaign-1-yes-0-no','HRD did NOT receive OPV supply at least 3d before campa' UNION ALL
        SELECT 199, 'Total number of all active cold chain equipment in district','Total number of all active cold chain equipment in district','total-number-of-all-active-cold-chain-equipment-in-district','Total # of all active cold chain equipment in district' UNION ALL
        SELECT 206, 'Number of social mobilizers and supervisors in place','Number of social mobilizers and supervisors in place','number-of-social-mobilizers-and-supervisors-in-place','# of SMs and supervisors in place' UNION ALL
        SELECT 37, 'Number of vaccination teams with at least one female','Number of vaccination teams with at least one female','number-of-teams-with-at-least-one-female','Number of vaccination teams with at least one female' UNION ALL
        SELECT 210, 'Number of social mobilizers who received on-the-job supervision during their last working week','Number of social mobilizers who received on-the-job supervision during their last working week','number-of-social-mobilizers-who-received-on-the-job-supervision-during-their-last-working-week','# of SMs who received supervision last work week' UNION ALL
        SELECT 211, 'Number of refusals resolved','Number of refusals resolved','number-of-refusals-resolved','Number of refusals resolved' UNION ALL
        SELECT 197, 'District reported on balance of SIA vaccine stocks after last SIA round? (1=yes, 0=no)','District reported on balance of SIA vaccine stocks after last SIA round? (1=yes, 0=no)','district-reported-on-balance-of-SIA-vaccine-stocks-after-last-SIA-round','On balance of SIA vaccine stocks' UNION ALL
        SELECT 213, 'Number of absences before re-visit','Number of absences before re-visit','number-of-absences-before-re-visit','# of absences before re-visit' UNION ALL
        SELECT 214, 'Number of absences after re-visit','Number of absences after re-visit','number-of-absences-after-re-visit','# of absences after re-visit' UNION ALL
        SELECT 216, 'Number of RI sessions monitored having stockouts of any vaccine in the last month','Number of RI sessions monitored having stockouts of any vaccine in the last month','number-of-ri-sessions-monitored-having-stockouts-of-any-vaccine-in-the-last-month','# of RI sessions monitored having stockouts of any vacc' UNION ALL
        SELECT 217, 'Number of RI sessions monitored','Number of RI sessions monitored','number-of-ri-sessions-monitored','Number of RI sessions monitored' UNION ALL
        SELECT 218, 'Number of high risk districts with locations where OPV is delivered together with any other polio-funded services demanded by community','Number of high risk districts with locations where OPV is delivered together with any other polio-funded services demanded by community','number-of-high-risk-districts-with-locations-where-opv-is-delivered-together-with-any-other-polio-funded-services-demanded-by-community','# HRDs with locations where OPV is delivered w services' UNION ALL
        SELECT 174, 'Proportion of access-challenged districts that have had a specific access approach identified','Proportion of access-challenged districts that have had a specific access approach identified','proportion-of-access-challenged-districts-that-have-had-a-specific-access-approach-identified','pct of access-challenged districts with access approach' UNION ALL
        SELECT 189, 'Percent of absences resolved during the previous month (both during campaigns and between rounds)','Percent of absences resolved during the previous month (both during campaigns and between rounds)','percent-of-absences-resolved-during-the-previous-month-both-during-campaigns-and-between-rounds','Absences Conversion' UNION ALL
        SELECT 134, 'ODK - group_spec_events_spec_mslscase','group_spec_events_spec_mslscase','group-spec-events-spec-mslscase','ODK - group_spec_events_spec_mslscase' UNION ALL
        SELECT 202, 'Is an access-challenged district that has a specific access approach identified (1=yes, 0=no)','Is an access-challenged district that has a specific access approach identified (1=yes, 0=no)','is-access-challenged-district-that-has-a-specific-access-approach-identified','Is an access-challenged district w access approach' UNION ALL
        SELECT 203, 'Is an access-challenged district (1=yes, 0=no)','Is an access-challenged district (1=yes, 0=no)','is-access-challenged-district','Is an access-challenged districts' UNION ALL
        SELECT 472, 'Is a high risk district where at least 90pct of active cold chain equipment are functional (1=yes, 0=no)','Is a high risk district where at least 90pct of active cold chain equipment are functional (1=yes, 0=no)','HRD-with-90pct-functional-cold-chain','HRD with 90pct functional cold chain' UNION ALL
        SELECT 219, 'OPV Wastage between 5pct and 15pct','Proportion of high risk districts where polio vaccine wastage rate in SIAs is between 5 and 15pct, calculated from the number of children vaccinated and the number of vaccines used, as recorded in vaccinator tally sheet','percent-high-risk-districts-where-polio-vaccine-wastage-rate-in-sias-is-between-5-and-15','Acceptable OPV Wastage' UNION ALL
        SELECT 193, 'OPV Delivery with Other Polio-Funded Services','Percent of HRDs where OPV is delivered together with any other polio-funded services demanded by the community','percent-of-hrds-with-locations-where-opv-is-delivered-together-with-any-other-polio-funded-services-demanded-by-the-community','Polio-Plus Activities' UNION ALL
        SELECT 475, 'Missed Children','Proportion of children missed among all target children, according to independent monitoring (post campaign assessment) data or polio control room data','missed-children-out-of-children-targeted','pct Missed Children' UNION ALL
        SELECT 180, 'Vaccinator from Local Community','Percent of vaccination teams in which at least 1 member is from local community in high risk areas','percent-of-vaccination-teams-in-which-at-least-1-member-is-from-local-community-in-high-risk-areas','Local Vaccinators' UNION ALL
        SELECT 204, 'Total number of LT vaccination transit points planned by the programme','Total number of LT vaccination transit points planned by the programme','total-number-of-lt-vaccination-transit-points-planned-by-the-programme','Total # of LT transit points planned by the programme' UNION ALL
        SELECT 207, 'Target number of social mobilizers and supervisors','Target number of social mobilizers and supervisors','target-number-of-social-mobilizers-and-supervisors','Target # of SMs and supervisors' UNION ALL
        SELECT 215, 'Number of absences resolved','Number of absences resolved','number-of-absences-resolved','Number of absences resolved' UNION ALL
        SELECT 81, 'ODK - Total Vaccinated Newborns Male','vaxnewbornsm','vaxnewbornsm','ODK - Total Vaccinated Newborns Male' UNION ALL
        SELECT 82, 'ODK - Total Vaccinated Newborns Female','vaxnewbornsf','vaxnewbornsf','ODK - Total Vaccinated Newborns Female' UNION ALL
        SELECT 89, 'ODK - Total Vaccinated Newborns','tot_vaxnewborn','tot-vaxnewborn','ODK - Total Vaccinated Newborns' UNION ALL
        SELECT 86, 'ODK - Total Vaccinated 2 to 11 months','tot_vax2_11mo','tot-vax2-11mo','ODK - Total Vaccinated 2 to 11 months' UNION ALL
        SELECT 88, 'ODK - Total Vaccinated 12 to 59 months','tot_vax12_59mo','tot-vax12-59mo','ODK - Total Vaccinated 12 to 59 months' UNION ALL
        SELECT 78, 'ODK - Total Vaccinated  2-11 months male','vax2_11mom','vax2-11mom','ODK - Total Vaccinated  2-11 months male' UNION ALL
        SELECT 77, 'ODK - Total Vaccinated  2-11 months Female','vax2_11mof','vax2-11mof','ODK - Total Vaccinated  2-11 months Female' UNION ALL
        SELECT 80, 'ODK - Total Vaccinated  12-59 months male','vax12_59mof','vax12-59mof','ODK - Total Vaccinated  12-59 months male' UNION ALL
        SELECT 79, 'ODK - Total Vaccinated  12-59 months Female','vax12_59mom','vax12-59mom','ODK - Total Vaccinated  12-59 months Female' UNION ALL
        SELECT 74, 'ODK - Total Vaccinated','tot_vax','tot-vax','ODK - Total Vaccinated' UNION ALL
        SELECT 83, 'ODK - Total Newborns','tot_newborns','tot-newborns','ODK - Total Newborns' UNION ALL
        SELECT 136, 'ODK - Total Missed Due to Unhappy with Team Male','group_msd_chd_msd_unhappywteamm','group-msd-chd-msd-unhappywteamm','ODK - Total Missed Due to Unhappy with Team Male' UNION ALL
        SELECT 137, 'ODK - Total Missed Due to Unhappy with Team Female','group_msd_chd_msd_unhappywteamf','group-msd-chd-msd-unhappywteamf','ODK - Total Missed Due to Unhappy with Team Female' UNION ALL
        SELECT 141, 'ODK - Total Missed Due to Too Many Rounds Male','group_msd_chd_msd_toomanyroundsm','group-msd-chd-msd-toomanyroundsm','ODK - Total Missed Due to Too Many Rounds Male' UNION ALL
        SELECT 140, 'ODK - Total Missed Due to Too Many Rounds Female','group_msd_chd_msd_toomanyroundsf','group-msd-chd-msd-toomanyroundsf','ODK - Total Missed Due to Too Many Rounds Female' UNION ALL
        SELECT 109, 'ODK - Total Missed Due to Social Event Male','group_msd_chd_msd_soceventm','group-msd-chd-msd-soceventm','ODK - Total Missed Due to Social Event Male' UNION ALL
        SELECT 110, 'ODK - Total Missed Due to Social Event Female','group_msd_chd_msd_soceventf','group-msd-chd-msd-soceventf','ODK - Total Missed Due to Social Event Female' UNION ALL
        SELECT 129, 'ODK - Total Missed Due to Side Effects Male','group_msd_chd_msd_sideeffectsm','group-msd-chd-msd-sideeffectsm','ODK - Total Missed Due to Side Effects Male' UNION ALL
        SELECT 128, 'ODK - Total Missed Due to Side Effects Female','group_msd_chd_msd_sideeffectsf','group-msd-chd-msd-sideeffectsf','ODK - Total Missed Due to Side Effects Female' UNION ALL
        SELECT 107, 'ODK - Total Missed Due to Security Male','group_msd_chd_msd_securitym','group-msd-chd-msd-securitym','ODK - Total Missed Due to Security Male' UNION ALL
        SELECT 108, 'ODK - Total Missed Due to Security Female','group_msd_chd_msd_securityf','group-msd-chd-msd-securityf','ODK - Total Missed Due to Security Female' UNION ALL
        SELECT 122, 'ODK - Total Missed Due to Religions Beliefs Male','group_msd_chd_msd_relbeliefsm','group-msd-chd-msd-relbeliefsm','ODK - Total Missed Due to Religions Beliefs Male' UNION ALL
        SELECT 119, 'ODK - Total Missed Due to Religions Beliefs Female','group_msd_chd_msd_relbeliefsf','group-msd-chd-msd-relbeliefsf','ODK - Total Missed Due to Religions Beliefs Female' UNION ALL
        SELECT 142, 'ODK - Total Missed Due to Polio uncommon Male','group_msd_chd_msd_poliouncommonm','group-msd-chd-msd-poliouncommonm','ODK - Total Missed Due to Polio uncommon Male' UNION ALL
        SELECT 143, 'ODK - Total Missed Due to Polio uncommon Female','group_msd_chd_msd_poliouncommonf','group-msd-chd-msd-poliouncommonf','ODK - Total Missed Due to Polio uncommon Female' UNION ALL
        SELECT 133, 'ODK - Total Missed Due to Polio Has Cure Male','group_msd_chd_msd_poliohascurem','group-msd-chd-msd-poliohascurem','ODK - Total Missed Due to Polio Has Cure Male' UNION ALL
        SELECT 132, 'ODK - Total Missed Due to Polio Has Cure Female','group_msd_chd_msd_poliohascuref','group-msd-chd-msd-poliohascuref','ODK - Total Missed Due to Polio Has Cure Female' UNION ALL
        SELECT 148, 'ODK - Total Missed Due to Other Protection Male','group_msd_chd_msd_otherprotectionm','group-msd-chd-msd-otherprotectionm','ODK - Total Missed Due to Other Protection Male' UNION ALL
        SELECT 147, 'ODK - Total Missed Due to Other Protection Female','group_msd_chd_msd_otherprotectionf','group-msd-chd-msd-otherprotectionf','ODK - Total Missed Due to Other Protection Female' UNION ALL
        SELECT 105, 'ODK - Total Missed Due to No Plusses Male','group_msd_chd_msd_noplusesm','group-msd-chd-msd-noplusesm','ODK - Total Missed Due to No Plusses Male' UNION ALL
        SELECT 106, 'ODK - Total Missed Due to No Plusses Female','group_msd_chd_msd_noplusesf','group-msd-chd-msd-noplusesf','ODK - Total Missed Due to No Plusses Female' UNION ALL
        SELECT 145, 'ODK - Total Missed Due to No Government Services Male','group_msd_chd_msd_nogovtservicesm','group-msd-chd-msd-nogovtservicesm','ODK - Total Missed Due to No Government Services Male' UNION ALL
        SELECT 146, 'ODK - Total Missed Due to No Government Services Female','group_msd_chd_msd_nogovtservicesf','group-msd-chd-msd-nogovtservicesf','ODK - Total Missed Due to No Government Services Female' UNION ALL
        SELECT 194, 'District Had Delayed OPV Supply','Percent of High Risk Districts that did not receive polio vaccine supply at least 3 days before the planned starting date of the campaign','percent-of-hrds-that-did-not-receive-polio-vaccine-supply-at-least-3-days-before-the-planned-starting-date-of-the-campaign','Delayed OPV Supply' UNION ALL
        SELECT 117, 'ODK - Total Missed Due to No Consent Male','group_msd_chd_msd_noconsentm','group-msd-chd-msd-noconsentm','ODK - Total Missed Due to No Consent Male' UNION ALL
        SELECT 118, 'ODK - Total Missed Due to No Consent Female','group_msd_chd_msd_noconsentf','group-msd-chd-msd-noconsentf','ODK - Total Missed Due to No Consent Female' UNION ALL
        SELECT 139, 'ODK - Total Missed Due to Household not visited Male','group_msd_chd_msd_hhnotvisitedm','group-msd-chd-msd-hhnotvisitedm','ODK - Total Missed Due to Household not visited Male' UNION ALL
        SELECT 138, 'ODK - Total Missed Due to Household not visited Female','group_msd_chd_msd_hhnotvisitedf','group-msd-chd-msd-hhnotvisitedf','ODK - Total Missed Due to Household not visited Female' UNION ALL
        SELECT 121, 'ODK - Total Missed Due to Felt Not Needed Male','group_msd_chd_msd_nofeltneedm','group-msd-chd-msd-nofeltneedm','ODK - Total Missed Due to Felt Not Needed Male' UNION ALL
        SELECT 120, 'ODK - Total Missed Due to Felt Not Needed Female','group_msd_chd_msd_nofeltneedf','group-msd-chd-msd-nofeltneedf','ODK - Total Missed Due to Felt Not Needed Female' UNION ALL
        SELECT 131, 'ODK - Total Missed Due to Family Moved Male','group_msd_chd_msd_familymovedm','group-msd-chd-msd-familymovedm','ODK - Total Missed Due to Family Moved Male' UNION ALL
        SELECT 130, 'ODK - Total Missed Due to Family Moved Female','group_msd_chd_msd_familymovedf','group-msd-chd-msd-familymovedf','ODK - Total Missed Due to Family Moved Female' UNION ALL
        SELECT 101, 'ODK - Total Missed Due to Children at Schools Male','group_msd_chd_msd_schoolm','group-msd-chd-msd-schoolm','ODK - Total Missed Due to Children at Schools Male' UNION ALL
        SELECT 100, 'ODK - Total Missed Due to Children at Schools Female','group_msd_chd_msd_schoolf','group-msd-chd-msd-schoolf','ODK - Total Missed Due to Children at Schools Female' UNION ALL
        SELECT 115, 'ODK - Total Missed Due to Child Sick Male','group_msd_chd_msd_childsickm','group-msd-chd-msd-childsickm','ODK - Total Missed Due to Child Sick Male' UNION ALL
        SELECT 116, 'ODK - Total Missed Due to Child Sick Female','group_msd_chd_msd_childsickf','group-msd-chd-msd-childsickf','ODK - Total Missed Due to Child Sick Female' UNION ALL
        SELECT 96, 'ODK - Total Missed Due to Child on Farm Male','group_msd_chd_msd_farmm','group-msd-chd-msd-farmm','ODK - Total Missed Due to Child on Farm Male' UNION ALL
        SELECT 97, 'ODK - Total Missed Due to Child on Farm Female','group_msd_chd_msd_farmf','group-msd-chd-msd-farmf','ODK - Total Missed Due to Child on Farm Female' UNION ALL
        SELECT 114, 'ODK - Total Missed Due to Child Died Male','group_msd_chd_msd_childdiedm','group-msd-chd-msd-childdiedm','ODK - Total Missed Due to Child Died Male' UNION ALL
        SELECT 123, 'ODK - Total Missed Due to Child at Playground Male','group_msd_chd_msd_playgroundm','group-msd-chd-msd-playgroundm','ODK - Total Missed Due to Child at Playground Male' UNION ALL
        SELECT 124, 'ODK - Total Missed Due to Child at Playground Female','group_msd_chd_msd_playgroundf','group-msd-chd-msd-playgroundf','ODK - Total Missed Due to Child at Playground Female' UNION ALL
        SELECT 98, 'ODK - Total Missed Due to Child at Market Male','group_msd_chd_msd_marketm','group-msd-chd-msd-marketm','ODK - Total Missed Due to Child at Market Male' UNION ALL
        SELECT 99, 'ODK - Total Missed Due to Child at Market Female','group_msd_chd_msd_marketf','group-msd-chd-msd-marketf','ODK - Total Missed Due to Child at Market Female' UNION ALL
        SELECT 102, 'ODK - Total missed due to Aged Out Male','group_msd_chd_msd_agedoutm','group-msd-chd-msd-agedoutm','ODK - Total missed due to Aged Out Male' UNION ALL
        SELECT 103, 'ODK - Total missed due to Aged Out Female','group_msd_chd_msd_agedoutf','group-msd-chd-msd-agedoutf','ODK - Total missed due to Aged Out Female' UNION ALL
        SELECT 113, 'ODK - Total Missed Due to  Child Died Female','group_msd_chd_msd_childdiedf','group-msd-chd-msd-childdiedf','ODK - Total Missed Due to  Child Died Female' UNION ALL
        SELECT 76, 'ODK - Total Missed','tot_missed','tot-missed','ODK - Total Missed' UNION ALL
        SELECT 90, 'ODK - Total Children 2 to 11 months','tot_2_11months','tot-2-11months','ODK - Total Children 2 to 11 months' UNION ALL
        SELECT 92, 'ODK - Total children 12 to 59 Months','tot_12_59months','tot-12-59months','ODK - Total children 12 to 59 Months' UNION ALL
        SELECT 75, 'ODK - Total Census','tot_census','tot-census','ODK - Total Census' UNION ALL
        SELECT 127, 'ODK - group_msd_chd_tot_missed_check','group_msd_chd_tot_missed_check','group-msd-chd-tot-missed-check','ODK - group_msd_chd_tot_missed_check' UNION ALL
        SELECT 84, 'ODK - Census 2 to 11 months Male','census2_11mom','census2-11mom','ODK - Census 2 to 11 months Male' UNION ALL
        SELECT 85, 'ODK - Census 2 to 11 months Female','census2_11mof','census2-11mof','ODK - Census 2 to 11 months Female' UNION ALL
        SELECT 87, 'ODK - Census 12 to 59 months Male','census12_59mom','census12-59mom','ODK - Census 12 to 59 months Male' UNION ALL
        SELECT 91, 'ODK - Census 12 to 59 months Female','census12_59mof','census12-59mof','ODK - Census 12 to 59 months Female' UNION ALL
        SELECT 94, 'ODK - Census  Newborns Male','censusnewbornsm','censusnewbornsm','ODK - Census  Newborns Male' UNION ALL
        SELECT 111, 'ODK - group_msd_chd_msd_poldiffsm','group_msd_chd_msd_poldiffsm','group-msd-chd-msd-poldiffsm','ODK - group_msd_chd_msd_poldiffsm' UNION ALL
        SELECT 126, 'ODK - group_spec_events_spec_afpcase','group_spec_events_spec_afpcase','group-spec-events-spec-afpcase','ODK - group_spec_events_spec_afpcase' UNION ALL
        SELECT 149, 'ODK - group_spec_events_spec_cmamreferral','group_spec_events_spec_cmamreferral','group-spec-events-spec-cmamreferral','ODK - group_spec_events_spec_cmamreferral' UNION ALL
        SELECT 104, 'ODK - group_spec_events_spec_fic','group_spec_events_spec_fic','group-spec-events-spec-fic','ODK - group_spec_events_spec_fic' UNION ALL
        SELECT 125, 'ODK - group_spec_events_spec_newborn','group_spec_events_spec_newborn','group-spec-events-spec-newborn','ODK - group_spec_events_spec_newborn' UNION ALL
        SELECT 150, 'ODK - group_spec_events_spec_otherdisease','group_spec_events_spec_otherdisease','group-spec-events-spec-otherdisease','ODK - group_spec_events_spec_otherdisease' UNION ALL
        SELECT 151, 'ODK - group_spec_events_spec_pregnantmother','group_spec_events_spec_pregnantmother','group-spec-events-spec-pregnantmother','ODK - group_spec_events_spec_pregnantmother' UNION ALL
        SELECT 144, 'ODK - group_spec_events_spec_rireferral','group_spec_events_spec_rireferral','group-spec-events-spec-rireferral','ODK - group_spec_events_spec_rireferral' UNION ALL
        SELECT 152, 'ODK - group_spec_events_spec_vcmattendedncer','group_spec_events_spec_vcmattendedncer','group-spec-events-spec-vcmattendedncer','ODK - group_spec_events_spec_vcmattendedncer' UNION ALL
        SELECT 135, 'ODK - group_spec_events_spec_zerodose','group_spec_events_spec_zerodose','group-spec-events-spec-zerodose','ODK - group_spec_events_spec_zerodose' UNION ALL
        SELECT 274, 'Outside_Percent missed children','Outside_Percent missed children','outside_percent-missed-children','Not Marked' UNION ALL
        SELECT 198, 'Number of functional active cold chain equipment in the district','Number of functional active cold chain equipment in the district','number-of-functional-active-cold-chain-equipment','# functional active cold chain equipment in district' UNION ALL
        SELECT 201, 'District has specific access approach identified (1=yes, 0=no)','District has specific access approach identified (1=yes, 0=no)','district-has-specific-access-approach-identified-1yes-0no','District has specific access approach identified' UNION ALL
        SELECT 208, 'Number of vaccination teams with at least 1 member from the local community','Number of vaccination teams with at least 1 member from the local community','number-of-vaccination-teams-with-at-least-1-member-from-the-local-community','# of vaccination teams with at least 1 local member' UNION ALL
        SELECT 209, 'Number of social mobilizers trained or refreshed with the integrated health package in the last 6 months','Number of social mobilizers trained or refreshed with the integrated health package in the last 6 months','number-of-social-mobilizers-trained-or-refreshed-with-the-integrated-health-package-in-the-last-6-months','# SMs trained, refreshed w. health package in last 6 mo' UNION ALL
        SELECT 55, 'Number of children targeted in high-risk districts','Number of children targeted in high-risk districts','number-of-targeted-under-five-children','Number of children targeted in HRDs' UNION ALL
        SELECT 220, 'Vaccine wastage rate','Vaccine wastage rate','vaccine-wastage-rate','Vaccine wastage rate' UNION ALL
        SELECT 33, 'Number of high risk sub-districts','Number of high risk sub-districts ','number-of-high-risk-areas-targeted-2','Number of high risk sub-districts ' UNION ALL
        SELECT 195, 'Is a high risk district? (1=yes, 0=no)','Is a high risk district? (1=yes, 0=no)','is-a-high-risk-district','Is high risk?' UNION ALL
        SELECT 254, 'Endprocess_NOimmReas10 - Fear of OPV side effects','Endprocess_NOimmReas10 - Fear of OPV side effects','endprocess_noimmreas10-fear-of-opv-side-effects','Fear of Side Effects' UNION ALL
        SELECT 221, 'Is an HRD that has polio vaccine wastage rate in SIAs between 5 and 15pct (1=yes, 0=no)','Is an HRD that has polio vaccine wastage rate in SIAs between 5 and 15pct (1=yes, 0=no)','hrd-that-has-polio-vaccine-wastage-rate-in-sias-between-5-and-15','Is an that has polio vaccine wastage btwn 5-15pct' UNION ALL
        SELECT 224, 'Percentage of established LT vaccination transit points with a dedicated social mobilizer, out of total number established by the programme','Percentage of established LT vaccination transit points with a dedicated social mobilizer, out of total number established by the programme','percentage-of-established-lt-vaccination-transit-points-with-a-dedicated-social-mobilizer,-vs.-total-number-established-by-the-programme','Percentage of established LT vaccination transit points with a dedicated social mobilizer, out of total number established by the programme' UNION ALL
        SELECT 222, 'Percentage of districts with microplans that passed review (out of districts sampled)','Percentage of districts with microplans that passed review (out of districts sampled)','percentage-of-districts-with-microplans-that-passed-review','Percentage of districts with microplans that passed review' UNION ALL
        SELECT 191, 'Routine Immunization Session Stockout','Proprotion of routine immunization sessions monitored having stockouts of any vaccine during last month','percent-of-ri-sessions-monitored-having-stockouts-of-any-vaccine-during-last-month','RI Stockouts' UNION ALL
        SELECT 178, 'Geographic Coverage by Social Mobilisers','Proportion of High-Risk sub-districts covered by social mobilisers','percent-of-hr-sub-districts-covered-by-social-mobilizers','Mobiliser Coverage' UNION ALL
        SELECT 184, 'Social Mobilisers Training in Integrated Health Package','Proportion of social mobilisers trained or refreshed with the integrated health package in the last 6 months','percent-of-social-mobilizers-trained-or-refreshed-with-the-integrated-health-package-in-the-last-6-months','Mobiliser Training on Polio+' UNION ALL
        SELECT 250, 'Endprocess_NOimmReas7 - Child at school','Endprocess_NOimmReas7 - Child at school','endprocess_noimmreas7-child-at-school','School ' UNION ALL
        SELECT 273, ' Not Marked',' Not Marked','-not-marked','Missed (Outside)' UNION ALL
        SELECT 272, 'Endprocess_Percent missed children','Endprocess_Percent missed children','endprocess_percent-missed-children','Missed Children' UNION ALL
        SELECT 247, 'Endprocess_NoimmReas4 - Child at social event','Endprocess_NoimmReas4 - Child at social event','endprocess_noimmreas4-child-at-social-event','Social Event ' UNION ALL
        SELECT 249, 'Endprocess_NOimmReas6 - Child at farm','Endprocess_NOimmReas6 - Child at farm','endprocess_noimmreas6-child-at-farm','Farm ' UNION ALL
        SELECT 242, 'Number of vaccine doses wasted','Number of vaccine doses wasted','number-of-vaccine-doses-wasted','Number of vaccine doses wasted' UNION ALL
        SELECT 243, 'Number of children 12 months and under','Number of children 12 months and under','number-of-children-12-months-and-under','Number of children 12 months and under' UNION ALL
        SELECT 244, 'Number of children under 12 months who received DPT3 or Penta3','Number of children under 12 months who received DPT3 or Penta3','number-of-children-under-12-months-who-received-dpt3-or-penta3','No. of children under 12 months who received RI' UNION ALL
        SELECT 248, 'Endprocess_NOimmReas5 - Child at market','Endprocess_NOimmReas5 - Child at market','endprocess_noimmreas5-child-at-market','Market ' UNION ALL
        SELECT 246, 'Endprocess_NOimmReas3 - Child at playground','Endprocess_NOimmReas3 - Child at playground','endprocess_noimmreas3-child-at-playground','Playground ' UNION ALL
        SELECT 253, 'Endprocess_NOimmReas9 - Too many rounds','Endprocess_NOimmReas9 - Too many rounds','endprocess_noimmreas9-too-many-rounds','Too Many Rounds ' UNION ALL
        SELECT 263, 'Endprocess_NOimmReas19 - No caregiver consent','Endprocess_NOimmReas19 - No caregiver consent','endprocess_noimmreas19-no-caregiver-consent','No Consent' UNION ALL
        SELECT 251, 'Endprocess_Reason for missed children - child absent','Endprocess_Reason for missed children - child absent','endprocess_reason-for-missed-children-child-absent','Child Absent' UNION ALL
        SELECT 252, 'Endprocess_NOimmReas8 - Child sick','Endprocess_NOimmReas8 - Child sick','endprocess_noimmreas8-child-sick','Child Sick' UNION ALL
        SELECT 236, 'Caregiver Knowledge of Routine Immunization','Proportion of caregivers in HRDs who know number of times they need to visit a RI site for routine immunization before a child reaches 1 year of age','pct-of-caregivers-in-hrds-who-know-number-of-times-they-need-to-visit-the-ri-site-for-routine-immunization-before-a-child-reaches-1-year-of-age','Knowledge of RI' UNION ALL
        SELECT 239, 'Female Social Moblisers in Place','Proportion of female social mobilisers among social mobilisers in place','pct-of-female-social-mobilisers-among-social-mobilizers-in-place','Female Mobilisers' UNION ALL
        SELECT 185, 'On-the-Job Supervision of Social Mobilisers','Proportion of social mobilisers who received on-the-job supervision during their last working week','percent-of-social-mobilizers-who-received-on-the-job-supervision-during-their-last-working-week','Mobiliser Supervision' UNION ALL
        SELECT 226, 'Timely Payment to Social Mobilisers','Proportion of social mobilisers who received timely payment for last campaign/month''s salary among ALL social mobilisers involved in the campaign.','pct-of-social-mobilizers-who-received-timely-payment-for-last-campaignmonths-salary-among-all-social-mobilisers-involved-in-the-campaign','Timely Mobiliser Payment' UNION ALL
        SELECT 228, 'Vaccinator Training in Inter-Personal Communication Skills','Proportion of vaccinators operating in HRD who have been trained on professional Inter Personal Communication package provided by UNICEF in the last 6 months','pct-of-vaccinators-operating-in-hrd-who-have-been-trained-on-professional-inter-personal-communication-package-provided-by-unicef-in-the-last-6-months','Vaccinator Training on IPC Skills' UNION ALL
        SELECT 230, 'Female Vaccinator in Team','Proportion of vaccination teams in which at least one member is female in HR areas','pct-of-vaccination-teams-in-which-at-least-one-member-is-female-in-hr-areas','Female Vaccinators' UNION ALL
        SELECT 476, '(TW Test) Infected People','How many people infected?','tw-test-infected-people','tw-test-outbreak-infected-people' UNION ALL
        SELECT 477, 'TW Test Outbreak Infected People','TW Test Outbreak Infected People','tw-test-outbreak-infected-people','TW Test Outbreak Infected People' UNION ALL
        SELECT 279, 'Endprocess_Influence5 - Radio','Endprocess_Influence5 - Radio','endprocess_influence5-radio','Radio   ' UNION ALL
        SELECT 258, 'Endprocess_NOimmReas14 - Religious belief','Endprocess_NOimmReas14 - Religious belief','endprocess_noimmreas14-religious-belief','Religious Beliefs ' UNION ALL
        SELECT 288, 'Endprocess_Percent vaccination influencer is radio','Endprocess_Percent vaccination influencer is radio','endprocess_percent-vaccination-influencer-is-radio','Radio ' UNION ALL
        SELECT 266, 'Endprocess_NOimmReas20 - Security','Endprocess_NOimmReas20 - Security','endprocess_noimmreas20-security','Security ' UNION ALL
        SELECT 269, 'Endprocess_Number of children 0 to 59 marked','Endprocess_Number of children 0 to 59 marked','endprocess_number-of-children-0-to-59-marked','Endprocess_Marked0to59' UNION ALL
        SELECT 270, 'Endprocess_Number of children 0 to 59 unimmunized','Endprocess_Number of children 0 to 59 unimmunized','endprocess_number-of-children-0-to-59-unimmunized','Endprocess_UnImmun0to59' UNION ALL
        SELECT 271, 'Endprocess_Number of children seen','Endprocess_Number of children seen','endprocess_number-of-children-seen','Endprocess_Number of children seen' UNION ALL
        SELECT 275, ' seen',' seen','-seen',' seen' UNION ALL
        SELECT 287, 'Endprocess_Percent vaccination influencer is personal decision','Endprocess_Percent vaccination influencer is personal decision','endprocess_percent-vaccination-influencer-is-personal-decision','Personal Decision' UNION ALL
        SELECT 277, 'Endprocess_Not aware','Endprocess_Not aware','endprocess_not-aware','Endprocess_Not aware' UNION ALL
        SELECT 285, 'Endprocess_Influence8 - Vaccinator','Endprocess_Influence8 - Vaccinator','endprocess_influence8-vaccinator','Vaccinator ' UNION ALL
        SELECT 260, 'Endprocess_NOimmReas16 - Unhappy with vaccination team','Endprocess_NOimmReas16 - Unhappy with vaccination team','endprocess_noimmreas16-unhappy-with-vaccination-team','Unhappy with Team' UNION ALL
        SELECT 291, 'Endprocess_Percent vaccination influencer is traditional leader','Endprocess_Percent vaccination influencer is traditional leader','endprocess_percent-vaccination-influencer-is-traditional-leader','Trad. Leader' UNION ALL
        SELECT 282, 'Endprocess_Influence3 - Traditional leader','Endprocess_Influence3 - Traditional leader','endprocess_influence3-traditional-leader','Trad. Leader   ' UNION ALL
        SELECT 293, 'Endprocess_Percent vaccination influencer is religious leader','Endprocess_Percent vaccination influencer is religious leader','endprocess_percent-vaccination-influencer-is-religious-leader','Rel. Leader' UNION ALL
        SELECT 284, 'Endprocess_Influence4 - Religious leader','Endprocess_Influence4 - Religious leader','endprocess_influence4-religious-leader','Rel. Leader   ' UNION ALL
        SELECT 290, 'Endprocess_Percent vaccination influencer is neighbour','Endprocess_Percent vaccination influencer is neighbour','endprocess_percent-vaccination-influencer-is-neighbour','Neighbour ' UNION ALL
        SELECT 265, 'Endprocess_Missed children - All reasons','Endprocess_Missed children - All reasons','endprocess_missed-children-all-reasons','Missed (Inside)' UNION ALL
        SELECT 286, 'Endprocess_All vaccination influencers','Endprocess_All vaccination influencers','endprocess_all-vaccination-influencers','Endprocess_All vaccination influencers' UNION ALL
        SELECT 289, 'Endprocess_Percent vaccination influencer is husband','Endprocess_Percent vaccination influencer is husband','endprocess_percent-vaccination-influencer-is-husband','Husband' UNION ALL
        SELECT 173, 'Cold Chain Functional Status','Proportion of high risk districts where at least 90pct of active cold chain equipment are functional','percent-of-high-risk-districts-where-at-least-90-of-active-cold-chain-equipment-are-functional','Cold Chain Functional Status' UNION ALL
        SELECT 276, 'Endprocess_Percent caregiver awareness','Endprocess_Percent caregiver awareness','percent-caregiver-awareness','Caregiver Awareness' UNION ALL
        SELECT 283, 'Endprocess_Influence7 - Community mobiliser','Endprocess_Influence7 - Community mobiliser','endprocess_influence7-community-mobiliser','Comm. Mobiliser ' UNION ALL
        SELECT 292, 'Endprocess_Pct vaccination influencer is community mobiliser','Endprocess_Pct vaccination influencer is community mobiliser','endprocess_pct-vaccination-influencer-is-community-mobiliser','Comm. Mobiliser  ' UNION ALL
        SELECT 280, 'Endprocess_Influence2 - Husband','Endprocess_Influence2 - Husband','endprocess_influence2-husband','Husband ' UNION ALL
        SELECT 281, 'Endprocess_Influence6 - Neighbour','Endprocess_Influence6 - Neighbour','endprocess_influence6-neighbour','Neighbour  ' UNION ALL
        SELECT 262, 'Endprocess_NOimmReas18 - No felt need','Endprocess_NOimmReas18 - No felt need','endprocess_noimmreas18-no-felt-need','No Felt Needed' UNION ALL
        SELECT 264, 'Endprocess_Reason for missed children - Non compliance','Endprocess_Reason for missed children - Non compliance','endprocess_reason-for-missed-children-non-compliance','Non-Comp. ' UNION ALL
        SELECT 261, 'Endprocess_NOimmReas17 - No pluses given','Endprocess_NOimmReas17 - No pluses given','endprocess_noimmreas17-no-pluses-given','No Pluses ' UNION ALL
        SELECT 267, 'Endprocess_NOimmReas1 - Household not in microplan','Endprocess_NOimmReas1 - Household not in microplan','endprocess_noimmreas1-household-not-in-microplan','Not in Plan ' UNION ALL
        SELECT 268, 'Endprocess_NOimmReas2 - Household in microplan but not visited','Endprocess_NOimmReas2 - Household in microplan but not visited','endprocess_noimmreas2-household-in-microplan-but-not-visited','Not Visited ' UNION ALL
        SELECT 278, 'Endprocess_Influence1 - Personal decision','Endprocess_Influence1 - Personal decision','endprocess_influence1-personal-decision','Personal Decision ' UNION ALL
        SELECT 256, 'Endprocess_NOimmReas12 - Polio has cure','Endprocess_NOimmReas12 - Polio has cure','endprocess_noimmreas12-polio-has-cure','Polio has Cure ' UNION ALL
        SELECT 259, 'Endprocess_NOimmReas15 - Political differences','Endprocess_NOimmReas15 - Political differences','endprocess_noimmreas15-political-differences','Political ' UNION ALL
        SELECT 307, 'Endprocess_Percent source of info is town announcer','Endprocess_Percent source of info is town announcer','endprocess_percent-source-of-info-is-town-announcer','Town Announcer' UNION ALL
        SELECT 324, 'Endprocess_Pct of children absent due to child at social event','Endprocess_Pct of children absent due to child at social event','12pct-of-children-absent-due-to-child-at-social-event','Social Event' UNION ALL
        SELECT 322, 'Endprocess_Pct missed children due to security','Endprocess_Pct missed children due to security','endprocess_pct-missed-children-due-to-security','Security' UNION ALL
        SELECT 296, 'Endprocess_Source of info on IPDs - Radio','Endprocess_Source of info on IPDs - Radio','endprocess_source-of-info-on-ipds-radio','Radio  ' UNION ALL
        SELECT 303, 'Endprocess_Source of info on IPDs - Relative','Endprocess_Source of info on IPDs - Relative','endprocess_source-of-info-on-ipds-relative','Relative ' UNION ALL
        SELECT 306, 'Endprocess_All sources of info on IPDs','Endprocess_All sources of info on IPDs','endprocess_all-sources-of-info-on-ipds','Endprocess_All sources of info on IPDs' UNION ALL
        SELECT 309, 'Endprocess_Percent source of info is relative','Endprocess_Percent source of info is relative','endprocess_percent-source-of-info-is-relative','Relative' UNION ALL
        SELECT 295, 'Endprocess_Source of info on IPDs - Town announcer','Endprocess_Source of info on IPDs - Town announcer','endprocess_source-of-info-on-ipds-town-announcer','Town Announcer ' UNION ALL
        SELECT 310, 'Endprocess_Percent source of info is radio','Endprocess_Percent source of info is radio','endprocess_percent-source-of-info-is-radio','Radio' UNION ALL
        SELECT 314, 'Endprocess_Percent source of info is poster','Endprocess_Percent source of info is poster','endprocess_percent-source-of-info-is-poster','Poster' UNION ALL
        SELECT 323, 'Endprocess_Pct of children absent due to playground','Endprocess_Pct of children absent due to playground','pct-chdrn-absent-due-to-playground','Playground' UNION ALL
        SELECT 319, 'Endprocess_Pct missed children due to HH in plan but not visited','Endprocess_Pct missed children due to HH in plan but not visited','endprocess_pct-missed-children-due-to-hh-in-plan-but-not-visited','Not Visited' UNION ALL
        SELECT 321, 'Endprocess_Pct missed children due to non compliance','Endprocess_Pct missed children due to non compliance','endprocess_pct-missed-children-due-to-non-compliance','Non-Comp.' UNION ALL
        SELECT 311, 'Endprocess_Percent source of info is newspaper','Endprocess_Percent source of info is newspaper','endprocess_percent-source-of-info-is-newspaper','Newspaper' UNION ALL
        SELECT 308, 'Endprocess_Percent source of info is mosque announcement','Endprocess_Percent source of info is mosque announcement','endprocess_percent-source-of-info-is-mosque-announcement','Mosque' UNION ALL
        SELECT 313, 'Endprocess_Percent source of info is traditional leader','Endprocess_Percent source of info is traditional leader','endprocess_percent-source-of-info-is-traditional-leader','Trad. Leader  ' UNION ALL
        SELECT 325, 'Endprocess_Pct of children absent due to child at market','Endprocess_Pct of children absent due to child at market','pct-absent-due-to-child-at-market','Market' UNION ALL
        SELECT 318, 'Endprocess_Percent missed children due to HH not in plan','Endprocess_Percent missed children due to HH not in plan','endprocess_percent-missed-children-due-to-hh-not-in-plan','Not in Plan' UNION ALL
        SELECT 297, 'Endprocess_Source of info on IPDs - Traditional leader','Endprocess_Source of info on IPDs - Traditional leader','endprocess_source-of-info-on-ipds-traditional-leader','Trad. Leader ' UNION ALL
        SELECT 312, 'Endprocess_Percent source of info is health worker','Endprocess_Percent source of info is health worker','endprocess_percent-source-of-info-is-health-worker','Health Worker' UNION ALL
        SELECT 316, 'Endprocess_Percent source of info is religious leader','Endprocess_Percent source of info is religious leader','endprocess_percent-source-of-info-is-religious-leader','Rel. Leader ' UNION ALL
        SELECT 315, 'Endprocess_Percent source of info is community mobiliser','Endprocess_Percent source of info is community mobiliser','endprocess_percent-source-of-info-is-community-mobiliser','Comm. Mobiliser' UNION ALL
        SELECT 298, 'Endprocess_Source of info on IPDs - Religious leader','Endprocess_Source of info on IPDs - Religious leader','endprocess_source-of-info-on-ipds-religious-leader','Rel. Leader  ' UNION ALL
        SELECT 320, 'Endprocess_Pct missed children due to child absent','Endprocess_Pct missed children due to child absent','endprocess_pct-missed-children-due-to-child-absent','Child Absent ' UNION ALL
        SELECT 302, 'Endprocess_Source of info on IPDs - Banner','Endprocess_Source of info on IPDs - Banner','endprocess_source-of-info-on-ipds-banner','Banner' UNION ALL
        SELECT 317, 'Endprocess_Percent source of info is banner','Endprocess_Percent source of info is banner','endprocess_percent-source-of-info-is-banner','Banner ' UNION ALL
        SELECT 305, 'Endprocess_Source of info on IPDs - Community mobiliser','Endprocess_Source of info on IPDs - Community mobiliser','endprocess_source-of-info-on-ipds-community-mobiliser','Comm. Mobiliser    ' UNION ALL
        SELECT 304, 'Endprocess_Source of info on IPDs - Health worker','Endprocess_Source of info on IPDs - Health worker','endprocess_source-of-info-on-ipds-health-worker','Health Worker ' UNION ALL
        SELECT 299, 'Endprocess_Source of info on IPDs - Mosque announcement','Endprocess_Source of info on IPDs - Mosque announcement','endprocess_source-of-info-on-ipds-mosque-announcement','Mosque ' UNION ALL
        SELECT 300, 'Endprocess_Source of info on IPDs - Newspaper','Endprocess_Source of info on IPDs - Newspaper','endprocess_source-of-info-on-ipds-newspaper','Newspaper ' UNION ALL
        SELECT 301, 'Endprocess_Source of info on IPDs - Poster','Endprocess_Source of info on IPDs - Poster','endprocess_source-of-info-on-ipds-poster','Poster ' UNION ALL
        SELECT 332, 'Endprocess_Pct of non compliance due to too many rounds','Endprocess_Pct of non compliance due to too many rounds','endprocess_pct-of-non-compliance-due-to-too-many-rounds','Too Many Rounds' UNION ALL
        SELECT 327, 'Endprocess_Pct of children absent due to child at school','Endprocess_Pct of children absent due to child at school','pct-chdrn-absent-due-to-child-at-school','School' UNION ALL
        SELECT 330, 'Endprocess_Pct of non compliance due to religious belief','Endprocess_Pct of non compliance due to religious belief','endprocess_pct-of-non-compliance-due-to-religious-belief','Religious Beliefs' UNION ALL
        SELECT 335, 'Endprocess_Pct of non compliance due to fear of OPV side effects','Endprocess_Pct of non compliance due to fear of OPV side effects','endprocess_pct-of-non-compliance-due-to-fear-of-opv-side-effects','Endprocess_Pct of non compliance due to OPV side effect' UNION ALL
        SELECT 336, 'Endprocess_Pct of non compliance due to other remedies available','Endprocess_Pct of non compliance due to other remedies available','endprocess_pct-of-non-compliance-due-to-other-remedies-available','Endprocess_Pct of non compliance due to other remedies ' UNION ALL
        SELECT 337, 'Endprocess_Pct of non compliance due to unhappy with team','Endprocess_Pct of non compliance due to unhappy with team','endprocess_pct-of-non-compliance-due-to-unhappy-with-team','Endprocess_Pct of non compliance due to unhappy w team' UNION ALL
        SELECT 338, 'Endprocess_Pct of non compliance due to no caregiver consent','Endprocess_Pct of non compliance due to no caregiver consent','endprocess_pct-of-non-compliance-due-to-no-caregiver-consent','Endprocess_Pct of non compliance due no caregiver conse' UNION ALL
        SELECT 339, 'Endprocess_Pct of non compliance due to no felt need','Endprocess_Pct of non compliance due to no felt need','endprocess_pct-of-non-compliance-due-to-no-felt-need','Endprocess_Pct of non compliance due to no felt need' UNION ALL
        SELECT 334, 'Endprocess_Pct of non compliance due to political differences','Endprocess_Pct of non compliance due to political differences','endprocess_pct-of-non-compliance-due-to-political-differences','Political' UNION ALL
        SELECT 329, 'Endprocess_Pct of non compliance due to polio is rare','Endprocess_Pct of non compliance due to polio is rare','endprocess_pct-of-non-compliance-due-to-polio-is-rare','Polio is Rare' UNION ALL
        SELECT 333, 'Endprocess_Pct of non compliance due to polio has cure','Endprocess_Pct of non compliance due to polio has cure','endprocess_pct-of-non-compliance-due-to-polio-has-cure','Polio has Cure' UNION ALL
        SELECT 344, 'Redo_Number of children 0 to 59 months missed in HH due to non compliance','Redo_Number of children 0 to 59 months missed in HH due to non compliance','redo_number-of-children-0-to-59-months-missed-in-hh-due-to-non-compliance',' of children 0 to 59 missed in HH due to NC' UNION ALL
        SELECT 348, 'Redo_Percent non compliance resolved by other','Redo_Percent non compliance resolved by other','redo_percent-non-compliance-resolved-by-other','Other' UNION ALL
        SELECT 331, 'Endprocess_Pct of non compliance due to no pluses given','Endprocess_Pct of non compliance due to no pluses given','endprocess_pct-of-non-compliance-due-to-no-pluses-given','No Pluses' UNION ALL
        SELECT 349, 'Endprocess_Aware','Endprocess_Aware','endprocess_aware','Endprocess_Aware' UNION ALL
        SELECT 350, 'Redo_Number of children 0-59 months missed in HH due to child absence','Redo_Number of children 0-59 months missed in HH due to child absence','redo_number-of-children-0-59-months-missed-in-hh-due-to-child-absence','Redo_Child absent' UNION ALL
        SELECT 351, 'Redo_Number of children 0-59 months missed in other NC places','Redo_Number of children 0-59 months missed in other NC places','redo_number-of-children-0-59-months-missed-in-other-nc-places','Redo_ChildNCOther' UNION ALL
        SELECT 352, 'Redo_Number of children 0-59 months missed in NC schools','Redo_Number of children 0-59 months missed in NC schools','redo_number-of-children-0-59-months-missed-in-nc-schools','Redo_ChildNCShool' UNION ALL
        SELECT 353, 'Redo_Reasons for NC - Child sick','Redo_Reasons for NC - Child sick','redo_reasons-for-nc-child-sick','Redo_ChildSick' UNION ALL
        SELECT 354, '. immunised in households with community leader intervention - Child absent','. immunised in households with community leader intervention - Child absent','households-with-community-leader-intervention-child-absent','Redo_COMImmRedoABSENT' UNION ALL
        SELECT 355, '. of household resolved','. of household resolved','-of-household-resolved','Redo_HHRevisited' UNION ALL
        SELECT 356, '. immunised in other NC places with intervention of community influencers','. immunised in other NC places with intervention of community influencers','places-with-intervention-of-community-influencers','Redo_IMMOTCommNC' UNION ALL
        SELECT 345, 'Redo_Percent non compliance resolved by traditional leader','Redo_Percent non compliance resolved by traditional leader','redo_percent-non-compliance-resolved-by-traditional-leader','Trad. Leader     ' UNION ALL
        SELECT 340, 'n compliance resolved by traditional leader','n compliance resolved by traditional leader','n-compliance-resolved-by-traditional-leader','Trad. Leader    ' UNION ALL
        SELECT 347, 'Redo_Percent non compliance resolved by religious leader','Redo_Percent non compliance resolved by religious leader','redo_percent-non-compliance-resolved-by-religious-leader','Rel. Leader     ' UNION ALL
        SELECT 342, 'n compliance resolved by religious leader','n compliance resolved by religious leader','n-compliance-resolved-by-religious-leader','Rel. Leader    ' UNION ALL
        SELECT 346, 'Redo_Percent non compliance resolved by community leader','Redo_Percent non compliance resolved by community leader','redo_percent-non-compliance-resolved-by-community-leader','Comm. Leader' UNION ALL
        SELECT 328, 'Endprocess_Pct of non compliance due to child sick','Endprocess_Pct of non compliance due to child sick','endprocess_pct-of-non-compliance-due-to-child-sick','Child Sick ' UNION ALL
        SELECT 341, 'n compliance resolved by community leader','n compliance resolved by community leader','n-compliance-resolved-by-community-leader','Comm. Leader ' UNION ALL
        SELECT 343, 'n compliance resolved by other','n compliance resolved by other','n-compliance-resolved-by-other','Other ' UNION ALL
        SELECT 357, '. immunised in other NC places with intervention of others','. immunised in other NC places with intervention of others','other-nc-places-with-intervention-of-others','Redo_IMMOTOtherNC' UNION ALL
        SELECT 358, '. immunised in other NC places with intervention of religious leaders','. immunised in other NC places with intervention of religious leaders','places-with-intervention-of-religious-leaders','Redo_IMMOTRelNC' UNION ALL
        SELECT 359, '. immunised in other NC places with intervention of traditional leaders','. immunised in other NC places with intervention of traditional leaders','-immunised-in-other-nc-places-with-intervention-of-traditional-leaders','Redo_IMMOTTradNC' UNION ALL
        SELECT 360, '. Immunised in households with traditonal leader intervention - Child absent','. Immunised in households with traditonal leader intervention - Child absent','-immunised-in-households-with-traditonal-leader-intervention-child-absent','Redo_ImmRedoABSENT' UNION ALL
        SELECT 361, '. immunised in NC schools with intervention of community influencer','. immunised in NC schools with intervention of community influencer','-immunised-in-nc-schools-with-intervention-of-community-influencer','Redo_IMMSCCommNC' UNION ALL
        SELECT 362, '. immunised in NC schools with intervention of others','. immunised in NC schools with intervention of others','-immunised-in-nc-schools-with-intervention-of-others','Redo_IMMSCOtherNC' UNION ALL
        SELECT 363, '. immunised in NC schools with intervention of religious leader','. immunised in NC schools with intervention of religious leader','-immunised-in-nc-schools-with-intervention-of-religious-leader','Redo_IMMSCRelNC' UNION ALL
        SELECT 364, '. immunised in NC schools with intervention of traditional leader','. immunised in NC schools with intervention of traditional leader','-immunised-in-nc-schools-with-intervention-of-traditional-leader','Redo_IMMSCTradNC' UNION ALL
        SELECT 365, 'Redo_Reasons for NC - No caregiver consent','Redo_Reasons for NC - No caregiver consent','redo_reasons-for-nc-no-caregiver-consent','Caregiver' UNION ALL
        SELECT 366, 'Redo_Number of NC households','Redo_Number of NC households','redo_number-of-nc-households','HHRedo' UNION ALL
        SELECT 370, '. of NC children not immunised (not resolved)','. of NC children not immunised (not resolved)','-of-nc-children-not-immunised-not-resolved','tImmRedo' UNION ALL
        SELECT 371, '. of children absent not immunised (not resolved)','. of children absent not immunised (not resolved)','-of-children-absent-not-immunised-not-resolved','tImmRedoABSENT' UNION ALL
        SELECT 372, 'Redo_Reasons for NC - OPV safety','Redo_Reasons for NC - OPV safety','redo_reasons-for-nc-opv-safety','Redo_OpvSafety' UNION ALL
        SELECT 368, 'Redo_Reasons for NC - No need felt','Redo_Reasons for NC - No need felt','needfelt','NeedFelt' UNION ALL
        SELECT 369, 'Redo_Number of other NC places','Redo_Number of other NC places','nocother','NOCOther' UNION ALL
        SELECT 373, '. immunised in households with intervention of others - Child absent','. immunised in households with intervention of others - Child absent','-immunised-in-households-with-intervention-of-others-child-absent','Redo_OTHERImRedoABSENT' UNION ALL
        SELECT 374, '. of other places resolved','. of other places resolved','-of-other-places-resolved','Redo_OTRevisited' UNION ALL
        SELECT 375, 'Redo_Reasons for NC - Political differences','Redo_Reasons for NC - Political differences','redo_reasons-for-nc-political-differences','Redo_PoliticalDifferences' UNION ALL
        SELECT 376, 'Redo_Reasons for child absent - Playground','Redo_Reasons for child absent - Playground','redo_reasons-for-child-absent-playground','Redo_Reason1ABS' UNION ALL
        SELECT 377, 'Redo_Reasons for child absent - Market','Redo_Reasons for child absent - Market','redo_reasons-for-child-absent-market','Redo_Reason2ABS' UNION ALL
        SELECT 378, 'Redo_Reasons for child absent - School','Redo_Reasons for child absent - School','redo_reasons-for-child-absent-school','Redo_Reason3ABS' UNION ALL
        SELECT 379, 'Redo_Reasons for child absent - Farm','Redo_Reasons for child absent - Farm','redo_reasons-for-child-absent-farm','Redo_Reason4ABS' UNION ALL
        SELECT 380, 'Redo_Reasons for child absent - Social Event','Redo_Reasons for child absent - Social Event','redo_reasons-for-child-absent-social-event','Redo_Reason5ABS' UNION ALL
        SELECT 381, 'Redo_Reasons for child absent - Other','Redo_Reasons for child absent - Other','redo_reasons-for-child-absent-other','Redo_Reason6ABS' UNION ALL
        SELECT 382, 'Redo_Reasons for NC - Reason not given','Redo_Reasons for NC - Reason not given','redo_reasons-for-nc-reason-not-given','Redo_ReasonNotGiven' UNION ALL
        SELECT 383, 'Redo_Reasons for NC - Religious belief','Redo_Reasons for NC - Religious belief','redo_reasons-for-nc-religious-belief','Redo_ReligiousBelief' UNION ALL
        SELECT 384, '. immunised in households with religious leader intervention - Child absent','. immunised in households with religious leader intervention - Child absent','-immunised-in-households-with-religious-leader-intervention-child-absent','Redo_RELImmRedoABSENT' UNION ALL
        SELECT 385, '. of schools resolved','. of schools resolved','-of-schools-resolved','Redo_SCRevisited' UNION ALL
        SELECT 386, '. of settlements to revisit','. of settlements to revisit','-of-settlements-to-revisit','Redo_SettlementsRedo' UNION ALL
        SELECT 387, 'Redo_Reasons for NC - Too many rounds','Redo_Reasons for NC - Too many rounds','redo_reasons-for-nc-too-many-rounds','Redo_TooManyRounds' UNION ALL
        SELECT 388, 'Redo_Reasons for NC - unhappy with immunisation personnel','Redo_Reasons for NC - unhappy with immunisation personnel','redo_reasons-for-nc-unhappy-with-immunisation-personnel','Redo_UnhappyWith' UNION ALL
        SELECT 367, 'Redo_Number of NC schools','Redo_Number of NC schools','ncshools','NCShools' UNION ALL
        SELECT 389, 'Redo_MissedRedo','Redo_MissedRedo','redo_missedredo','Redo_MissedRedo' UNION ALL
        SELECT 390, 'Redo_TargetRedo','Redo_TargetRedo','redo_targetredo','Redo_TargetRedo' UNION ALL
        SELECT 391, 'Outside_Number of settlements visited by suveyor','Outside_Number of settlements visited by suveyor','number-of-settlements-visited-by-suveyor','Outside_Settlementno' UNION ALL
        SELECT 392, ' number of children sampled in settlement 3',' number of children sampled in settlement 3','-number-of-children-sampled-in-settlement-3','Outside_totSeet3' UNION ALL
        SELECT 393, ' children not finger marked (not immunized) in settlement 3',' children not finger marked (not immunized) in settlement 3','not-finger-marked-not-immunized-in-settlement-3','Outside_totMist3' UNION ALL
        SELECT 394, ' number of children sampled in settlement 1',' number of children sampled in settlement 1','-number-of-children-sampled-in-settlement-1','Outside_totSeet1' UNION ALL
        SELECT 395, ' number of children sampled in settlement 2',' number of children sampled in settlement 2','-number-of-children-sampled-in-settlement-2','Outside_totSeet2' UNION ALL
        SELECT 396, ' children not finger marked (not immunized) in settlement 1',' children not finger marked (not immunized) in settlement 1','not-finger-marked-not-immunized-in-settlement-1','Outside_totMist1' UNION ALL
        SELECT 397, ' children not finger marked (not immunized) in settlement 2',' children not finger marked (not immunized) in settlement 2','finger-marked-not-immunized-in-settlement-2','Outside_totMist2' UNION ALL
        SELECT 398, ' number of locations sampled by suveyor',' number of locations sampled by suveyor','-number-of-locations-sampled-by-suveyor','Outside_numberof Locations' UNION ALL
        SELECT 399, 'Outside_Unvaccinated this round','Outside_Unvaccinated this round','outside_unvaccinated-this-round','Outside_Unvaccinated this round' UNION ALL
        SELECT 400, 'Outside_0to9mth Seen','Outside_0to9mth Seen','redo_0to9mth-seen','Outside_0to9mth Seen' UNION ALL
        SELECT 5, 'Number of vaccine doses used in HRD','Number of vaccine doses used in HRD','number-of-vaccine-doses-used','Number of vaccine doses used in HRD' UNION ALL
        SELECT 401, 'Outside_0to9mth notMarked','Outside_0to9mth notMarked','outside_0to9mth-notmarked','Outside_0to9mth notMarked' UNION ALL
        SELECT 404, 'Outside_children 24-59mth sampled by suveyor','Outside_children 24-59mth sampled by suveyor','outside_children-24-59mth-sampled-by-suveyor','Outside_24to59mth Seen' UNION ALL
        SELECT 402, 'Outside_children 0-23mth sampled by suveyor','Outside_children 0-23mth sampled by suveyor','outside_0to23mth-seen','Outside_children 0-23mth sampled by suveyor' UNION ALL
        SELECT 403, 'Outside_children 0-23mth not finger marked','Outside_children 0-23mth not finger marked','outside_0to23mth-notmarked','Outside_children 0-23mth not finger marked' UNION ALL
        SELECT 405, 'Outside_children 24-59mth not finger marked (not immunized)','Outside_children 24-59mth not finger marked (not immunized)','outside_24to59mth-notmarked','Outside_24to59mth notMarked' UNION ALL
        SELECT 406, ' number of children sampled (calculated)',' number of children sampled (calculated)','-number-of-children-sampled-calculated',' Seen' UNION ALL
        SELECT 407, ' number of children not finger marked (calculated)',' number of children not finger marked (calculated)','children-not-finger-marked-calculated',' Notmarked' UNION ALL
        SELECT 408, ' number of children seen in settlement 4',' number of children seen in settlement 4','-number-of-children-seen-in-settlement-4','Outside_totSeet4' UNION ALL
        SELECT 409, ' children not finger marked (not immunized) in settlement 4',' children not finger marked (not immunized) in settlement 4','finger-not-immunized-in-settlement-4','Outside_totMist4' UNION ALL
        SELECT 410, ' number of children sampled in settlement 5',' number of children sampled in settlement 5','-number-of-children-sampled-in-settlement-5','Outside_totSeet5' UNION ALL
        SELECT 411, ' number of children sampled in settlement 6',' number of children sampled in settlement 6','-number-of-children-sampled-in-settlement-6','Outside_totSeet6' UNION ALL
        SELECT 412, ' children not finger marked (not immunized) in settlement 5',' children not finger marked (not immunized) in settlement 5','--children-not-finger-marked-not-immunized-in-settlement-5','Outside_totMist5' UNION ALL
        SELECT 413, ' children not finger marked (not immunized) in settlement 6',' children not finger marked (not immunized) in settlement 6','---children-not-finger-marked-not-immunized-in-settlement-6','Outside_totMist6' UNION ALL
        SELECT 414, 'Endprocess_HHsampled','Endprocess_HHsampled','endprocess_hhsampled','Endprocess_HHsampled' UNION ALL
        SELECT 415, 'Endprocess_HHvisitedTEAMS','Endprocess_HHvisitedTEAMS','endprocess_hhvisitedteams','Endprocess_HHvisitedTEAMS' UNION ALL
        SELECT 416, 'Endprocess_ZeroDose','Endprocess_ZeroDose','endprocess_zerodose','Endprocess_ZeroDose' UNION ALL
        SELECT 417, 'Endprocess_TotalYoungest','Endprocess_TotalYoungest','endprocess_totalyoungest','Endprocess_TotalYoungest' UNION ALL
        SELECT 418, 'Endprocess_YoungstRI','Endprocess_YoungstRI','endprocess_youngstri','Endprocess_YoungstRI' UNION ALL
        SELECT 419, 'Endprocess_RAssessMrk','Endprocess_RAssessMrk','endprocess_rassessmrk','Endprocess_RAssessMrk' UNION ALL
        SELECT 420, 'Endprocess_RCorctCAT','Endprocess_RCorctCAT','endprocess_rcorctcat','Endprocess_RCorctCAT' UNION ALL
        SELECT 421, 'Endprocess_RIncorect','Endprocess_RIncorect','endprocess_rincorect','Endprocess_RIncorect' UNION ALL
        SELECT 422, 'Endprocess_RXAssessMrk','Endprocess_RXAssessMrk','endprocess_rxassessmrk','Endprocess_RXAssessMrk' UNION ALL
        SELECT 423, 'Endprocess_RXCorctCAT','Endprocess_RXCorctCAT','endprocess_rxcorctcat','Endprocess_RXCorctCAT' UNION ALL
        SELECT 424, 'Endprocess_RXIncorect','Endprocess_RXIncorect','endprocess_rxincorect','Endprocess_RXIncorect' UNION ALL
        SELECT 168, 'Number of cVDPV and WPV cases','Number of cVDPV and WPV cases','number-of-cvdpv-and-wpv-cases','Number of cVDPV and WPV cases' UNION ALL
        SELECT 158, 'Number of children missed due to all access issues','Number of children missed due to all access issues','inaccessible-children-reported-in-the-district-during-the-campaign','Inaccessible Children' UNION ALL
        SELECT 187, 'Percent of refusals resolved during the previous month (both during campaigns and in between rounds)','Percent of refusals resolved during the previous month (both during campaigns and in between rounds)','percent-of-refusals-resolved-during-the-previous-month-both-during-campaigns-and-in-between-rounds','Refusals Conversion' UNION ALL
        SELECT 434, 'Reason for inaccessible children - Perception of fear','Reason for inaccessible children - Perception of fear','rsn-children-perception-of-fear','Perception of fear' UNION ALL
        SELECT 435, 'Reason for inaccessible children - Local community not supportive','Reason for inaccessible children - Local community not supportive','rsn-children-local-community-not-supportive','Local community not supportive' UNION ALL
        SELECT 436, 'Reason for inaccessible children - Crime','Reason for inaccessible children - Crime','rsn-children-crime','Crime' UNION ALL
        SELECT 437, 'Reason for inaccessible children - Militant / Anti-Govt Elements','Reason for inaccessible children - Militant / Anti-Govt Elements','rsn-children-militant-anti-govt-elements','Militant / Anti-Govt Elements' UNION ALL
        SELECT 438, 'Reason for inaccessible children - Security Operations / Incidents','Reason for inaccessible children - Security Operations / Incidents','rsn-children-security-operations-incidents','Security Operations / Incidents' UNION ALL
        SELECT 439, 'Reason for inaccessible children - Management issues','Reason for inaccessible children - Management issues','rsn-children-management-issues','Management issues' UNION ALL
        SELECT 440, 'Reason for inaccessible children - Environment issues','Reason for inaccessible children - Environment issues','rsn-children-environment-issues','Reason for inaccessible children - Environment issues' UNION ALL
        SELECT 441, 'Reason for inaccessible children - Political issues','Reason for inaccessible children - Political issues','rsn-children-political-issues','Political issues' UNION ALL
        SELECT 442, 'pct Reason for inaccessible children - Perception of fear','pct Reason for inaccessible children - Perception of fear','rsn-children-perception-of-fear-2','pct Perception of fear' UNION ALL
        SELECT 443, 'pct Reason for inaccessible children - Local community not supportive','pct Reason for inaccessible children - Local community not supportive','rsn-children-local-community-not-supportive-2','pct Local community not supportive' UNION ALL
        SELECT 444, 'pct Reason for inaccessible children - Crime','pct Reason for inaccessible children - Crime','rsn-children-crime-2','pct Crime' UNION ALL
        SELECT 445, 'pct Reason for inaccessible children - Militant / Anti-Govt Elements','pct Reason for inaccessible children - Militant / Anti-Govt Elements','rsn-children-militant-anti-govt-elements-2','pct Militant / Anti-Govt Elements' UNION ALL
        SELECT 446, 'pct Reason for inaccessible children - Security Operations / Incidents','pct Reason for inaccessible children - Security Operations / Incidents','rsn-children-security-operations-incidents-2','pct Security Operations / Incidents' UNION ALL
        SELECT 447, 'pct Reason for inaccessible children - Management issues','pct Reason for inaccessible children - Management issues','rsn-children-management-issues-2','pct Management issues' UNION ALL
        SELECT 448, 'pct Reason for inaccessible children - Environment issues','pct Reason for inaccessible children - Environment issues','rsn-children-environment-issues-2','pct Environment issues' UNION ALL
        SELECT 449, 'pct Reason for inaccessible children - Political issues','pct Reason for inaccessible children - Political issues','rsn-children-political-issues-2','pct Political issues' UNION ALL
        SELECT 451, 'Reason for inaccessible children - No reason provided','Reason for inaccessible children - No reason provided','rsn-children-no-reason-provided','Reason for inaccessible children - No reason provided' UNION ALL
        SELECT 450, 'pct Reason for inaccessible children - No reason provided','pct Reason for inaccessible children - No reason provided','rsn-children-no-reason','pct No reason provided' UNION ALL
        SELECT 431, 'Number of non-polio AFP cases with zero doses of OPV','Number of non-polio AFP cases with zero doses of OPV','non-polio-afp-cases-with-zero-doses-of-opv','0 Doses' UNION ALL
        SELECT 432, 'Number of non-polio AFP cases with 1-3 doses of OPV','Number of non-polio AFP cases with 1-3 doses of OPV','non-polio-afp-cases-with-1-3-doses-of-opv','1â€“3 Doses' UNION ALL
        SELECT 433, 'Number of non-polio AFP cases with 4+ doses of OPV','Number of non-polio AFP cases with 4+ doses of OPV','non-polio-afp-cases-with-4-doses-of-opv','4+ Doses' UNION ALL
        SELECT 294, 'Endprocess_Percent vaccination influencer is vaccinator','Endprocess_Percent vaccination influencer is vaccinator','endprocess_percent-vaccination-influencer-is-vaccinator','Vaccinator' UNION ALL
        SELECT 257, 'Endprocess_NOimmReas13 - There are other remedies available','Endprocess_NOimmReas13 - There are other remedies available','endprocess_noimmreas13-there-are-other-remedies-available','Other Remedies Avail.' UNION ALL
        SELECT 326, 'Endprocess_Pct of children absent due to child at farm','Endprocess_Pct of children absent due to child at farm','pct-chdrn-absent-due-to-child-at-farm','Farm' UNION ALL
        SELECT 255, 'Endprocess_NOimmReas11 - Polio is rare','Endprocess_NOimmReas11 - Polio is rare','endprocess_noimmreas11-polio-is-rare','Polio is Rare ' UNION ALL
        SELECT 233, 'UNICEF Staffing','Proportion of UNICEF Polio Positions in place at National + State / Province level','pct-of-unicef-polio-positions-in-place-at-national-state-province-level','Human Resouces'
        )x


        """)
    ]
