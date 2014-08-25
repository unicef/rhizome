import csv
import sys, os
sys.path.append('/Users/johndingee_seed/code/polio/polio')
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
from django.conf import settings


from models import VCMBirthRecord


def main():
    print 'yo'

    with open ("/Users/johndingee_seed/Desktop/csv_exports/VCM_Summary.csv") as f:
        f_reader = csv.reader(f, delimiter = ',', quotechar="|")
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
                    # meta_instanceID =row[13], \
                    # KEY =row[13]
                    )


if __name__ == "__main__":
    main()
