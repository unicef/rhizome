from django.db import models

class VCMBirthRecord(models.Model):
    # THIS IS WRONG it should be VCMBirthRecord

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
    KEY = models.CharField(max_length=255)

    def __unicode__(self):
        return unicode(self.full_name)

    class Meta:
        app_label = 'odk_source'
