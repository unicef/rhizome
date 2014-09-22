from django.db import models
from datapoints.models import Source, Indicator, Region, Campaign
from django.contrib.auth.models import User

class SourceRegion(models.Model):

    region_string = models.CharField(max_length=255)
    source = models.ForeignKey(Source)
    source_guid = models.CharField(max_length=255)

    def __unicode__(self):
        return self.region_string

class SourceIndicator(models.Model):

    indicator_string = models.CharField(max_length=255)
    source = models.ForeignKey(Source)
    source_guid = models.CharField(max_length=255)

    def __unicode__(self):
        return self.indicator_string


class SourceCampaign(models.Model):

    campaign_string = models.CharField(max_length=255)
    source = models.ForeignKey(Source)
    source_guid = models.CharField(max_length=255)

    def __unicode__(self):
        return self.campaign_string


class RegionMap(models.Model):

    master_region = models.ForeignKey(Indicator)
    source_region = models.ForeignKey(SourceIndicator)
    mapped_by = models.ForeignKey(User)


class IndicatorMap(models.Model):

    master_indicator = models.ForeignKey(Indicator)
    source_indicator = models.ForeignKey(SourceIndicator)
    mapped_by = models.ForeignKey(User)


class CampaignMap(models.Model):

    master_campaign = models.ForeignKey(Indicator)
    source_campaign = models.ForeignKey(SourceIndicator)
    mapped_by = models.ForeignKey(User)
