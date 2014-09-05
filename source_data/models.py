from django.db import models
import hashlib
import random
from datetime import datetime

class EtlJob(models.Model):

    date_attempted = models.DateTimeField()
    date_completed = models.DateTimeField(null=True)
    task_name = models.CharField(max_length=55)
    status = models.CharField(max_length=10)
    guid = models.CharField(primary_key=True, max_length=40)

    def save(self, *args, **kwargs):
        if not self.guid:
            self.guid = hashlib.sha1(str(random.random())).hexdigest()

        super(EtlJob, self).save(*args, **kwargs)


class ProcessStatus(models.Model):
    status_text = models.CharField(max_length=25)
    status_description = models.CharField(max_length=255)

    def __unicode__(self):
        return unicode(self.status_text)

    class Meta:
        app_label = 'source_data'


class VCMBirthRecord(models.Model):

    SubmissionDate = models.CharField(max_length=255)
    deviceid = models.CharField(max_length=255)
    simserial = models.CharField(max_length=255)
    phonenumber = models.CharField(max_length=255)
    DateOfReport = models.CharField(max_length=255)
    DateReport = models.CharField(max_length=255)
    SettlementCode = models.CharField(max_length=255)
    HouseHoldNumber = models.CharField(max_length=255)
    DOB = models.CharField(max_length=255)
    NameOfChild = models.CharField(max_length=255)
    VCM0Dose = models.CharField(max_length=255)
    VCMRILink = models.CharField(max_length=255)
    VCMNameCAttended = models.CharField(max_length=255)
    meta_instanceID = models.CharField(max_length=255)
    KEY = models.CharField(max_length=255,unique=True)
    process_status = models.ForeignKey(ProcessStatus)
    request_guid = models.CharField(max_length=255)
    created_at = models.DateTimeField(default=datetime.now())

    def __unicode__(self):
        return unicode(self.NameOfChild)

    class Meta:
        app_label = 'source_data'

