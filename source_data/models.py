import hashlib
import random

from datetime import datetime
from django.db import models
from django.contrib.auth.models import User

from datapoints.models import Source, Indicator, Region, Campaign


    ###################
    ####### ETL #######
    ###################

class EtlJob(models.Model):

    date_attempted = models.DateTimeField(default=datetime.now())
    date_completed = models.DateTimeField(null=True)
    task_name = models.CharField(max_length=55)
    status = models.CharField(max_length=10)
    guid = models.CharField(primary_key=True, max_length=40)
    cron_guid = models.CharField(max_length=40)
    error_msg = models.TextField(null=True)
    success_msg = models.CharField(max_length=255)

    class Meta:
        ordering = ('-date_attempted',)


    def save(self, *args, **kwargs):

        if not self.guid:
            self.guid = hashlib.sha1(str(random.random())).hexdigest()

        if not self.date_completed:
            self.date_completed = datetime.now()

        super(EtlJob, self).save(*args, **kwargs)



class ProcessStatus(models.Model):

    status_text = models.CharField(max_length=25)
    status_description = models.CharField(max_length=255)

    def __unicode__(self):
        return unicode(self.status_text)

    class Meta:
        app_label = 'source_data'

    ##########################
    ####### CSV UPLOAD #######
    ##########################

class Document(models.Model):

    docfile = models.FileField(upload_to='documents/%Y/%m/%d',null=True)
    doc_text = models.TextField(null=True)
    created_by = models.ForeignKey(User)
    guid = models.CharField(max_length=255)
    source_datapoint_count = models.IntegerField(null=True)
    master_datapoint_count = models.IntegerField(null=True)
    is_processed = models.BooleanField(default=False)
    source = models.ForeignKey(Source)

    class Meta:
        unique_together = ('docfile','doc_text')
        ordering = ('-id',)

    def save(self, *args, **kwargs):
        if not self.guid:
            self.guid = hashlib.sha1(str(random.random())).hexdigest()

        super(Document, self).save(*args, **kwargs)


class SourceDataPoint(models.Model):
    '''
    source will be odk or csv upload. source_id (for odk) is the guid
    of the submissions.  This is not unique to this table as there are many
    indicators per submission. For a CSV upload the source_id is csv upload,
    the source guid is the uniquesoc and the document id is traced here as well.
    for ODK, the document ID will coorespond to the form (vcm_summary_new)
    '''

    region_code = models.CharField(max_length=255)
    campaign_string = models.CharField(max_length=255)
    indicator_string = models.CharField(max_length=255)
    cell_value = models.CharField(max_length=255,null=True)
    row_number= models.IntegerField()
    source = models.ForeignKey(Source)
    document = models.ForeignKey(Document)
    source_guid = models.CharField(max_length=255)
    status = models.ForeignKey(ProcessStatus)
    guid = models.CharField(unique=True, max_length=255)
    created_at = models.DateTimeField(default=datetime.now())


    def save(self, *args, **kwargs):
        if not self.guid:
            self.guid = hashlib.sha1(str(random.random())).hexdigest()

        super(SourceDataPoint, self).save(*args, **kwargs)


    def get_val(self):
        return self.cell_value


    class Meta:
        app_label = 'source_data'
        unique_together = ('source','source_guid','indicator_string')
        db_table = 'source_datapoint'

    ###################
    #### META MAP #####
    ###################


class SourceRegion(models.Model):

    region_code = models.CharField(max_length=255, null=False, unique=True)
    lat = models.CharField(max_length=255, null=True)
    lon = models.CharField(max_length=255, null=True)
    parent_name = models.CharField(max_length=255, null=True)
    parent_code = models.CharField(max_length=255, null=True)
    region_type = models.CharField(max_length=255, null=True)
    country = models.CharField(max_length=255, null=True)
    source_guid = models.CharField(max_length=255)
    document = models.ForeignKey(Document)
    is_high_risk = models.BooleanField(default=False)

    class Meta:
        db_table = 'source_region'

    def __unicode__(self):

        if self.region_type:

            return self.region_code + ' (' + self.region_type + ')'

        else:
            return self.region_code + '( UNKNOWN REGION TYPE )'

class SourceRegionPolygon(models.Model):

    source_region = models.ForeignKey(SourceRegion, unique=True)
    shape_len  = models.FloatField()
    shape_area = models.FloatField()
    polygon = models.TextField()

    class Meta:
        db_table = 'source_region_polygon'


class SourceIndicator(models.Model):

    indicator_string = models.CharField(max_length=255,unique=True)
    source_guid = models.CharField(max_length=255)
    document = models.ForeignKey(Document)


    class Meta:
        db_table = 'source_indicator'

    def __unicode__(self):
        return self.indicator_string


class SourceCampaign(models.Model):

    campaign_string = models.CharField(max_length=255,unique=True)
    source_guid = models.CharField(max_length=255)
    document = models.ForeignKey(Document)

    class Meta:
        db_table = 'source_campaign'

    def __unicode__(self):
        return self.campaign_string


