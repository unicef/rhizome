from django.db import models

class VCM_Birth_Record(models.Model):

    SubmissionDate = models.DateTimeField()
    deviceid = models.IntegerField()
    simserial = models.IntegerField()
    phonenumber = models.IntegerField()
    DateOfReport = models.DateField()
    DateReport = models.DateField()
    SettlementCode = models.IntegerField()
    HouseHoldNumber = models.IntegerField()
    DOB = models.DateField()
    NameOfChild  = models.CharField(max_length=100)
    VCM0Dose  = models.CharField(max_length=3)
    VCMRILink = models.CharField(max_length=3)
    VCMNameCAttended = models.CharField(max_length=3)
    meta_instanceID = models.CharField(max_length=55,unique=True)
    KEY = models.CharField(max_length=55,unique=True)

    def __unicode__(self):
        return unicode(self.full_name)
