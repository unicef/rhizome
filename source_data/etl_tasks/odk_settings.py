

JAR_FILE="/Users/johndingee_seed/code/polio/source_data/Briefcase_v1.4.4.jar"
AGGREGATE_URL="https://vcm-ng.appspot.com/"
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
    'VCM_Sett_Coordinates_1_2.csv': ['SubmissionDate','deviceid','simserial','phonenumber','DateRecorded','SettlementCode','SettlementName','VCMName','VCMPhone','SettlementGPS-Latitude','SettlementGPS-Longitude','SettlementGPS-Altitude','SettlementGPS-Accuracy','meta-instanceID','KEY']
}
