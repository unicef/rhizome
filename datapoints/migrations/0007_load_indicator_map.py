# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('datapoints', '0006_load_indicators_and_campaigns'),
    ]

    operations = [

        migrations.RunSQL("""

                DROP TABLE IF EXISTS _tmp_indicator_map;

                CREATE TABLE _tmp_indicator_map AS

                SELECT 'Number of Unicef polio positions in their posts in PBR-approved structures' as indicator_name,32 as indicator_id UNION ALL
                SELECT 'Target number of Unicef polio positions in PBR-approved structures',31 UNION ALL
                SELECT 'Number of children missed due to other reasons',24 UNION ALL
                SELECT 'Number of refusals before re-visit',25 UNION ALL
                SELECT 'Number of refusals after re-visit',26 UNION ALL
                SELECT 'Number of target social mobilizers',35 UNION ALL
                SELECT 'Number of female social mobilizers',40 UNION ALL
                SELECT 'Percentage of States/Regions with OPV supply arriving at state/region level in sufficient time before campaign',67 UNION ALL
                SELECT 'YoungstRI',418 UNION ALL
                SELECT 'RCorctCAT',420 UNION ALL
                SELECT 'TotalYoungest',417 UNION ALL
                SELECT 'RIncorect',421 UNION ALL
                SELECT 'HHvisitedTEAMS',415 UNION ALL
                SELECT 'RXCorctCAT',423 UNION ALL
                SELECT 'RXAssessMrk',422 UNION ALL
                SELECT 'RXIncorect',424 UNION ALL
                SELECT 'Sum of Marked0to59',269 UNION ALL
                SELECT 'Sum of UnImmun0to59',270 UNION ALL
                SELECT 'TOTAL teams Checked',38 UNION ALL
                SELECT '# HR areas (Clusters) with social mobilizers',34 UNION ALL
                SELECT ' # target social mobilizers',35 UNION ALL
                SELECT '# caregivers',29 UNION ALL
                SELECT '# refusals before re-visit',25 UNION ALL
                SELECT '# Microplans incoroporating social data',28 UNION ALL
                SELECT 'Amount committed',44 UNION ALL
                SELECT '# districts having NO stock-outs of OPV',53 UNION ALL
                SELECT '# teams w/ at least one female worker',37 UNION ALL
                SELECT '# teams',38 UNION ALL
                SELECT '# w/ capacity',62 UNION ALL
                SELECT ' # of HR areas (clusters) targeted  ',33 UNION ALL
                SELECT '# Microplans in LPD',27 UNION ALL
                SELECT 'Other reasons',24 UNION ALL
                SELECT '# refusals after re-visit',26 UNION ALL
                SELECT '# female social mobilizers',40 UNION ALL
                SELECT '# of targeted under-five children',55 UNION ALL
                SELECT 'Amount TOTAL FRR funds',43 UNION ALL
                SELECT '# in place',36 UNION ALL
                SELECT '# vaccine doses used',5 UNION ALL
                SELECT '# HR areas with social mobilizers',34 UNION ALL
                SELECT 'Number of core polio communication personnel in place in a country programme',32 UNION ALL
                SELECT '# Microplans in High Risk District',27 UNION ALL
                SELECT '# front line workers',41 UNION ALL
                SELECT 'Target number of core polio personnel in place in a country programme',31 UNION ALL
                SELECT 'CensusNewBornsF',93 UNION ALL
                SELECT '# trained on RI in past 6 mos.',49 UNION ALL
                SELECT '# children vaccined',51 UNION ALL
                SELECT ' # front line workers',41 UNION ALL
                SELECT 'Target core polio personnel in place in a country programme',31 UNION ALL
                SELECT '# aware',30 UNION ALL
                SELECT ' # of HR areas targeted  ',33 UNION ALL
                SELECT 'Total # of targetted social mobilizers',35 UNION ALL
                SELECT '# target social mobilizers',35 UNION ALL
                SELECT '# trained on RI in past 6 months.',49 UNION ALL
                SELECT 'Target core polio communication personnel in place in a country programme',31 UNION ALL
                SELECT ' # teams',38 UNION ALL
                SELECT '# workers w/ IPC skills',42 UNION ALL
                SELECT 'Number of core polio personnel in place in a country programme',32 UNION ALL
                SELECT 'CensusNewBornsM',94 UNION ALL
                SELECT '# health facilities w/ capacity',62 UNION ALL
                SELECT 'Tot_Newborns',83 UNION ALL
                SELECT '# received payment timely',46 UNION ALL
                SELECT '% w/ capacity',62 UNION ALL
                SELECT 'Census2_11MoF',85 UNION ALL
                SELECT 'Target # of core polio communication',31 UNION ALL
                SELECT 'Census2_11MoM',84 UNION ALL
                SELECT '# of core polio communication personnel in place',32 UNION ALL
                SELECT '# of HR areas targeted',33 UNION ALL
                SELECT 'Number of cases of cVDPV2',69 UNION ALL
                SELECT 'Number of cases of iVDPV2',162 UNION ALL
                SELECT 'Number of cases of WPV1',70 UNION ALL
                SELECT 'Number of cases of WPV3',160 UNION ALL
                SELECT 'Number of cases of aVDPV2',159 UNION ALL
                SELECT 'Number of cases of WPV1WPV3',161 UNION ALL
                SELECT 'Target number of core polio communications in place',31 UNION ALL
                SELECT 'Number of social mobilisers who are female',40 UNION ALL
                SELECT '# of teams',38 UNION ALL
                SELECT 'Tot_2_11Months',90 UNION ALL
                SELECT 'Target number of core polio communication positions',31 UNION ALL
                SELECT '# Microplans incorporating social data',28 UNION ALL
                SELECT '# of core polio communication in place',32 UNION ALL
                SELECT 'Target number of social mobilisers',35 UNION ALL
                SELECT 'All missed children',21 UNION ALL
                SELECT 'Number of social mobilisers who were paid on time',46 UNION ALL
                SELECT 'Census12_59MoF',91 UNION ALL
                SELECT 'Number of social mobilisers in place',36 UNION ALL
                SELECT '# of subregional units',56 UNION ALL
                SELECT 'Target # of core polio communication ',31 UNION ALL
                SELECT 'Number of social mobilizers who were paid on time',46 UNION ALL
                SELECT 'Number of social mobilizers paid on time',46 UNION ALL
                SELECT 'Number of social mobilizers in place',36 UNION ALL
                SELECT 'Amount FRR',43 UNION ALL
                SELECT '# of social mobilizers who received payment on time',46 UNION ALL
                SELECT '% with OPV arriving in sufficient time',67 UNION ALL
                SELECT '# of children vaccined',51 UNION ALL
                SELECT 'Target # of social mobilizers',35 UNION ALL
                SELECT '# of social mobilizers in place',36 UNION ALL
                SELECT '# of HR areas with social mobilizers',34 UNION ALL
                SELECT '# of subregional units where OPV arrived in sufficient time',57 UNION ALL
                SELECT 'Census12_59MoM',87 UNION ALL
                SELECT '# of social mobilizers paid on time',46 UNION ALL
                SELECT '# of female social mobilizers',40 UNION ALL
                SELECT 'Target number of social mobilizers',35 UNION ALL
                SELECT '# polio teams w/ at least one female worker',37 UNION ALL
                SELECT 'NOimmReas19',263 UNION ALL
                SELECT 'Tot_12_59Months',92 UNION ALL
                SELECT 'ZeroDose',416 UNION ALL
                SELECT 'NOimmReas13',257 UNION ALL
                SELECT 'NOimmReas12',256 UNION ALL
                SELECT 'NOimmReas11',255 UNION ALL
                SELECT 'NOimmReas10',254 UNION ALL
                SELECT 'NOimmReas17',261 UNION ALL
                SELECT 'NOimmReas16',260 UNION ALL
                SELECT 'STannounc',295 UNION ALL
                SELECT 'UnImmun0to59',270 UNION ALL
                SELECT 'NOimmReas3',246 UNION ALL
                SELECT 'NOimmReas2',268 UNION ALL
                SELECT 'NOimmReas1',267 UNION ALL
                SELECT 'NOimmReas7',250 UNION ALL
                SELECT 'NOimmReas6',249 UNION ALL
                SELECT 'Tot_Census',75 UNION ALL
                SELECT 'NOimmReas4',247 UNION ALL
                SELECT 'NOimmReas18',262 UNION ALL
                SELECT 'VaxNewBornsF',82 UNION ALL
                SELECT 'VaxNewBornsM',81 UNION ALL
                SELECT 'SRadio',296 UNION ALL
                SELECT 'Tot_VaxNewBorn',89 UNION ALL
                SELECT 'SMosque',299 UNION ALL
                SELECT 'SReiliglead',298 UNION ALL
                SELECT 'SRelative',303 UNION ALL
                SELECT 'STradlead',297 UNION ALL
                SELECT 'Vax2_11MoF',77 UNION ALL
                SELECT 'Sbanner',302 UNION ALL
                SELECT 'Scommmob',305 UNION ALL
                SELECT 'SNOTAWARE',277 UNION ALL
                SELECT 'NOimmReas20',266 UNION ALL
                SELECT 'NOimmReas5',248 UNION ALL
                SELECT 'SNewspaper',300 UNION ALL
                SELECT 'Vax2_11MoM',78 UNION ALL
                SELECT 'Tot_Vax2_11Mo',86 UNION ALL
                SELECT 'Influence5',279 UNION ALL
                SELECT 'Influence4',284 UNION ALL
                SELECT 'Influence7',283 UNION ALL
                SELECT 'Influence6',281 UNION ALL
                SELECT 'Influence1',278 UNION ALL
                SELECT 'Vax12_59MoF',80 UNION ALL
                SELECT 'Influence3',282 UNION ALL
                SELECT 'Influence2',280 UNION ALL
                SELECT 'Vax12_59MoM',79 UNION ALL
                SELECT 'Tot_Vax12_59Mo',88 UNION ALL
                SELECT 'NOimmReas14',258 UNION ALL
                SELECT 'Influence8',285 UNION ALL
                SELECT 'HHsampled',414 UNION ALL
                SELECT 'Tot_Vax',74 UNION ALL
                SELECT 'Tot_Missed',76 UNION ALL
                SELECT 'NOimmReas15',259 UNION ALL
                SELECT 'NOimmReas9',253 UNION ALL
                SELECT 'Marked0to59',269 UNION ALL
                SELECT 'NOimmReas8',252 UNION ALL
                SELECT 'SHworker',304 UNION ALL
                SELECT 'SPoster',301 UNION ALL
                SELECT 'ReasonNotGiven',382 UNION ALL
                SELECT 'PoliticalDifferences',375 UNION ALL
                SELECT 'NotImmRedo',370 UNION ALL
                SELECT 'SettlementsRedo',386 UNION ALL
                SELECT 'TargetRedo',390 UNION ALL
                SELECT 'ChildNCShool',352 UNION ALL
                SELECT 'COMImmRedo',341 UNION ALL
                SELECT 'NoNeedFelt',368 UNION ALL
                SELECT 'IMMSCRelNC',363 UNION ALL
                SELECT 'ChildAbsent',350 UNION ALL
                SELECT 'COMImmRedoABSENT',354 UNION ALL
                SELECT 'IMMSCOtherNC',362 UNION ALL
                SELECT 'Reason1ABS',376 UNION ALL
                SELECT 'ChildNCOther',351 UNION ALL
                SELECT 'IMMOTTradNC',359 UNION ALL
                SELECT 'NoNCShools',367 UNION ALL
                SELECT 'Reason2ABS',377 UNION ALL
                SELECT 'HHRevisited',355 UNION ALL
                SELECT 'RELImmRedo',342 UNION ALL
                SELECT 'OTRevisited',374 UNION ALL
                SELECT 'SCRevisited',385 UNION ALL
                SELECT 'ImmRedoABSENT',360 UNION ALL
                SELECT 'NoNOCOther',369 UNION ALL
                SELECT 'OTHERImRedoABSENT',373 UNION ALL
                SELECT 'Reason4ABS',379 UNION ALL
                SELECT 'MissedRedo',389 UNION ALL
                SELECT 'ChildSick',353 UNION ALL
                SELECT 'NotImmRedoABSENT',371 UNION ALL
                SELECT 'Reason6ABS',381 UNION ALL
                SELECT 'UnhappyWith',388 UNION ALL
                SELECT 'IMMSCCommNC',361 UNION ALL
                SELECT 'RAssessMrk',419 UNION ALL
                SELECT 'Reason5ABS',380 UNION ALL
                SELECT 'NoCaregiver',365 UNION ALL
                SELECT 'RELImmRedoABSENT',384 UNION ALL
                SELECT 'IMMOTOtherNC',357 UNION ALL
                SELECT 'IMMSCTradNC',364 UNION ALL
                SELECT 'IMMOTRelNC',358 UNION ALL
                SELECT 'NoHHRedo',366 UNION ALL
                SELECT 'Reason3ABS',378 UNION ALL
                SELECT 'ImmRedo',340 UNION ALL
                SELECT 'IMMOTCommNC',356 UNION ALL
                SELECT 'OTHERImRedo',343 UNION ALL
                SELECT 'ReligiousBelief',383 UNION ALL
                SELECT 'NonCompliance',344 UNION ALL
                SELECT 'OpvSafety',372 UNION ALL
                SELECT 'TooManyRounds',387 UNION ALL
                SELECT '0to23mth Seen',402 UNION ALL
                SELECT '0to23mth notMarked',403 UNION ALL
                SELECT '24to59mth notMarked',405 UNION ALL
                SELECT 'TOTAL Seen',275 UNION ALL
                SELECT 'totSeet2',395 UNION ALL
                SELECT 'totSeet3',392 UNION ALL
                SELECT 'totSeet1',394 UNION ALL
                SELECT 'totSeet6',411 UNION ALL
                SELECT 'totSeet4',408 UNION ALL
                SELECT 'totSeet5',410 UNION ALL
                SELECT '0to9mth Seen',400 UNION ALL
                SELECT 'totMist2',397 UNION ALL
                SELECT 'totMist3',393 UNION ALL
                SELECT 'totMist1',396 UNION ALL
                SELECT 'totMist6',413 UNION ALL
                SELECT 'TOTAL Notmarked',273 UNION ALL
                SELECT 'totMist4',409 UNION ALL
                SELECT 'totMist5',412 UNION ALL
                SELECT 'Unvaccinated this round',399 UNION ALL
                SELECT '24to59mth Seen',404 UNION ALL
                SELECT 'numberof Locations',398 UNION ALL
                SELECT '0to9mth notMarked',401 UNION ALL
                SELECT 'Number of cases of W1W3',161 UNION ALL
                SELECT 'Reason for inaccessible children - No reason provided',451 UNION ALL
                SELECT 'Political issues',441 UNION ALL
                SELECT 'Environment issues',440 UNION ALL
                SELECT 'Management issues',439 UNION ALL
                SELECT 'Security Operations / Incidents',438 UNION ALL
                SELECT 'Militant / Anti-Govt Elements',437 UNION ALL
                SELECT 'Crime',436 UNION ALL
                SELECT 'Local community not supportive',435 UNION ALL
                SELECT 'Perception of fear',434 UNION ALL
                SELECT 'Number of functional active cold chain equipment in the district',198 UNION ALL
                SELECT 'Number of HRDs that have polio vaccine wastage rate in SIAs between 5 and 15%',221 UNION ALL
                SELECT 'Vaccine wastage rate',220 UNION ALL
                SELECT 'Number of social  mobilizers in place',36 UNION ALL
                SELECT 'd4',433 UNION ALL
                SELECT 'd1_3',432 UNION ALL
                SELECT 'd0',431 UNION ALL
                SELECT 'cVDPV2',69 UNION ALL
                SELECT 'WPV1',70 UNION ALL
                SELECT 'Number of cases of WPV 1',70 UNION ALL
                SELECT 'Number of children 12 months and under',243 UNION ALL
                SELECT 'Number of children under 12 months who received DPT3 or Penta3',244 UNION ALL
                SELECT '# of children vaccinated at transit points last month',177 UNION ALL
                SELECT 'Number of children missed due to all access issues',158 UNION ALL
                SELECT 'Amount total requested FRR funds',43 UNION ALL
                SELECT 'Amount FRR funds committed',44 UNION ALL
                SELECT 'Number of RI sessions monitored',217 UNION ALL
                SELECT 'Number of RI sessions monitored having stockouts of any vaccine in the last month',216 UNION ALL
                SELECT 'Number of high risk districts',195 UNION ALL
                SELECT 'Number of HR districts with locations where OPV is delivered together with any other polio-funded services demanded by the community',218 UNION ALL
                SELECT 'Number of RI defaulters mobilized by social mobilizers last month (with accessibility breakdown)',192 UNION ALL
                SELECT 'Number of caregivers in HR districts',29 UNION ALL
                SELECT '# of HRD which reported on balance SIA vaccine stocks after last SIA round',197 UNION ALL
                SELECT 'Total number of all active cold chain equipment in the district',199 UNION ALL
                SELECT 'Number of children vaccinated in HRD',51 UNION ALL
                SELECT 'Number of vaccine doses used in HRD',5 UNION ALL
                SELECT 'HR District did not receive polio vaccine supply at least 3 days before the planned start date of campaign (yes/no)',196 UNION ALL
                SELECT 'Number of social mobilizers who received on-the-job supervision during their last working week',210 UNION ALL
                SELECT 'Number of SMs trained or refreshed with the integrated health package in the last 6 months',209 UNION ALL
                SELECT 'Number of vaccination teams',38 UNION ALL
                SELECT 'Number of vaccination teams with at least 1 member from the local community',208 UNION ALL
                SELECT 'Target # of social mobilizers and supervisors',207 UNION ALL
                SELECT 'Number of SMs and supervisors in place',206 UNION ALL
                SELECT 'Number of HR sub-districts',33 UNION ALL
                SELECT 'Number of HR sub-districts with at least 1 permanent SM',34 UNION ALL
                SELECT '# health fcilities having NO stock-outs of OPV',66 UNION ALL
                SELECT '# children received Penta3',244 UNION ALL
                SELECT 'Amount FRR updated amount',45 UNION ALL
                SELECT '# received payment on time',46 UNION ALL
                SELECT ' # polio teams',38 UNION ALL
                SELECT '# social mobilizers in place',36 UNION ALL
                SELECT 'Target # of core polio communication personnel',31 UNION ALL
                SELECT 'Number of social mobilizers who received timely payment for last campaign/month''s salary',46 UNION ALL
                SELECT 'Number of vaccinators and SMs operating in HRDs trained on professional IPC package in last 6 months',42 UNION ALL
                SELECT 'Number of vaccination teams with at least 1 female member',37 UNION ALL
                SELECT 'Number of vaccinators and SMs operating in HRD who have been trained on professional Inter Personal Communication packaged in the last 6 months',42 UNION ALL
                SELECT 'Number of vaccinators and SMs',41 UNION ALL
                SELECT 'Number of children targeted in high-risk districts',55 UNION ALL
                SELECT 'Number of vaccination teams with at least one female',37 UNION ALL
                SELECT 'Number of vaccinators and social mobilizers',41 UNION ALL
                SELECT 'spec_grp_choice',95 UNION ALL
                SELECT 'TSettle',208 UNION ALL
                SELECT 'Number of absences after re-visit',214 UNION ALL
                SELECT 'Number of absences before re-visit',213 UNION ALL
                SELECT 'Number of non-polio AFP cases with 1-3 doses of OPV',432 UNION ALL
                SELECT 'Number of non-polio AFP cases with zero doses of OPV',431 UNION ALL
                SELECT 'Number of non-polio AFP cases with 4+ doses of OPV',433 UNION ALL
                SELECT 'Number of WPV1 cases',70 UNION ALL
                SELECT 'Number of cVDPV2 cases',69 UNION ALL
                SELECT 'Is an access-challenged district',203 UNION ALL
                SELECT 'Total number of LT vaccination transit points planned by the programme',204 UNION ALL
                SELECT 'Number of children vaccined in HRD',51 UNION ALL
                SELECT 'Number of high risk sub-districts',33 UNION ALL
                SELECT 'Number of social mobilizers receiving timely payment for last campaign',46 UNION ALL
                SELECT 'Target number of social mobilizers and supervisors',207 UNION ALL
                SELECT 'Number of high risk sub-districts covered by at least 1 social mobilizer',34 UNION ALL
                SELECT 'Number of children vaccinated at transit points last month',177 UNION ALL
                SELECT '# of vaccination teams in HRA',38 UNION ALL
                SELECT 'Is an access-challenged district that has a specific access approach identified',202 UNION ALL
                SELECT 'Number of established LT vaccination transit points',175 UNION ALL
                SELECT 'number of social mobilisers participating the telephone survey',463 UNION ALL
                SELECT 'Number of social mobilizers trained or refreshed with the integrated health package in the last 6 months',209 UNION ALL
                SELECT 'Is an HRD that has polio vaccine wastage rate in SIAs between 5 and 15%',221 UNION ALL
                SELECT 'HR district did NOT receive polio vaccine supply at least 3 days before the planned start date of campaign',196 UNION ALL
                SELECT 'Number of social mobilizers and supervisors in place',206 UNION ALL
                SELECT 'Number of established LT vaccination transit points with a dedicated social mobilizer',176 UNION ALL
                SELECT 'Is a high risk district',195 UNION ALL
                SELECT 'Is an access-challenged district (Yes/No)',203 UNION ALL
                SELECT 'Has a specific access approach identified (Yes/No)',202 UNION ALL
                SELECT '# of children who received Penta 3',244 UNION ALL
                SELECT '# of children 7-12 months old',243 UNION ALL
                SELECT '# of micro plans reviewed',27 UNION ALL
                SELECT 'District reported balance of SIA vaccine stocks (Yes/No)',197 UNION ALL
                SELECT 'Number of vaccination teams with at least one member from local community',208 UNION ALL
                SELECT 'Number of children missed due to all access reasons',158 UNION ALL
                SELECT 'Reason for inaccessible children - Environment issues',440 UNION ALL
                SELECT 'Reason for inaccessible children - Crime',436 UNION ALL
                SELECT 'Reason for inaccessible children - Militant / Anti-Govt Elements',437 UNION ALL
                SELECT 'Reason for inaccessible children - Management issues',439 UNION ALL
                SELECT 'Reason for inaccessible children - Local community not supportive',435 UNION ALL
                SELECT 'Reason for inaccessible children - Security Operations / Incidents',438 UNION ALL
                SELECT 'Reason for inaccessible children - Perception of fear',434 UNION ALL
                SELECT 'Total number of all active cold chain equipment in district',199 UNION ALL
                SELECT 'Number of refusals afte re-visit',26 UNION ALL
                SELECT 'Number of microplans reviewed',27 UNION ALL
                SELECT 'Number of vaccinators',41 UNION ALL
                SELECT 'Number of vaccinators trained on IPC skills',42 UNION ALL
                SELECT '# of health facilities',199 UNION ALL
                SELECT 'Number of targeted children in HRA',55 UNION ALL
                SELECT '# of high-risk districts with 90% of active cold chain equipments functional',198 UNION ALL
                SELECT 'Number of Microplans incoroporating social data',28 UNION ALL
                SELECT '# of identfied/planned target points',204 UNION ALL
                SELECT 'Number of planned SM and supervisors',207 UNION ALL
                SELECT '# of target children',55 UNION ALL
                SELECT 'District DID NOT receiv OPV 3 days before campaign',196 UNION ALL
                SELECT '# absences after re-visit',214 UNION ALL
                SELECT '# of absences before re-visit',213 UNION ALL
                SELECT '# of refusals before re-visit',25 UNION ALL
                SELECT 'Number of clusters (sub-district units)',33 UNION ALL
                SELECT 'district wastage rate between 5 - 15%',221 UNION ALL
                SELECT '# of children missed due to access issues',470 UNION ALL
                SELECT '# of female SMs in place',40 UNION ALL
                SELECT 'Number of social mobilizers who received timely payment',46 UNION ALL
                SELECT '# of established transit points',175 UNION ALL
                SELECT '# of children vaccinated at TP',177 UNION ALL
                SELECT '% wastage',220 UNION ALL
                SELECT 'Number of social mobilizers responding telephone survey',463 UNION ALL
                SELECT '# vaccination teams with at least one female ',37 UNION ALL
                SELECT 'District is high-risk',195 UNION ALL
                SELECT '# of SMs in place',36 UNION ALL
                SELECT '# of children missed due to absence',350 UNION ALL
                SELECT '# vaccination teams with at least one member from local community',208 UNION ALL
                SELECT '# of established transit points with social mobiliser',176 UNION ALL
                SELECT 'Number of clusters covered by SMs',34 UNION ALL
                SELECT 'group_msd_chd-msd_poldiffsf',112 UNION ALL
                SELECT 'group_spec_events-spec_newborn',125 UNION ALL
                SELECT 'group_msd_chd-msd_toomanyroundsm',141 UNION ALL
                SELECT 'group_msd_chd-msd_poliouncommonf',143 UNION ALL
                SELECT 'group_msd_chd-msd_poliohascuref',132 UNION ALL
                SELECT 'group_msd_chd-msd_playgroundf',124 UNION ALL
                SELECT 'group_msd_chd-msd_marketm',98 UNION ALL
                SELECT 'group_spec_events-spec_zerodose',135 UNION ALL
                SELECT 'group_msd_chd-msd_soceventm',109 UNION ALL
                SELECT 'group_msd_chd-msd_familymovedm',131 UNION ALL
                SELECT 'group_msd_chd-msd_noplusesf',106 UNION ALL
                SELECT 'group_msd_chd-msd_familymovedf',130 UNION ALL
                SELECT 'group_msd_chd-msd_noconsentf',118 UNION ALL
                SELECT 'group_msd_chd-msd_sideeffectsm',129 UNION ALL
                SELECT 'group_msd_chd-msd_nogovtservicesf',146 UNION ALL
                SELECT 'group_msd_chd-tot_missed_check',127 UNION ALL
                SELECT 'group_msd_chd-msd_poliouncommonm',142 UNION ALL
                SELECT 'group_msd_chd-msd_relbeliefsf',119 UNION ALL
                SELECT 'group_msd_chd-msd_agedoutf',103 UNION ALL
                SELECT 'group_msd_chd-msd_unhappywteamm',136 UNION ALL
                SELECT 'group_msd_chd-msd_marketf',99 UNION ALL
                SELECT 'group_msd_chd-msd_nogovtservicesm',145 UNION ALL
                SELECT 'group_spec_events-spec_otherdisease',150 UNION ALL
                SELECT 'group_msd_chd-msd_farmf',97 UNION ALL
                SELECT 'group_spec_events-spec_vcmattendedncer',152 UNION ALL
                SELECT 'group_spec_events-spec_cmamreferral',149 UNION ALL
                SELECT 'group_msd_chd-msd_hhnotvisitedf',138 UNION ALL
                SELECT 'group_msd_chd-msd_poldiffsm',111 UNION ALL
                SELECT 'group_msd_chd-msd_farmm',96 UNION ALL
                SELECT 'group_msd_chd-msd_agedoutm',102 UNION ALL
                SELECT 'group_spec_events-spec_rireferral',144 UNION ALL
                SELECT 'group_msd_chd-msd_nofeltneedf',120 UNION ALL
                SELECT 'group_msd_chd-msd_childdiedm',114 UNION ALL
                SELECT 'group_msd_chd-msd_soceventf',110 UNION ALL
                SELECT 'group_msd_chd-msd_toomanyroundsf',141 UNION ALL
                SELECT 'group_msd_chd-msd_hhnotvisitedm',139 UNION ALL
                SELECT 'group_spec_events-spec_mslscase',134 UNION ALL
                SELECT 'group_spec_events-spec_fic',104 UNION ALL
                SELECT 'group_msd_chd-msd_poliohascurem',133 UNION ALL
                SELECT 'group_msd_chd-msd_securityf',108 UNION ALL
                SELECT 'group_spec_events-spec_afpcase',126 UNION ALL
                SELECT 'group_msd_chd-msd_relbeliefsm',122 UNION ALL
                SELECT 'tot_missed',76 UNION ALL
                SELECT 'group_msd_chd-msd_childdiedf',113 UNION ALL
                SELECT 'group_msd_chd-msd_unhappywteamf',137 UNION ALL
                SELECT 'group_msd_chd-msd_schoolm',101 UNION ALL
                SELECT 'group_msd_chd-msd_otherprotectionf',147 UNION ALL
                SELECT 'group_msd_chd-msd_securitym',107 UNION ALL
                SELECT 'group_msd_chd-msd_otherprotectionm',148 UNION ALL
                SELECT 'group_msd_chd-msd_playgroundm',123 UNION ALL
                SELECT 'group_msd_chd-msd_schoolf',100 UNION ALL
                SELECT 'group_msd_chd-msd_childsickm',115 UNION ALL
                SELECT 'group_msd_chd-msd_childsickf',116 UNION ALL
                SELECT 'group_msd_chd-msd_noplusesm',105 UNION ALL
                SELECT 'group_msd_chd-msd_sideeffectsf',128 UNION ALL
                SELECT 'group_msd_chd-msd_nofeltneedm',121 UNION ALL
                SELECT 'group_spec_events-spec_pregnantmother',151 UNION ALL
                SELECT 'group_msd_chd-msd_noconsentm',117 UNION ALL
                SELECT 'Number of target children',55 ;


                INSERT INTO source_indicator
                (indicator_string,source_guid,document_id)

                SELECT indicator_name,indicator_name, sdd.id FROM _tmp_indicator_map tim

                INNER JOIN source_data_document sdd
                on sdd.doc_text = 'init_db'
                WHERE NOT EXISTS (
                	SELECT 1 FROM source_indicator si
                	WHERE tim.indicator_name = si.indicator_string
                );
                
                INSERT INTO indicator_map
                (source_object_id, master_object_id, mapped_by_id)

                SELECT si.id,tim.indicator_id,u.id
                FROM _tmp_indicator_map tim
                INNER JOIN auth_user u
                ON u.username = 'john'
                INNER JOIn source_indicator si
                ON si.indicator_string = tim.indicator_name


        """)
    ]
