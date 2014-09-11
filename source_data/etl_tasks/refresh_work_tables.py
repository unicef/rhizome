import csv
import sys, os
import pprint as pp
import pandas as pd
import odk_settings

from django.db.utils import IntegrityError
from pandas import DataFrame, concat

sys.path.append('/Users/johndingee_seed/code/polio') #BAD
os.environ['DJANGO_SETTINGS_MODULE'] = 'polio.settings'
from django.conf import settings


from source_data.models import *


class WorkTableTask(object):

    def __init__(self,request_guid,file_to_process):
        print 'initializing work table task'

        self.request_guid = request_guid
        self.file_to_process = file_to_process


        self.file_to_function_map = {
            "VCM_Sett_Coordinates_1.2" : VCMSettlement,
            "New_VCM_Summary" : VCMSummaryNew,
            "VCM_Summary" : VCMSummary,
            "cluster_supervisor" : ClusterSupervisor,
            "Phone Inventory": PhoneInventory,
            "VCM_Birth_Record": VCMBirthRecord,
            "activity_report": ActivityReport,
            "VWS_Register" :VWSRegister ,
            "Practice_VCM_Sett_Coordinates_1.2": PracticeVCMSettCoordinates,
            "Pax_List_Report_Training" :PaxListReportTraining,
            "Practice_VCM_Summary":PracticeVCMSummary,
            "Practice_VCM_Birth_Record": PracticeVCMBirthRecord,
            "KnowThePeople": KnowThePeople,
            "Health_Camps_Yobe": HealthCamp,
            "Health_Camps_Kebbi": HealthCamp,
            'Health_Camps_Bauchi': HealthCamp,
            'Health_Camps_Jigawa': HealthCamp,
            'Health_Camps_Kano': HealthCamp,
            'Health_Camps_Katsina': HealthCamp,
            'Health_Camps_Sokoto': HealthCamp,
            'Health_Camps_Kaduna': HealthCamp,
        }

        # this below shoudl be a configuration
        self.csv_dir = '/Users/johndingee_seed/code/polio/static/odk_source/csv_exports/'

        # execute the relevant function
        work_table_obj = self.file_to_function_map[self.file_to_process]

        # only process if the file is not empty
        self.full_file_path = self.csv_dir + self.file_to_process.replace('.',"_") + '.csv'

        if os.path.getsize(self.full_file_path) > 0:
            self.csv_to_work_table(work_table_obj)

    def df_row_to_dict(self,row,columns):

        output_dict = {}

        for col in columns:
            output_dict[col] = row[columns.index(col)]

        output_dict['process_status'] = ProcessStatus.objects.get(status_text='TO_PROCESS')
        output_dict['request_guid'] = self.request_guid

        if 'Health_Camps' in self.file_to_process:
              region = self.file_to_process.replace('Health_Camps_','').replace('.csv','')

              output_dict['region'] = region


        return output_dict


    def build_dataframe(self):



        df = pd.read_csv(self.full_file_path, error_bad_lines = False)  # YOU NEED TO HANDLE ERRORS!

        return df

    def csv_to_work_table(self, work_table_object):

        df = self.build_dataframe()
        df_columns = [col.lower().replace('-','_') for col in df.columns]

        for i, row in enumerate(df.values):
            to_create = self.df_row_to_dict(row,df_columns)

            try:
                created = work_table_object.objects.create(**to_create)
            except IntegrityError:
                print 'key: ' +  row[df_columns.index('KEY')] + ' already exists...'