class RegionMap(models.Model):

    master_object = models.ForeignKey(Region)
    source_object = models.ForeignKey(SourceRegion,unique=True)
    mapped_by = models.ForeignKey(User)

    class Meta:
        db_table = 'region_map'


class IndicatorMap(models.Model):

    master_object = models.ForeignKey(Indicator)
    source_object = models.ForeignKey(SourceIndicator,unique=True)
    mapped_by = models.ForeignKey(User)

    class Meta:
        db_table = 'indicator_map'


class CampaignMap(models.Model):

    master = models.ForeignKey(Campaign)
    source = models.ForeignKey(SourceCampaign,unique=True)
    mapped_by = models.ForeignKey(User)

    class Meta:
        db_table = 'campaign_map'


    ###################
    ####### ODK #######
    ###################


class VCMBirthRecord(models.Model):

    submissiondate = models.CharField(max_length=255)
    deviceid = models.CharField(max_length=255)
    simserial = models.CharField(max_length=255)
    phonenumber = models.CharField(max_length=255)
    dateofreport = models.CharField(max_length=255)
    datereport = models.CharField(max_length=255)
    settlementcode = models.CharField(max_length=255)
    householdnumber = models.CharField(max_length=255)
    dob = models.CharField(max_length=255)
    nameofchild = models.CharField(max_length=255)
    vcm0dose = models.CharField(max_length=255)
    vcmrilink = models.CharField(max_length=255)
    vcmnamecattended = models.CharField(max_length=255)
    meta_instanceid = models.CharField(max_length=255)
    key = models.CharField(max_length=255,unique=True)
    process_status = models.ForeignKey(ProcessStatus)
    request_guid = models.CharField(max_length=255)
    created_at = models.DateTimeField(default=datetime.now())

    def __unicode__(self):
        return unicode(self.NameOfChild)

    class Meta:
        app_label = 'source_data'

