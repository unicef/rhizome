

JAR_FILE="/Users/johndingee_seed/code/polio/source_data/Briefcase_v1.4.4.jar"
AGGREGATE_URL="https://vcm_ng.appspot.com/"
STORAGE_DIRECTORY="/Users/johndingee_seed/code/polio/static/odk_source/"
EXPORT_DIRECTORY="/Users/johndingee_seed/code/polio/static/odk_source/csv_exports"
USERNAME="admin"
PASSWORD="P@ssword"

# FORM_LIST = ['VCM_Sett_Coordinates_1.2']

# FORM_LIST = ['VCM_Sett_Coordinates_1.2','New_VCM_Summary', \
#     'activity_report','VCM_Birth_Record']


# SECONDARY_FORM_LIST = ['Health_Camps_Bauchi','Health_Camps_Sokoto',\
#         'Phone Inventory', 'Health_Camps_Jigawa','Health_Camps_Yobe',\
#         'Polio Sample','VCM_Summary','Health_Camps_Kaduna',\
#         'Health_Camps_Zamfara','Practice_VCM_Birth_Record',\
#         'VWS_Register','Health_Camps_Kano','KnowThePeople',\
#         'Practice_VCM_Sett_Coordinates_1.2','Health_Camps_Katsina',\
#         'Practice_VCM_Summary','cluster_supervisor','Health_Camps_Kebbi'\
#         'Pax_List_Report_Training']


FORM_LIST = ['Health_Camps_Bauchi','Health_Camps_Sokoto',\
        'Phone Inventory', 'Health_Camps_Jigawa','Health_Camps_Yobe',\
        'Polio Sample','VCM_Summary','Health_Camps_Kaduna',\
        'Health_Camps_Zamfara','Practice_VCM_Birth_Record',\
        'VWS_Register','Health_Camps_Kano','KnowThePeople',\
        'Practice_VCM_Sett_Coordinates_1.2','Health_Camps_Katsina',\
        'Practice_VCM_Summary','cluster_supervisor','Health_Camps_Kebbi'\
        'Pax_List_Report_Training','VCM_Sett_Coordinates_1.2','New_VCM_Summary', \
        'activity_report','VCM_Birth_Record']



# WHEN I OUTPUT THE CSV VIA THE COMMAND LINE TOOLS THE HEADER IS NOT INCLUDED :(
HEADER_DICT = {
    'VCM_Sett_Coordinates_1_2.csv': ['SubmissionDate','deviceid','simserial','phonenumber','DateRecorded','SettlementCode','SettlementName','VCMName','VCMPhone','SettlementGPS_Latitude','SettlementGPS_Longitude','SettlementGPS_Altitude','SettlementGPS_Accuracy','meta_instanceID','KEY'],
    'New_VCM_Summary.csv' :['SubmissionDate', 'deviceid', 'simserial', 'phonenumber', 'DateOfReport', 'Date_Implement', 'SettlementCode', 'CensusNewBornsF', 'CensusNewBornsM', 'Tot_Newborns', 'Census2_11MoF', 'Census2_11MoM', 'Tot_2_11Months', 'Census12_59MoF', 'Census12_59MoM', 'Tot_12_59Months', 'Tot_Census', 'VaxNewBornsF', 'VaxNewBornsM',\
    'Tot_VaxNewBorn', 'display_vax2', 'display_vax3', 'display_vax1', 'Vax2_11MoF', 'Vax2_11MoM', 'Tot_Vax2_11Mo', 'display_vax4', 'display_vax5', 'display_vax6', 'Vax12_59MoF', 'Vax12_59MoM', 'Tot_Vax12_59Mo', 'Tot_Vax', 'Tot_Missed', 'display_vax7', 'display_vax8', 'display_vax9', 'display_msd1', 'display_msd2',\
    'group_msd_chd_Msd_PlaygroundF', 'group_msd_chd_Msd_PlaygroundM', 'group_msd_chd_Msd_SocEventF', 'group_msd_chd_Msd_SocEventM', 'group_msd_chd_Msd_MarketF', 'group_msd_chd_Msd_MarketM', 'group_msd_chd_Msd_FarmF', 'group_msd_chd_Msd_FarmM', 'group_msd_chd_Msd_SchoolF', 'group_msd_chd_Msd_SchoolM', 'group_msd_chd_Msd_ChildSickF', 'group_msd_chd_Msd_ChildSickM', 'group_msd_chd_Msd_SideEffectsF', 'group_msd_chd_Msd_SideEffectsM', 'group_msd_chd_Msd_NoFeltNeedF', 'group_msd_chd_Msd_NoFeltNeedM', 'group_msd_chd_Msd_TooManyRoundsF', 'group_msd_chd_Msd_TooManyRoundsM', 'group_msd_chd_Msd_RelBeliefsF', 'group_msd_chd_Msd_RelBeliefsM', \
    'group_msd_chd_Msd_PolDiffsF', 'group_msd_chd_Msd_PolDiffsM', 'group_msd_chd_Msd_UnhappyWTeamF', 'group_msd_chd_Msd_UnhappyWTeamM', 'group_msd_chd_Msd_NoPlusesF', 'group_msd_chd_Msd_NoPlusesM', 'group_msd_chd_Msd_NoGovtServicesF', 'group_msd_chd_Msd_NoGovtServicesM', 'group_msd_chd_Msd_PolioUncommonF', 'group_msd_chd_Msd_PolioUncommonM', 'group_msd_chd_Msd_PolioHasCureF', 'group_msd_chd_Msd_PolioHasCureM', 'group_msd_chd_Msd_OtherProtectionF', 'group_msd_chd_Msd_OtherProtectionM', 'group_msd_chd_Msd_NoConsentF', 'group_msd_chd_Msd_NoConsentM', 'group_msd_chd_Msd_HHNotVisitedF', 'group_msd_chd_Msd_HHNotVisitedM', 'group_msd_chd_Msd_SecurityF', 'group_msd_chd_Msd_SecurityM', \
    'group_msd_chd_Msd_AgedOutF', 'group_msd_chd_Msd_AgedOutM', 'group_msd_chd_Msd_FamilyMovedF', 'group_msd_chd_Msd_FamilyMovedM', 'group_msd_chd_Msd_ChildDiedF', 'group_msd_chd_Msd_ChildDiedM', 'group_msd_chd_Tot_Missed_Check', 'group_msd_chd_display_msd3', 'spec_grp_choice', 'group_spec_events_Spec_ZeroDose', 'group_spec_events_Spec_PregnantMother', 'group_spec_events_Spec_Newborn', 'group_spec_events_Spec_VCMAttendedNCer', 'group_spec_events_Spec_CMAMReferral', 'group_spec_events_Spec_RIReferral', 'group_spec_events_Spec_AFPCase', 'group_spec_events_Spec_MslsCase', 'group_spec_events_Spec_OtherDisease', 'group_spec_events_Spec_FIC', 'meta_instanceID',\
    'KEY'],
}
