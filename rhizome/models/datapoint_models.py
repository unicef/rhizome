from django.db import models
from simple_history.models import HistoricalRecords

from rhizome.models.indicator_models import Indicator
from rhizome.models.location_models import Location
from rhizome.models.campaign_models import Campaign
from rhizome.models.document_models import Document, CacheJob

class DataPointComputed(models.Model):

    value = models.FloatField()
    cache_job = models.ForeignKey(CacheJob, default=-1)
    indicator = models.ForeignKey(Indicator)
    location = models.ForeignKey(Location)
    campaign = models.ForeignKey(Campaign)
    document = models.ForeignKey(Document)

    class Meta:
        db_table = 'datapoint_with_computed'
        unique_together = ('location', 'campaign', 'indicator')

class AggDataPoint(models.Model):

    indicator = models.ForeignKey(Indicator)
    location = models.ForeignKey(Location)
    campaign = models.ForeignKey(Campaign)
    value = models.FloatField()
    cache_job = models.ForeignKey(CacheJob, default=-1)

    class Meta:
        db_table = 'agg_datapoint'
        unique_together = ('location', 'campaign', 'indicator')