class VCMSummaryNew(models.Model):
    submissiondate = models.CharField(max_length=255)
    deviceid = models.CharField(max_length=255)
    simserial = models.CharField(max_length=255)
    phonenumber = models.CharField(max_length=255)
    dateofreport = models.CharField(max_length=255)
    date_implement = models.CharField(max_length=255)
    settlementcode = models.CharField(max_length=255)
    censusnewbornsf = models.CharField(max_length=255)
    censusnewbornsm = models.CharField(max_length=255)
    tot_newborns = models.CharField(max_length=255)
    census2_11mof = models.CharField(max_length=255)
    census2_11mom = models.CharField(max_length=255)
    tot_2_11months = models.CharField(max_length=255)
    census12_59mof = models.CharField(max_length=255)
    census12_59mom = models.CharField(max_length=255)
    tot_12_59months = models.CharField(max_length=255)
    tot_census = models.CharField(max_length=255)
    vaxnewbornsf = models.CharField(max_length=255)
    vaxnewbornsm = models.CharField(max_length=255)
    tot_vaxnewborn = models.CharField(max_length=255)
    display_vax2 = models.CharField(max_length=255)
    display_vax3 = models.CharField(max_length=255)
    display_vax1 = models.CharField(max_length=255)
    vax2_11mof = models.CharField(max_length=255)
    vax2_11mom = models.CharField(max_length=255)
    tot_vax2_11mo = models.CharField(max_length=255)
    display_vax4 = models.CharField(max_length=255)
    display_vax5 = models.CharField(max_length=255)
    display_vax6 = models.CharField(max_length=255)
    vax12_59mof = models.CharField(max_length=255)
    vax12_59mom = models.CharField(max_length=255)
    tot_vax12_59mo = models.CharField(max_length=255)
    tot_vax = models.CharField(max_length=255)
    tot_missed = models.CharField(max_length=255)
    display_vax7 = models.CharField(max_length=255)
    display_vax8 = models.CharField(max_length=255)
    display_vax9 = models.CharField(max_length=255)
    display_msd1 = models.CharField(max_length=255)
    display_msd2 = models.CharField(max_length=255)
    group_msd_chd_msd_playgroundf = models.CharField(max_length=255)
    group_msd_chd_msd_playgroundm = models.CharField(max_length=255)
    group_msd_chd_msd_soceventf = models.CharField(max_length=255)
    group_msd_chd_msd_soceventm = models.CharField(max_length=255)
    group_msd_chd_msd_marketf = models.CharField(max_length=255)
    group_msd_chd_msd_marketm = models.CharField(max_length=255)
    group_msd_chd_msd_farmf = models.CharField(max_length=255)
    group_msd_chd_msd_farmm = models.CharField(max_length=255)
    group_msd_chd_msd_schoolf = models.CharField(max_length=255)
    group_msd_chd_msd_schoolm = models.CharField(max_length=255)
    group_msd_chd_msd_childsickf = models.CharField(max_length=255)
    group_msd_chd_msd_childsickm = models.CharField(max_length=255)
    group_msd_chd_msd_sideeffectsf = models.CharField(max_length=255)
    group_msd_chd_msd_sideeffectsm = models.CharField(max_length=255)
    group_msd_chd_msd_nofeltneedf = models.CharField(max_length=255)
    group_msd_chd_msd_nofeltneedm = models.CharField(max_length=255)
    group_msd_chd_msd_toomanyroundsf = models.CharField(max_length=255)
    group_msd_chd_msd_toomanyroundsm = models.CharField(max_length=255)
    group_msd_chd_msd_relbeliefsf = models.CharField(max_length=255)
    group_msd_chd_msd_relbeliefsm = models.CharField(max_length=255)
    group_msd_chd_msd_poldiffsf = models.CharField(max_length=255)
    group_msd_chd_msd_poldiffsm = models.CharField(max_length=255)
    group_msd_chd_msd_unhappywteamf = models.CharField(max_length=255)
    group_msd_chd_msd_unhappywteamm = models.CharField(max_length=255)
    group_msd_chd_msd_noplusesf = models.CharField(max_length=255)
    group_msd_chd_msd_noplusesm = models.CharField(max_length=255)
    group_msd_chd_msd_nogovtservicesf = models.CharField(max_length=255)
    group_msd_chd_msd_nogovtservicesm = models.CharField(max_length=255)
    group_msd_chd_msd_poliouncommonf = models.CharField(max_length=255)
    group_msd_chd_msd_poliouncommonm = models.CharField(max_length=255)
    group_msd_chd_msd_poliohascuref = models.CharField(max_length=255)
    group_msd_chd_msd_poliohascurem = models.CharField(max_length=255)
    group_msd_chd_msd_otherprotectionf = models.CharField(max_length=255)
    group_msd_chd_msd_otherprotectionm = models.CharField(max_length=255)
    group_msd_chd_msd_noconsentf = models.CharField(max_length=255)
    group_msd_chd_msd_noconsentm = models.CharField(max_length=255)
    group_msd_chd_msd_hhnotvisitedf = models.CharField(max_length=255)
    group_msd_chd_msd_hhnotvisitedm = models.CharField(max_length=255)
    group_msd_chd_msd_securityf = models.CharField(max_length=255)
    group_msd_chd_msd_securitym = models.CharField(max_length=255)
    group_msd_chd_msd_agedoutf = models.CharField(max_length=255)
    group_msd_chd_msd_agedoutm = models.CharField(max_length=255)
    group_msd_chd_msd_familymovedf = models.CharField(max_length=255)
    group_msd_chd_msd_familymovedm = models.CharField(max_length=255)
    group_msd_chd_msd_childdiedf = models.CharField(max_length=255)
    group_msd_chd_msd_childdiedm = models.CharField(max_length=255)
    group_msd_chd_tot_missed_check = models.CharField(max_length=255)
    group_msd_chd_display_msd3 = models.CharField(max_length=255)
    spec_grp_choice = models.CharField(max_length=255)
    group_spec_events_spec_zerodose = models.CharField(max_length=255)
    group_spec_events_spec_pregnantmother = models.CharField(max_length=255)
    group_spec_events_spec_newborn = models.CharField(max_length=255)
    group_spec_events_spec_vcmattendedncer = models.CharField(max_length=255)
    group_spec_events_spec_cmamreferral = models.CharField(max_length=255)
    group_spec_events_spec_rireferral = models.CharField(max_length=255)
    group_spec_events_spec_afpcase = models.CharField(max_length=255)
    group_spec_events_spec_mslscase = models.CharField(max_length=255)
    group_spec_events_spec_otherdisease = models.CharField(max_length=255)
    group_spec_events_spec_fic = models.CharField(max_length=255)
    meta_instanceid = models.CharField(max_length=255)
    key = models.CharField(max_length=255, unique=True)
    process_status = models.ForeignKey(ProcessStatus)
    request_guid = models.CharField(max_length=255)
    created_at = models.DateTimeField(default=datetime.now())

    def __unicode__(self):
        return unicode('Hello')

    class Meta:
        app_label = 'source_data'


class VCMSettlement(models.Model):

    submissiondate = models.CharField(max_length=255)
    deviceid = models.CharField(max_length=255)
    simserial = models.CharField(max_length=255)
    phonenumber = models.CharField(max_length=255)
    daterecorded = models.CharField(max_length=255)
    settlementcode = models.CharField(max_length=255)
    settlementname = models.CharField(max_length=255)
    vcmname = models.CharField(max_length=255)
    vcmphone = models.CharField(max_length=255)
    settlementgps_latitude = models.CharField(max_length=255)
    settlementgps_longitude = models.CharField(max_length=255)
    settlementgps_altitude = models.CharField(max_length=255)
    settlementgps_accuracy = models.CharField(max_length=255)
    meta_instanceid = models.CharField(max_length=255)
    key = models.CharField(max_length=255, unique=True)
    process_status = models.ForeignKey(ProcessStatus)
    request_guid = models.CharField(max_length=255)
    created_at = models.DateTimeField(default=datetime.now())

    def __unicode__(self):
        return unicode(self.settlementname)

    class Meta:
        app_label = 'source_data'


