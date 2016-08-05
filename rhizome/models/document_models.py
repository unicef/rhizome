import hashlib
import random
from django.db import models
from django.contrib.auth.models import User

from jsonfield import JSONField

class Document(models.Model):

    docfile = models.FileField(upload_to='documents/%Y/%m/%d', null=True)
    file_type = models.CharField(max_length=10)
    doc_title = models.TextField(unique=True)
    file_header = JSONField(null=True)
    created_by = models.ForeignKey(User, null=True)
    guid = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'source_doc'
        ordering = ('-created_at',)

    def save(self, *args, **kwargs):
        if not self.guid:
            self.guid = hashlib.sha1(str(random.random())).hexdigest()

        super(Document, self).save(*args, **kwargs)
