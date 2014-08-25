import csv
import sys, os
sys.path.append('/Users/johndingee_seed/code/polio/polio')
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
from django.conf import settings


from models import VCMBirthRecord,VCMSummaryNew


def ingest_birth_records():

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

def ingest_vcm_summary_new():

    with open ("/Users/johndingee_seed/Desktop/ALL_ODK_DATA_8_25/New_VCM_Summary.csv") as f:
        f_reader = csv.reader(f, delimiter = ',', quotechar='"')
        for i, row in enumerate(f_reader):
            if i > 0:
                # print row
                print i
                created = VCMSummaryNew.objects.create(
                # created = VCMSummaryNew.objects.get_or_create(
                    SubmissionDate = row[0], \
                    deviceid = row[1], \
                    simserial = row[2], \
                    phonenumber = row[3], \
                    DateOfReport = row[4], \
                    Date_Implement = row[5], \
                    SettlementCode = row[6], \
                    CensusNewBornsF = row[7], \
                    CensusNewBornsM = row[8], \
                    Tot_Newborns = row[9], \
                    Census2_11MoF = row[10], \
                    Census2_11MoM = row[11], \
                    Tot_2_11Months = row[12], \
                    Census12_59MoF = row[13], \
                    Census12_59MoM = row[14], \
                    Tot_12_59Months = row[15], \
                    Tot_Census = row[16], \
                    VaxNewBornsF = row[17], \
                    VaxNewBornsM = row[18], \
                    Tot_VaxNewBorn = row[19], \
                    display_vax2 = row[20], \
                    display_vax3 = row[21], \
                    display_vax1 = row[22], \
                    Vax2_11MoF = row[23], \
                    Vax2_11MoM = row[24], \
                    Tot_Vax2_11Mo = row[25], \
                    display_vax4 = row[26], \
                    display_vax5 = row[27], \
                    display_vax6 = row[28], \
                    Vax12_59MoF = row[29], \
                    Vax12_59MoM = row[30], \
                    Tot_Vax12_59Mo = row[31], \
                    Tot_Vax = row[32], \
                    Tot_Missed = row[33], \
                    display_vax7 = row[34], \
                    display_vax8 = row[35], \
                    display_vax9 = row[36], \
                    display_msd1 = row[37], \
                    display_msd2 = row[38], \
                    group_msd_chd_Msd_PlaygroundF = row[39], \
                    group_msd_chd_Msd_PlaygroundM = row[40], \
                    group_msd_chd_Msd_SocEventF = row[41], \
                    group_msd_chd_Msd_SocEventM = row[42], \
                    group_msd_chd_Msd_MarketF = row[43], \
                    group_msd_chd_Msd_MarketM = row[44], \
                    group_msd_chd_Msd_FarmF = row[45], \
                    group_msd_chd_Msd_FarmM = row[46], \
                    group_msd_chd_Msd_SchoolF = row[47], \
                    group_msd_chd_Msd_SchoolM = row[48], \
                    group_msd_chd_Msd_ChildSickF = row[49], \
                    group_msd_chd_Msd_ChildSickM = row[50], \
                    group_msd_chd_Msd_SideEffectsF = row[51], \
                    group_msd_chd_Msd_SideEffectsM = row[52], \
                    group_msd_chd_Msd_NoFeltNeedF = row[53], \
                    group_msd_chd_Msd_NoFeltNeedM = row[54], \
                    group_msd_chd_Msd_TooManyRoundsF = row[55], \
                    group_msd_chd_Msd_TooManyRoundsM = row[56], \
                    group_msd_chd_Msd_RelBeliefsF = row[57], \
                    group_msd_chd_Msd_RelBeliefsM = row[58], \
                    group_msd_chd_Msd_PolDiffsF = row[59], \
                    group_msd_chd_Msd_PolDiffsM = row[60], \
                    group_msd_chd_Msd_UnhappyWTeamF = row[61], \
                    group_msd_chd_Msd_UnhappyWTeamM = row[62], \
                    group_msd_chd_Msd_NoPlusesF = row[63], \
                    group_msd_chd_Msd_NoPlusesM = row[64], \
                    group_msd_chd_Msd_NoGovtServicesF = row[65], \
                    group_msd_chd_Msd_NoGovtServicesM = row[66], \
                    group_msd_chd_Msd_PolioUncommonF = row[67], \
                    group_msd_chd_Msd_PolioUncommonM = row[68], \
                    group_msd_chd_Msd_PolioHasCureF = row[69], \
                    group_msd_chd_Msd_PolioHasCureM = row[70], \
                    group_msd_chd_Msd_OtherProtectionF = row[71], \
                    group_msd_chd_Msd_OtherProtectionM = row[72], \
                    group_msd_chd_Msd_NoConsentF = row[73], \
                    group_msd_chd_Msd_NoConsentM = row[74], \
                    group_msd_chd_Msd_HHNotVisitedF = row[75], \
                    group_msd_chd_Msd_HHNotVisitedM = row[76], \
                    group_msd_chd_Msd_SecurityF = row[76], \
                    group_msd_chd_Msd_SecurityM = row[77], \
                    group_msd_chd_Msd_AgedOutF = row[78], \
                    group_msd_chd_Msd_AgedOutM = row[79], \
                    group_msd_chd_Msd_FamilyMovedF = row[80], \
                    group_msd_chd_Msd_FamilyMovedM = row[81], \
                    group_msd_chd_Msd_ChildDiedF = row[82], \
                    group_msd_chd_Msd_ChildDiedM = row[83], \
                    group_msd_chd_Tot_Missed_Check = row[84], \
                    group_msd_chd_display_msd3 = row[85], \
                    spec_grp_choice = row[86], \
                    group_spec_events_Spec_ZeroDose = row[87], \
                    group_spec_events_Spec_PregnantMother = row[88], \
                    group_spec_events_Spec_Newborn = row[89], \
                    group_spec_events_Spec_VCMAttendedNCer = row[90], \
                    group_spec_events_Spec_CMAMReferral = row[91], \
                    group_spec_events_Spec_RIReferral = row[92], \
                    group_spec_events_Spec_AFPCase = row[93], \
                    group_spec_events_Spec_MslsCase = row[94], \
                    group_spec_events_Spec_OtherDisease = row[95], \
                    group_spec_events_Spec_FIC = row[96], \
                    meta_instanceID = row[97], \
                    KEY = row[98]
                    )

def create_new_indicators_from_vcm_summary():
    with open ("/Users/johndingee_seed/Desktop/ALL_ODK_DATA_8_25/New_VCM_Summary.csv") as f:
        f_reader = csv.reader(f, delimiter = ',', quotechar='"')
        for i, row in enumerate(f_reader):
            if i == 0:
                print row






if __name__ == "__main__":
    create_new_indicators_from_vcm_summary()