class VCMSummary(models.Model):
    submissiondate = models.CharField(max_length=255)
    deviceid = models.CharField(max_length=255)
    simserial = models.CharField(max_length=255)
    phonenumber = models.CharField(max_length=255)
    dateofreport = models.CharField(max_length=255)
    date_implement = models.CharField(max_length=255)
    settlementcode = models.CharField(max_length=255)
    censusnewbornsf = models.CharField(max_length=255)
    censusnewbornsm = models.CharField(max_length=255)
    census2_11mof = models.CharField(max_length=255)
    census2_11mom = models.CharField(max_length=255)
    census12_59mof = models.CharField(max_length=255)
    census12_59mom = models.CharField(max_length=255)
    vaxnewbornsf = models.CharField(max_length=255)
    vaxnewbornsm = models.CharField(max_length=255)
    vax2_11mof = models.CharField(max_length=255)
    vax2_11mom = models.CharField(max_length=255)
    vax12_59mof = models.CharField(max_length=255)
    vax12_59mom = models.CharField(max_length=255)
    msd_grp_choice = models.CharField(max_length=255)
    group_msd_chd_msd_playgroundf = models.CharField(max_length=255)
    group_msd_chd_msd_playgroundm = models.CharField(max_length=255)
    group_msd_chd_msd_soceventf = models.CharField(max_length=255)
    group_msd_chd_msd_soceventm = models.CharField(max_length=255)
    group_msd_chd_msd_marketf = models.CharField(max_length=255)
    group_msd_chd_msd_marketm = models.CharField(max_length=255)
    group_msd_chd_msd_farmf = models.CharField(max_length=255)
    group_msd_chd_msd_farmm = models.CharField(max_length=255)
    group_msd_chd_msd_schoolf = models.CharField(max_length=255)
    group_msd_chd_msd_schoolm = models.CharField(max_length=255)
    group_msd_chd_msd_childsickf = models.CharField(max_length=255)
    group_msd_chd_msd_childsickm = models.CharField(max_length=255)
    group_msd_chd_msd_sideeffectsf = models.CharField(max_length=255)
    group_msd_chd_msd_sideeffectsm = models.CharField(max_length=255)
    group_msd_chd_msd_nofeltneedf = models.CharField(max_length=255)
    group_msd_chd_msd_nofeltneedm = models.CharField(max_length=255)
    group_msd_chd_msd_toomanyroundsf = models.CharField(max_length=255)
    group_msd_chd_msd_toomanyroundsm = models.CharField(max_length=255)
    group_msd_chd_msd_relbeliefsf = models.CharField(max_length=255)
    group_msd_chd_msd_relbeliefsm = models.CharField(max_length=255)
    group_msd_chd_msd_poldiffsf = models.CharField(max_length=255)
    group_msd_chd_msd_poldiffsm = models.CharField(max_length=255)
    group_msd_chd_msd_unhappywteamf = models.CharField(max_length=255)
    group_msd_chd_msd_unhappywteamm = models.CharField(max_length=255)
    group_msd_chd_msd_noplusesf = models.CharField(max_length=255)
    group_msd_chd_msd_noplusesm = models.CharField(max_length=255)
    group_msd_chd_msd_nogovtservicesf = models.CharField(max_length=255)
    group_msd_chd_msd_nogovtservicesm = models.CharField(max_length=255)
    group_msd_chd_msd_poliouncommonf = models.CharField(max_length=255)
    group_msd_chd_msd_poliouncommonm = models.CharField(max_length=255)
    group_msd_chd_msd_poliohascuref = models.CharField(max_length=255)
    group_msd_chd_msd_poliohascurem = models.CharField(max_length=255)
    group_msd_chd_msd_otherprotectionf = models.CharField(max_length=255)
    group_msd_chd_msd_otherprotectionm = models.CharField(max_length=255)
    group_msd_chd_msd_noconsentf = models.CharField(max_length=255)
    group_msd_chd_msd_noconsentm = models.CharField(max_length=255)
    group_msd_chd_msd_hhnotvisitedf = models.CharField(max_length=255)
    group_msd_chd_msd_hhnotvisitedm = models.CharField(max_length=255)
    group_msd_chd_msd_noreasonf = models.CharField(max_length=255)
    group_msd_chd_msd_noreasonm = models.CharField(max_length=255)
    group_msd_chd_msd_securityf = models.CharField(max_length=255)
    group_msd_chd_msd_securitym = models.CharField(max_length=255)
    group_msd_chd_msd_agedoutf = models.CharField(max_length=255)
    group_msd_chd_msd_agedoutm = models.CharField(max_length=255)
    group_msd_chd_msd_familymovedf = models.CharField(max_length=255)
    group_msd_chd_msd_familymovedm = models.CharField(max_length=255)
    group_msd_chd_msd_childdiedf = models.CharField(max_length=255)
    group_msd_chd_msd_childdiedm = models.CharField(max_length=255)
    spec_grp_choice = models.CharField(max_length=255)
    group_spec_events_spec_zerodose = models.CharField(max_length=255)
    group_spec_events_spec_pregnantmother = models.CharField(max_length=255)
    group_spec_events_spec_newborn = models.CharField(max_length=255)
    group_spec_events_spec_vcmattendedncer = models.CharField(max_length=255)
    group_spec_events_spec_cmamreferral = models.CharField(max_length=255)
    group_spec_events_spec_rireferral = models.CharField(max_length=255)
    group_spec_events_spec_afpcase = models.CharField(max_length=255)
    group_spec_events_spec_mslscase = models.CharField(max_length=255)
    group_spec_events_spec_otherdisease = models.CharField(max_length=255)
    group_spec_events_spec_fic = models.CharField(max_length=255)
    meta_instanceid = models.CharField(max_length=255)
    key = models.CharField(max_length=255, unique=True)
    process_status = models.ForeignKey(ProcessStatus)
    request_guid = models.CharField(max_length=255)
    created_at = models.DateTimeField(default=datetime.now())

    def __unicode__(self):
        return unicode('hello')

    class Meta:
        app_label = 'source_data'


