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
            "VCM_Sett_Coordinates_1_2.csv" : VCMSettlement,
            "New_VCM_Summary.csv" : VCMSummaryNew,
            "VCM_Summary.csv" : VCMSummaryOld,
            "cluster_supervisor.csv" : ClusterSupervisor,
            "Phone Inventory.csv": PhoneInventory,
            "VCM_Birth_Record.csv": VCMBirthRecord,
            "activity_report.csv": ActivityReport,
            "VWS_Register.csv" :VWSRegister ,
            "Practice_VCM_Sett_Coordinates_1_2.csv": PracticeVCMSettCoordinates,
            "Pax_List_Report_Training.csv" :PaxListReportTraining,
            "Practice_VCM_Summary.csv":PracticeVCMSummary,
            "Practice_VCM_Birth_Record.csv": PracticeVCMBirthRecord,

            "Health_Camps_Yobe.csv": HealthCamp,
            "Health_Camps_Kebbi.csv": HealthCamp,
            'Health_Camps_Bauchi.csv': HealthCamp,
            'Health_Camps_Jigawa.csv': HealthCamp,
            'Health_Camps_Kano.csv': HealthCamp,
            'Health_Camps_Katsina.csv': HealthCamp,
            'Health_Camps_Sokoto.csv': HealthCamp,
            'Health_Camps_Kaduna.csv': HealthCamp,
        }

        # this below shoudl be a configuration
        self.csv_dir = '/Users/johndingee_seed/code/polio/static/odk_source/csv_exports/'
        self.columns = odk_settings.HEADER_DICT[self.file_to_process]

        # execute the relevant function
        work_table_obj = self.file_to_function_map[self.file_to_process]

        # only process if the file is not empty
        if os.path.getsize(self.csv_dir + file_to_process) > 0:
            self.csv_to_work_table(work_table_obj)

    def df_row_to_dict(self,row):

        output_dict = {}

        for col in self.columns:
            output_dict[col] = row[self.columns.index(col)]

        output_dict['process_status'] = ProcessStatus.objects.get(status_text='TO_PROCESS')
        output_dict['request_guid'] = self.request_guid

        if 'Health_Camps' in self.file_to_process:
              region = self.file_to_process.replace('Health_Camps_','').replace('.csv','')

              output_dict['region'] = region



        return output_dict


    def build_dataframe(self):

        f = self.csv_dir + self.file_to_process

        df = pd.read_csv(f, error_bad_lines = False)  # YOU NEED TO HANDLE ERRORS!

        return df

    def csv_to_work_table(self, work_table_object):

        df = self.build_dataframe()


        for i, row in enumerate(df.values):
            to_create = self.df_row_to_dict(row)

            try:
                created = work_table_object.objects.create(**to_create)
            except IntegrityError:
                print 'key: ' +  row[self.columns.index('KEY')] + ' already exists...'



if __name__ == "__main__":
    t = WorkTableTask('blasfbafbfa')
    t.ingest_sett_coordinates()
    # t.build_dataframe('VCM_Sett_Coordinates_1_2.csv')
