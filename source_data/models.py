import hashlib
import random

from datetime import datetime
from django.db import models
from django.contrib.auth.models import User

from jsonfield import JSONField

# ##################
# ###### ETL #######
# ##################


class EtlJob(models.Model):

    date_attempted = models.DateTimeField(auto_now=True)
    date_completed = models.DateTimeField(null=True)
    task_name = models.CharField(max_length=55)
    status = models.CharField(max_length=10)
    guid = models.CharField(primary_key=True, max_length=40)
    cron_guid = models.CharField(max_length=40)
    error_msg = models.TextField(null=True)
    success_msg = models.CharField(max_length=255)

    class Meta:
        db_table = 'etl_job'
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
        db_table = 'process_status'

# #########################
# ###### CSV UPLOAD #######
# #########################


class Document(models.Model):

    docfile = models.FileField(upload_to='documents/%Y/%m/%d', null=True)
    doc_title = models.TextField(unique=True)
    file_header = JSONField(null=True)
    created_by = models.ForeignKey(User)
    guid = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'source_doc'
        ordering = ('-created_at',)

    def save(self, *args, **kwargs):
        if not self.guid:
            self.guid = hashlib.sha1(str(random.random())).hexdigest()

        if not self.file_header and self.docfile:
            for i, (line) in enumerate(self.docfile):

                if i == 0:
                    header_data = line.split("\r")[0]

            self.file_header = header_data

        super(Document, self).save(*args, **kwargs)


class SourceObjectMap(models.Model):
    # FIXME -> need to check what would be foreign keys
    # so regoin_maps / campaign_maps are vlide

    master_object_id = models.IntegerField()  # need to think about to FK this.
    master_object_name = models.CharField(max_length=255, null=True)
    source_object_code = models.CharField(max_length=255)
    content_type = models.CharField(max_length=20)
    mapped_by = models.ForeignKey(User)

    class Meta:
        db_table = 'source_object_map'
        unique_together = (('content_type', 'source_object_code'))


class DocumentSourceObjectMap(models.Model):

    document = models.ForeignKey(Document)
    source_object_map = models.ForeignKey(SourceObjectMap)

    class Meta:

        unique_together = (('document', 'source_object_map'))
        db_table = 'doc_object_map'


class DocDetailType(models.Model):
    '''
    '''
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        db_table = 'doc_detail_type'


class DocumentDetail(models.Model):
    '''
    '''

    document = models.ForeignKey(Document)
    doc_detail_type = models.ForeignKey(DocDetailType)
    doc_detail_value = models.CharField(max_length=255)

    class Meta:
        db_table = 'doc_detail'
        unique_together = (('document', 'doc_detail_type'))


class SourceSubmission(models.Model):

    document = models.ForeignKey(Document)
    instance_guid = models.CharField(max_length=255)
    row_number = models.IntegerField()
    data_date = models.DateTimeField(null=True)
    location_code = models.CharField(max_length=1000)
    campaign_code = models.CharField(max_length=1000)
    location_display = models.CharField(max_length=1000)
    submission_json = JSONField()
    created_at = models.DateTimeField(auto_now=True)
    process_status = models.CharField(max_length=25)  # should be a FK

    class Meta:
        db_table = 'source_submission'
        unique_together = (('document', 'instance_guid'))

    def get_location_id(self):

        try:
            l_id = SourceObjectMap.objects.get(content_type = 'location',\
                source_object_code = self.location_code).master_object_id
        except ObjectDoesNotExist:
            l_id = None

        return l_id

    def get_campaign_id(self):

        try:
            c_id = SourceObjectMap.objects.get(content_type = 'campaign',\
                source_object_code = self.campaign_code).master_object_id
        except ObjectDoesNotExist:
            c_id = None

        return c_id