class ClusterSupervisor(models.Model):
    submissiondate = models.CharField(max_length=255)
    daterecorded = models.CharField(max_length=255)
    start_time = models.CharField(max_length=255)
    end_time = models.CharField(max_length=255)
    instruction = models.CharField(max_length=255)
    supervision_location_latitude = models.CharField(max_length=255)
    supervision_location_longitude = models.CharField(max_length=255)
    supervision_location_altitude = models.CharField(max_length=255)
    supervision_location_accuracy = models.CharField(max_length=255)
    supervisor_title = models.CharField(max_length=255)
    supervisor_name = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    lga = models.CharField(max_length=255)
    supervisee_name = models.CharField(max_length=255)
    num_lgac = models.CharField(max_length=255)
    hrop_endorsed = models.CharField(max_length=255)
    hrop_socialdata = models.CharField(max_length=255)
    hrop_special_pop = models.CharField(max_length=255)
    hrop_activities_planned = models.CharField(max_length=255)
    hrop_activities_conducted = models.CharField(max_length=255)
    hrop_implementation = models.CharField(max_length=255)
    hrop_workplan_aligned = models.CharField(max_length=255)
    coord_smwg_meetings = models.CharField(max_length=255)
    coord_vcm_meeting = models.CharField(max_length=255)
    coord_rfp_meeting = models.CharField(max_length=255)
    vcm_supervision = models.CharField(max_length=255)
    vcm_data = models.CharField(max_length=255)
    vcm_birthtracking = models.CharField(max_length=255)
    ri_supervision = models.CharField(max_length=255)
    fund_transparency = models.CharField(max_length=255)
    meta_instanceid = models.CharField(max_length=255)
    key = models.CharField(max_length=255, unique=True)
    process_status = models.ForeignKey(ProcessStatus)
    request_guid = models.CharField(max_length=255)
    created_at = models.DateTimeField(default=datetime.now())

    def __unicode__(self):
        return unicode('hello')

    class Meta:
        app_label = 'source_data'


class PhoneInventory(models.Model):
    submissiondate = models.CharField(max_length=255)
    meta_instanceid = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    lga = models.CharField(max_length=255)
    colour_phone = models.CharField(max_length=255)
    asset_number = models.CharField(max_length=255)
    telephone_no = models.CharField(max_length=255)
    deviceid = models.CharField(max_length=255)
    key = models.CharField(max_length=255, unique=True)
    process_status = models.ForeignKey(ProcessStatus)
    request_guid = models.CharField(max_length=255)
    created_at = models.DateTimeField(default=datetime.now())

    def __unicode__(self):
        return unicode('hello')

    class Meta:
        app_label = 'source_data'