class VCMSummaryNew(models.Model):
    SubmissionDate = models.CharField(max_length=255)
    deviceid = models.CharField(max_length=255)
    simserial = models.CharField(max_length=255)
    phonenumber = models.CharField(max_length=255)
    DateOfReport = models.CharField(max_length=255)
    Date_Implement = models.CharField(max_length=255)
    SettlementCode = models.CharField(max_length=255)
    CensusNewBornsF = models.CharField(max_length=255)
    CensusNewBornsM = models.CharField(max_length=255)
    Tot_Newborns = models.CharField(max_length=255)
    Census2_11MoF = models.CharField(max_length=255)
    Census2_11MoM = models.CharField(max_length=255)
    Tot_2_11Months = models.CharField(max_length=255)
    Census12_59MoF = models.CharField(max_length=255)
    Census12_59MoM = models.CharField(max_length=255)
    Tot_12_59Months = models.CharField(max_length=255)
    Tot_Census = models.CharField(max_length=255)
    VaxNewBornsF = models.CharField(max_length=255)
    VaxNewBornsM = models.CharField(max_length=255)
    Tot_VaxNewBorn = models.CharField(max_length=255)
    display_vax2 = models.CharField(max_length=255)
    display_vax3 = models.CharField(max_length=255)
    display_vax1 = models.CharField(max_length=255)
    Vax2_11MoF = models.CharField(max_length=255)
    Vax2_11MoM = models.CharField(max_length=255)
    Tot_Vax2_11Mo = models.CharField(max_length=255)
    display_vax4 = models.CharField(max_length=255)
    display_vax5 = models.CharField(max_length=255)
    display_vax6 = models.CharField(max_length=255)
    Vax12_59MoF = models.CharField(max_length=255)
    Vax12_59MoM = models.CharField(max_length=255)
    Tot_Vax12_59Mo = models.CharField(max_length=255)
    Tot_Vax = models.CharField(max_length=255)
    Tot_Missed = models.CharField(max_length=255)
    display_vax7 = models.CharField(max_length=255)
    display_vax8 = models.CharField(max_length=255)
    display_vax9 = models.CharField(max_length=255)
    display_msd1 = models.CharField(max_length=255)
    display_msd2 = models.CharField(max_length=255)
    group_msd_chd_Msd_PlaygroundF = models.CharField(max_length=255)
    group_msd_chd_Msd_PlaygroundM = models.CharField(max_length=255)
    group_msd_chd_Msd_SocEventF = models.CharField(max_length=255)
    group_msd_chd_Msd_SocEventM = models.CharField(max_length=255)
    group_msd_chd_Msd_MarketF = models.CharField(max_length=255)
    group_msd_chd_Msd_MarketM = models.CharField(max_length=255)
    group_msd_chd_Msd_FarmF = models.CharField(max_length=255)
    group_msd_chd_Msd_FarmM = models.CharField(max_length=255)
    group_msd_chd_Msd_SchoolF = models.CharField(max_length=255)
    group_msd_chd_Msd_SchoolM = models.CharField(max_length=255)
    group_msd_chd_Msd_ChildSickF = models.CharField(max_length=255)
    group_msd_chd_Msd_ChildSickM = models.CharField(max_length=255)
    group_msd_chd_Msd_SideEffectsF = models.CharField(max_length=255)
    group_msd_chd_Msd_SideEffectsM = models.CharField(max_length=255)
    group_msd_chd_Msd_NoFeltNeedF = models.CharField(max_length=255)
    group_msd_chd_Msd_NoFeltNeedM = models.CharField(max_length=255)
    group_msd_chd_Msd_TooManyRoundsF = models.CharField(max_length=255)
    group_msd_chd_Msd_TooManyRoundsM = models.CharField(max_length=255)
    group_msd_chd_Msd_RelBeliefsF = models.CharField(max_length=255)
    group_msd_chd_Msd_RelBeliefsM = models.CharField(max_length=255)
    group_msd_chd_Msd_PolDiffsF = models.CharField(max_length=255)
    group_msd_chd_Msd_PolDiffsM = models.CharField(max_length=255)
    group_msd_chd_Msd_UnhappyWTeamF = models.CharField(max_length=255)
    group_msd_chd_Msd_UnhappyWTeamM = models.CharField(max_length=255)
    group_msd_chd_Msd_NoPlusesF = models.CharField(max_length=255)
    group_msd_chd_Msd_NoPlusesM = models.CharField(max_length=255)
    group_msd_chd_Msd_NoGovtServicesF = models.CharField(max_length=255)
    group_msd_chd_Msd_NoGovtServicesM = models.CharField(max_length=255)
    group_msd_chd_Msd_PolioUncommonF = models.CharField(max_length=255)
    group_msd_chd_Msd_PolioUncommonM = models.CharField(max_length=255)
    group_msd_chd_Msd_PolioHasCureF = models.CharField(max_length=255)
    group_msd_chd_Msd_PolioHasCureM = models.CharField(max_length=255)
    group_msd_chd_Msd_OtherProtectionF = models.CharField(max_length=255)
    group_msd_chd_Msd_OtherProtectionM = models.CharField(max_length=255)
    group_msd_chd_Msd_NoConsentF = models.CharField(max_length=255)
    group_msd_chd_Msd_NoConsentM = models.CharField(max_length=255)
    group_msd_chd_Msd_HHNotVisitedF = models.CharField(max_length=255)
    group_msd_chd_Msd_HHNotVisitedM = models.CharField(max_length=255)
    group_msd_chd_Msd_SecurityF = models.CharField(max_length=255)
    group_msd_chd_Msd_SecurityM = models.CharField(max_length=255)
    group_msd_chd_Msd_AgedOutF = models.CharField(max_length=255)
    group_msd_chd_Msd_AgedOutM = models.CharField(max_length=255)
    group_msd_chd_Msd_FamilyMovedF = models.CharField(max_length=255)
    group_msd_chd_Msd_FamilyMovedM = models.CharField(max_length=255)
    group_msd_chd_Msd_ChildDiedF = models.CharField(max_length=255)
    group_msd_chd_Msd_ChildDiedM = models.CharField(max_length=255)
    group_msd_chd_Tot_Missed_Check = models.CharField(max_length=255)
    group_msd_chd_display_msd3 = models.CharField(max_length=255)
    spec_grp_choice = models.CharField(max_length=255)
    group_spec_events_Spec_ZeroDose = models.CharField(max_length=255)
    group_spec_events_Spec_PregnantMother = models.CharField(max_length=255)
    group_spec_events_Spec_Newborn = models.CharField(max_length=255)
    group_spec_events_Spec_VCMAttendedNCer = models.CharField(max_length=255)
    group_spec_events_Spec_CMAMReferral = models.CharField(max_length=255)
    group_spec_events_Spec_RIReferral = models.CharField(max_length=255)
    group_spec_events_Spec_AFPCase = models.CharField(max_length=255)
    group_spec_events_Spec_MslsCase = models.CharField(max_length=255)
    group_spec_events_Spec_OtherDisease = models.CharField(max_length=255)
    group_spec_events_Spec_FIC = models.CharField(max_length=255)
    meta_instanceID = models.CharField(max_length=255)
    KEY = models.CharField(max_length=255, unique=True)
    process_status = models.ForeignKey(ProcessStatus)
    request_guid = models.CharField(max_length=255)
    created_at = models.DateTimeField(default=datetime.now())

    def __unicode__(self):
        return unicode('Hello')

    class Meta:
        app_label = 'source_data'


class VCMSettlement(models.Model):

    SubmissionDate = models.CharField(max_length=255)
    deviceid = models.CharField(max_length=255)
    simserial = models.CharField(max_length=255)
    phonenumber = models.CharField(max_length=255)
    DateRecorded = models.CharField(max_length=255)
    SettlementCode = models.CharField(max_length=255)
    SettlementName = models.CharField(max_length=255)
    VCMName = models.CharField(max_length=255)
    VCMPhone = models.CharField(max_length=255)
    SettlementGPS_Latitude = models.CharField(max_length=255)
    SettlementGPS_Longitude = models.CharField(max_length=255)
    SettlementGPS_Altitude = models.CharField(max_length=255)
    SettlementGPS_Accuracy = models.CharField(max_length=255)
    meta_instanceID = models.CharField(max_length=255)
    KEY = models.CharField(max_length=255, unique=True)
    process_status = models.ForeignKey(ProcessStatus)
    request_guid = models.CharField(max_length=255)
    created_at  = models.DateTimeField(default=datetime.now())


    def __unicode__(self):
        return unicode(self.SettlementName)

    class Meta:
        app_label = 'source_data'
