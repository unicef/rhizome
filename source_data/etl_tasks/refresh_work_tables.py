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


from source_data.models import VCMBirthRecord,VCMSummaryNew,VCMSettlement, ProcessStatus



class WorkTableTask(object):

    def __init__(self,request_guid,file_to_process):
        print 'initializing work table task'

        self.request_guid = request_guid
        self.file_to_process = file_to_process


        self.csv_dir = '/Users/johndingee_seed/code/polio/static/odk_source/csv_exports/'
        self.columns = odk_settings.HEADER_DICT[self.file_to_process]

        self.file_to_function_map = {
            "VCM_Sett_Coordinates_1_2.csv" : self.ingest_sett_coordinates,
            "New_VCM_Summary.csv" : self.ingest_vcm_summary_new
        }

        # prep the data frame
        self.df = self.build_dataframe(self.file_to_process)
        # execute the relevant function
        fn = self.file_to_function_map[self.file_to_process]

        x = fn()


    def df_row_to_dict(self,row):

        output_dict = {}

        for col in self.columns:
            output_dict[col] = row[self.columns.index(col)]

        output_dict['process_status'] = ProcessStatus.objects.get(status_text='TO_PROCESS')
        output_dict['request_guid'] = self.request_guid

        return output_dict


    def build_dataframe(self,file_name):

        f = self.csv_dir + file_name

        df = pd.read_csv(f, error_bad_lines = False)  # YOU NEED TO HANDLE ERRORS!

        return df

    def ingest_sett_coordinates(self):

        for i,row in enumerate(self.df.values):
            to_create = self.df_row_to_dict(row)

            try:
                created = VCMSettlement.objects.create(**to_create)
            except IntegrityError:
                print 'key: ' +  row[self.columns.index('KEY')] + ' already exists...'


    def ingest_vcm_summary_new(self):

        for i, row in enumerate(self.df.values):
            to_create = self.df_row_to_dict(row)
            try:
                created = VCMSummaryNew.objects.create(**to_create)
            except IntegrityError:
                print 'key: ' +  row[self.columns.index('KEY')] + ' already exists...'



    def ingest_birth_records(self):

        with open ("/Users/johndingee_seed/Desktop/ALL_ODK_DATA_8_25/VCM_Birth_Record.csv") as f:
            f_reader = csv.reader(f, delimiter = ',', quotechar='"')
            for i, row in enumerate(f_reader):
                if i > 0:
                    created = VCMBirthRecord.objects.create(
                        SubmissionDate =row[0], \
                        deviceid =row[1], \
                        simserial =row[2], \
                        phonenumber =row[3], \
                        DateOfReport =row[4], \
                        DateReport =row[5], \
                        SettlementCode =row[6], \
                        HouseHoldNumber =row[7], \
                        DOB =row[8], \
                        NameOfChild =row[9], \
                        VCM0Dose =row[10], \
                        VCMRILink =row[11], \
                        VCMNameCAttended =row[12], \
                        meta_instanceID =row[13], \
                        KEY =row[13]
                        )



if __name__ == "__main__":
    t = WorkTableTask('blasfbafbfa')
    t.ingest_sett_coordinates()
    # t.build_dataframe('VCM_Sett_Coordinates_1_2.csv')