class ActivityReport(models.Model):
    submissiondate = models.CharField(max_length=255)
    daterecorded = models.CharField(max_length=255)
    start_time = models.CharField(max_length=255)
    endtime = models.CharField(max_length=255)
    settlementgps_latitude = models.CharField(max_length=255)
    settlementgps_longitude = models.CharField(max_length=255)
    settlementgps_altitude = models.CharField(max_length=255)
    settlementgps_accuracy = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    lga = models.CharField(max_length=255)
    ward = models.CharField(max_length=255)
    settlementname = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    names = models.CharField(max_length=255)
    activity = models.CharField(max_length=255)
    hc_townannouncer = models.CharField(max_length=255)
    hc_opvvaccinator = models.CharField(max_length=255)
    hc_recorder_opv = models.CharField(max_length=255)
    hc_separatetally = models.CharField(max_length=255)
    hc_clinician1 = models.CharField(max_length=255)
    hc_clinician2 = models.CharField(max_length=255)
    hc_recorder_ri = models.CharField(max_length=255)
    hc_crowdcontroller = models.CharField(max_length=255)
    hc_nc_location = models.CharField(max_length=255)
    hc_appropriate_location = models.CharField(max_length=255)
    hc_stockout = models.CharField(max_length=255)
    hc_num_opv = models.CharField(max_length=255)
    hc_num_measles = models.CharField(max_length=255)
    hc_num_penta = models.CharField(max_length=255)
    hc_num_patients = models.CharField(max_length=255)
    hc_team_allowances = models.CharField(max_length=255)
    cd_attendance = models.CharField(max_length=255)
    cd_num_hh_affected = models.CharField(max_length=255)
    cd_local_leadership_present = models.CharField(max_length=255)
    cd_resolved = models.CharField(max_length=255)
    cd_hh_pending_issues = models.CharField(max_length=255)
    cd_num_vaccinated = models.CharField(max_length=255)
    cd_iec = models.CharField(max_length=255)
    cd_pro_opv_cd = models.CharField(max_length=255)
    cm_attendance = models.CharField(max_length=255)
    cm_num_husband_issues = models.CharField(max_length=255)
    cm_num_caregiver_issues = models.CharField(max_length=255)
    cm_vcm_sett = models.CharField(max_length=255)
    cm_vcm_present = models.CharField(max_length=255)
    cm_iec = models.CharField(max_length=255)
    cm_num_vaccinated = models.CharField(max_length=255)
    cm_num_positive = models.CharField(max_length=255)
    ipds_team = models.CharField(max_length=255)
    ipds_issue_reported = models.CharField(max_length=255)
    ipds_other_issue = models.CharField(max_length=255)
    ipds_num_hh = models.CharField(max_length=255)
    ipds_num_children = models.CharField(max_length=255)
    ipds_issue_resolved = models.CharField(max_length=255)
    ipds_team_allowances = models.CharField(max_length=255)
    ipds_community_leader_present = models.CharField(max_length=255)
    meta_instanceid = models.CharField(max_length=255)
    key = models.CharField(max_length=255, unique=True)
    process_status = models.ForeignKey(ProcessStatus)
    request_guid = models.CharField(max_length=255)
    created_at = models.DateTimeField(default=datetime.now())

    def __unicode__(self):
        return unicode('hello')

    class Meta:
        app_label = 'source_data'


class VWSRegister(models.Model):
    submissiondate = models.CharField(max_length=255)
    deviceid = models.CharField(max_length=255)
    simserial = models.CharField(max_length=255)
    phonenumber = models.CharField(max_length=255)
    datephonecollected = models.CharField(max_length=255)
    fname_vws = models.CharField(max_length=255)
    lname_vws = models.CharField(max_length=255)
    wardcode = models.CharField(max_length=255)
    personal_phone = models.CharField(max_length=255)
    acceptphoneresponsibility = models.CharField(max_length=255)
    meta_instanceid = models.CharField(max_length=255)
    key = models.CharField(max_length=255, unique=True)
    process_status = models.ForeignKey(ProcessStatus)
    request_guid = models.CharField(max_length=255)
    created_at = models.DateTimeField(default=datetime.now())

    def __unicode__(self):
        return unicode('hello')

    class Meta:
        app_label = 'source_data'


class HealthCamp(models.Model):
    region = models.CharField(max_length=255)
    submissiondate = models.CharField(max_length=255)
    formhub_uuid = models.CharField(max_length=255)
    phonenumber = models.CharField(max_length=255)
    userid = models.CharField(max_length=255)
    daterecorded = models.CharField(max_length=255)
    start_time = models.CharField(max_length=255)
    lga = models.CharField(max_length=255)
    ward = models.CharField(max_length=255)
    settlementname = models.CharField(max_length=255)
    names = models.CharField(max_length=255)
    agencyname = models.CharField(max_length=255)
    townannouncer = models.CharField(max_length=255)
    megaphone = models.CharField(max_length=255)
    opvvaccinator = models.CharField(max_length=255)
    recorder_opv = models.CharField(max_length=255)
    separatetally = models.CharField(max_length=255)
    clinician1 = models.CharField(max_length=255)
    clinician2 = models.CharField(max_length=255)
    recorder_ri = models.CharField(max_length=255)
    crowdcontroller = models.CharField(max_length=255)
    nc_location = models.CharField(max_length=255)
    appropriate_location = models.CharField(max_length=255)
    hc_stockout = models.CharField(max_length=255)
    num_opv = models.CharField(max_length=255)
    num_measles = models.CharField(max_length=255)
    num_penta = models.CharField(max_length=255)
    num_patients = models.CharField(max_length=255)
    hc_photo = models.CharField(max_length=255)
    settlementgps_latitude = models.CharField(max_length=255)
    settlementgps_longitude = models.CharField(max_length=255)
    settlementgps_altitude = models.CharField(max_length=255)
    settlementgps_accuracy = models.CharField(max_length=255)
    endtime = models.CharField(max_length=255)
    meta_instanceid = models.CharField(max_length=255)
    key = models.CharField(max_length=255, unique=True)
    process_status = models.ForeignKey(ProcessStatus)
    request_guid = models.CharField(max_length=255)
    created_at = models.DateTimeField(default=datetime.now())

    def __unicode__(self):
        return unicode('hello')

    class Meta:
        app_label = 'source_data'


