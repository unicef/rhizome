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

    master_object = models.ForeignKey(Campaign)
    source_object = models.ForeignKey(SourceCampaign,unique=True)
    mapped_by = models.ForeignKey(User)

    class Meta:
        db_table = 'campaign_map'

class DocumentDetail(models.Model):

    document = models.ForeignKey(Document)
    db_model = models.CharField(max_length=255)
    source_object_id = models.IntegerField()
    master_object_id = models.IntegerField()
    source_string = models.CharField(max_length=255)
    source_dp_count = models.IntegerField()
    master_dp_count = models.IntegerField()
    map_id = models.IntegerField()

    class Meta:
        db_table = 'document_detail'

## ODK ##

class ODKForm(models.Model):

    document = models.ForeignKey(Document,null=True)
    last_processed = models.DateTimeField(null=True)
    response_msg = models.CharField(null=True,max_length=255)
    source_datapoint_count = models.IntegerField(default=0)
    master_datapoint_count = models.IntegerField(default=0)
    form_name = models.CharField(max_length=255)

    class Meta:
        db_table = 'odk_form'

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
        db_table = 'odk_vcm_settlement'
