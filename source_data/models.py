import hashlib
import random

from datetime import datetime
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

from jsonfield import JSONField

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

        super(Document, self).save(*args, **kwargs)


class SourceObjectMap(models.Model):
    # FIXME -> need to check what would be foreign keys
    # so region_maps / campaign_maps are valid

    master_object_id = models.IntegerField()  # need to think about to FK this.
    master_object_name = models.CharField(max_length=255, null=True)
    source_object_code = models.CharField(max_length=255)
    content_type = models.CharField(max_length=20)
    mapped_by = models.ForeignKey(User, null=True)
    ## mapped_by is only null so that i can initialize the database with ##
    ## mappings without a user_id created ##

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
    data_date = models.DateTimeField()
    location_code = models.CharField(max_length=1000)
    location_display = models.CharField(max_length=1000)
    submission_json = JSONField()
    created_at = models.DateTimeField(auto_now=True)
    process_status = models.CharField(max_length=25)  # should be a FK

    class Meta:
        db_table = 'source_submission'
        unique_together = (('document', 'instance_guid'))

    def get_location_id(self):

        try:
            loc_id = SourceObjectMap.objects.get(content_type = 'location',\
                source_object_code = self.location_code).master_object_id
        except ObjectDoesNotExist:
            loc_id = None

        return loc_id