class PracticeVCMSettCoordinates(models.Model):
    submissiondate = models.CharField(max_length=255)
    deviceid = models.CharField(max_length=255)
    simserial = models.CharField(max_length=255)
    phonenumber = models.CharField(max_length=255)
    daterecorded = models.CharField(max_length=255)
    settlementcode = models.CharField(max_length=255)
    settlementname = models.CharField(max_length=255)
    vcmname = models.CharField(max_length=255)
    vcmphone = models.CharField(max_length=255)
    settlementgps_latitude = models.CharField(max_length=255)
    settlementgps_longitude = models.CharField(max_length=255)
    settlementgps_altitude = models.CharField(max_length=255)
    settlementgps_accuracy = models.CharField(max_length=255)
    meta_instanceid = models.CharField(max_length=255)
    key = models.CharField(max_length=255, unique=True)
    process_status = models.ForeignKey(ProcessStatus)
    request_guid = models.CharField(max_length=255)
    created_at = models.DateTimeField(default=datetime.now())

    def __unicode__(self):
        return unicode('hello')

    class Meta:
        app_label = 'source_data'


class PaxListReportTraining(models.Model):
    submissiondate = models.CharField(max_length=255)
    meta_instanceid = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    nameofparticipant = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    phonenumber = models.CharField(max_length=255)
    emailaddr = models.CharField(max_length=255)
    timestamp = models.CharField(max_length=255)
    key = models.CharField(max_length=255, unique=True)
    process_status = models.ForeignKey(ProcessStatus)
    request_guid = models.CharField(max_length=255)
    created_at = models.DateTimeField(default=datetime.now())

    def __unicode__(self):
        return unicode('hello')

    class Meta:
        app_label = 'source_data'


