import hashlib
import random
import json

from datetime import datetime
from django.db import models
from django.contrib.auth.models import User

from datapoints.models import Indicator, Location, ResultStructure
from jsonfield import JSONField

    ###################
    ####### ETL #######
    ###################

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
    doc_title = models.TextField(unique=True)
    file_header = JSONField(null=True)
    created_by = models.ForeignKey(User)
    guid = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created_at',)

    def save(self, *args, **kwargs):
        if not self.guid:
            self.guid = hashlib.sha1(str(random.random())).hexdigest()

        if not self.file_header and self.docfile:
            for i,(line) in enumerate(self.docfile):

                if i == 0:
                    header_data = line.split("\r")[0]

            self.file_header = header_data
            print self.file_header

        super(Document, self).save(*args, **kwargs)


class SourceObjectMap(models.Model):
    # FIXME -> need to check what would be foreign keys
    # so regoin_maps / result_structure_maps are vlide

    master_object_id = models.IntegerField() ## need to think about to FK this.
    master_object_name = models.CharField(max_length=255,null=True)
    source_object_code = models.CharField(max_length=255)
    content_type = models.CharField(max_length=10)
    mapped_by = models.ForeignKey(User)

    class Meta:
        db_table = 'source_object_map'
        unique_together = (('content_type','source_object_code'))

class DocumentSourceObjectMap(models.Model):

    document = models.ForeignKey(Document)
    source_object_map = models.ForeignKey(SourceObjectMap)

    class Meta:

        unique_together = (('document','source_object_map'))
        db_table = 'document_to_source_object_map'

class DocDetailType(models.Model):
    '''
    '''
    name = models.CharField(max_length=255,unique=True)

    class Meta:
        db_table = 'document_detail_type'


class DocumentDetail(models.Model):
    '''
    '''

    document =  models.ForeignKey(Document)
    doc_detail_type = models.ForeignKey(DocDetailType)
    doc_detail_value = models.CharField(max_length=255)

    class Meta:
        db_table = 'document_detail'
        unique_together = (('document','doc_detail_type'))


class SourceSubmission(models.Model):

    document = models.ForeignKey(Document)
    instance_guid = models.CharField(max_length=255)
    row_number = models.IntegerField()
    submission_json = JSONField()
    created_at = models.DateTimeField(auto_now=True)
    process_status = models.CharField(max_length=25)

    class Meta:
        db_table = 'source_submission'
        unique_together = (('document','instance_guid'))

class SourceSubmissionDetail(models.Model):
    '''
    '''

    document = models.ForeignKey(Document)
    source_submission = models.OneToOneField(SourceSubmission)
    username_code = models.CharField(max_length=1000)
    result_structure_code = models.CharField(max_length=1000)
    location_code = models.CharField(max_length=1000)
    location_display = models.CharField(max_length=1000)
    img_location = models.CharField(max_length=1000)
    raw_data_proxy = models.CharField(max_length=1) ## hack so the admin metadata call works
    location = models.ForeignKey('datapoints.location', null=True)
    result_structure = models.ForeignKey('datapoints.resultstructure', null=True)

    class Meta:
        db_table = 'source_submission_detail'