class PracticeVCMSummary(models.Model):
    submissiondate = models.CharField(max_length=255)
    deviceid = models.CharField(max_length=255)
    simserial = models.CharField(max_length=255)
    phonenumber = models.CharField(max_length=255)
    dateofreport = models.CharField(max_length=255)
    date_implement = models.CharField(max_length=255)
    settlementcode = models.CharField(max_length=255)
    censusnewbornsf = models.CharField(max_length=255)
    censusnewbornsm = models.CharField(max_length=255)
    census2_11mof = models.CharField(max_length=255)
    census2_11mom = models.CharField(max_length=255)
    census12_59mof = models.CharField(max_length=255)
    census12_59mom = models.CharField(max_length=255)
    vaxnewbornsf = models.CharField(max_length=255)
    vaxnewbornsm = models.CharField(max_length=255)
    vax2_11mof = models.CharField(max_length=255)
    vax2_11mom = models.CharField(max_length=255)
    vax12_59mof = models.CharField(max_length=255)
    vax12_59mom = models.CharField(max_length=255)
    msd_grp_choice = models.CharField(max_length=255)
    group_msd_chd_msd_playgroundf = models.CharField(max_length=255)
    group_msd_chd_msd_playgroundm = models.CharField(max_length=255)
    group_msd_chd_msd_soceventf = models.CharField(max_length=255)
    group_msd_chd_msd_soceventm = models.CharField(max_length=255)
    group_msd_chd_msd_marketf = models.CharField(max_length=255)
    group_msd_chd_msd_marketm = models.CharField(max_length=255)
    group_msd_chd_msd_farmf = models.CharField(max_length=255)
    group_msd_chd_msd_farmm = models.CharField(max_length=255)
    group_msd_chd_msd_schoolf = models.CharField(max_length=255)
    group_msd_chd_msd_schoolm = models.CharField(max_length=255)
    group_msd_chd_msd_childsickf = models.CharField(max_length=255)
    group_msd_chd_msd_childsickm = models.CharField(max_length=255)
    group_msd_chd_msd_sideeffectsf = models.CharField(max_length=255)
    group_msd_chd_msd_sideeffectsm = models.CharField(max_length=255)
    group_msd_chd_msd_nofeltneedf = models.CharField(max_length=255)
    group_msd_chd_msd_nofeltneedm = models.CharField(max_length=255)
    group_msd_chd_msd_toomanyroundsf = models.CharField(max_length=255)
    group_msd_chd_msd_toomanyroundsm = models.CharField(max_length=255)
    group_msd_chd_msd_relbeliefsf = models.CharField(max_length=255)
    group_msd_chd_msd_relbeliefsm = models.CharField(max_length=255)
    group_msd_chd_msd_poldiffsf = models.CharField(max_length=255)
    group_msd_chd_msd_poldiffsm = models.CharField(max_length=255)
    group_msd_chd_msd_unhappywteamf = models.CharField(max_length=255)
    group_msd_chd_msd_unhappywteamm = models.CharField(max_length=255)
    group_msd_chd_msd_noplusesf = models.CharField(max_length=255)
    group_msd_chd_msd_noplusesm = models.CharField(max_length=255)
    group_msd_chd_msd_nogovtservicesf = models.CharField(max_length=255)
    group_msd_chd_msd_nogovtservicesm = models.CharField(max_length=255)
    group_msd_chd_msd_poliouncommonf = models.CharField(max_length=255)
    group_msd_chd_msd_poliouncommonm = models.CharField(max_length=255)
    group_msd_chd_msd_poliohascuref = models.CharField(max_length=255)
    group_msd_chd_msd_poliohascurem = models.CharField(max_length=255)
    group_msd_chd_msd_otherprotectionf = models.CharField(max_length=255)
    group_msd_chd_msd_otherprotectionm = models.CharField(max_length=255)
    group_msd_chd_msd_noconsentf = models.CharField(max_length=255)
    group_msd_chd_msd_noconsentm = models.CharField(max_length=255)
    group_msd_chd_msd_hhnotvisitedf = models.CharField(max_length=255)
    group_msd_chd_msd_hhnotvisitedm = models.CharField(max_length=255)
    group_msd_chd_msd_noreasonf = models.CharField(max_length=255)
    group_msd_chd_msd_noreasonm = models.CharField(max_length=255)
    group_msd_chd_msd_securityf = models.CharField(max_length=255)
    group_msd_chd_msd_securitym = models.CharField(max_length=255)
    group_msd_chd_msd_agedoutf = models.CharField(max_length=255)
    group_msd_chd_msd_agedoutm = models.CharField(max_length=255)
    group_msd_chd_msd_familymovedf = models.CharField(max_length=255)
    group_msd_chd_msd_familymovedm = models.CharField(max_length=255)
    group_msd_chd_msd_childdiedf = models.CharField(max_length=255)
    group_msd_chd_msd_childdiedm = models.CharField(max_length=255)
    spec_grp_choice = models.CharField(max_length=255)
    group_spec_events_spec_zerodose = models.CharField(max_length=255)
    group_spec_events_spec_pregnantmother = models.CharField(max_length=255)
    group_spec_events_spec_newborn = models.CharField(max_length=255)
    group_spec_events_spec_vcmattendedncer = models.CharField(max_length=255)
    group_spec_events_spec_cmamreferral = models.CharField(max_length=255)
    group_spec_events_spec_rireferral = models.CharField(max_length=255)
    group_spec_events_spec_afpcase = models.CharField(max_length=255)
    group_spec_events_spec_mslscase = models.CharField(max_length=255)
    group_spec_events_spec_otherdisease = models.CharField(max_length=255)
    group_spec_events_spec_fic = models.CharField(max_length=255)
    meta_instanceid = models.CharField(max_length=255)
    key = models.CharField(max_length=255, unique=True)
    process_status = models.ForeignKey(ProcessStatus)
    request_guid = models.CharField(max_length=255)
    created_at = models.DateTimeField(default=datetime.now())

    def __unicode__(self):
        return unicode('hello')

    class Meta:
        app_label = 'source_data'


class PracticeVCMBirthRecord(models.Model):
    submissiondate = models.CharField(max_length=255)
    deviceid = models.CharField(max_length=255)
    simserial = models.CharField(max_length=255)
    phonenumber = models.CharField(max_length=255)
    dateofreport = models.CharField(max_length=255)
    datereport = models.CharField(max_length=255)
    settlementcode = models.CharField(max_length=255)
    householdnumber = models.CharField(max_length=255)
    dob = models.CharField(max_length=255)
    nameofchild = models.CharField(max_length=255)
    vcm0dose = models.CharField(max_length=255)
    vcmrilink = models.CharField(max_length=255)
    vcmnamecattended = models.CharField(max_length=255)
    meta_instanceid = models.CharField(max_length=255)
    key = models.CharField(max_length=255, unique=True)
    process_status = models.ForeignKey(ProcessStatus)
    request_guid = models.CharField(max_length=255)
    created_at = models.DateTimeField(default=datetime.now())

    def __unicode__(self):
        return unicode('hello')

    class Meta:
        app_label = 'source_data'


class KnowThePeople(models.Model):
    submissiondate = models.CharField(max_length=255)
    meta_instanceid = models.CharField(max_length=255)
    nameofpax = models.CharField(max_length=255)
    state_country = models.CharField(max_length=255)
    dob = models.CharField(max_length=255)
    brothers = models.CharField(max_length=255)
    sisters = models.CharField(max_length=255)
    prefferedcity = models.CharField(max_length=255)
    citiesvisited = models.CharField(max_length=255)
    key = models.CharField(max_length=255, unique=True)
    process_status = models.ForeignKey(ProcessStatus)
    request_guid = models.CharField(max_length=255)
    created_at = models.DateTimeField(default=datetime.now())

    def __unicode__(self):
        return unicode('hello')

    class Meta:
        app_label = 'source_data'
