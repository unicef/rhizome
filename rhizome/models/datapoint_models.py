from django.db import models
from simple_history.models import HistoricalRecords

from rhizome.models.indicator_models import Indicator
from rhizome.models.location_models import Location
from rhizome.models.campaign_models import Campaign
import rhizome.models.document_models as dm

class CacheJob(models.Model):
    '''
    A table that shows the start/end time of each cache job, as well as the
    response message of the job itself.  This allows a DBA to track what is
    happening with our cache jobs and how long they are taking.
    '''

    date_attempted = models.DateTimeField(auto_now=True)
    date_completed = models.DateTimeField(null=True)
    is_error = models.BooleanField()
    response_msg = models.CharField(max_length=255)

    class Meta:
        db_table = 'cache_job'
        ordering = ('-date_attempted',)


class DataPoint(models.Model):
    '''
    The core table of the application.  This is where the raw data is stored
    and brought together from data entry, ODK and csv upload.

    Note that this table does not store the aggregated or calculated data, only
    the raw data that we get from the source.

    The source_submission shows the original source of the data in the
    source_submission.  The source_submission is -1 in the case of data
    entry.

    The cache_job_id column allows us to find out when and why a particular
    datapoint was refreshed.  New datapoints have a cache_job_id = -1 which
    tells the system that it needs to be refreshed.
    '''

    indicator = models.ForeignKey(Indicator)
    location = models.ForeignKey(Location)
    campaign = models.ForeignKey(Campaign, null=True)
    data_date = models.DateTimeField(null=True)
    value = models.FloatField(null=True)
    created_at = models.DateTimeField(auto_now=True)
    source_submission = models.ForeignKey(dm.SourceSubmission)
    cache_job = models.ForeignKey(CacheJob, default=-1)
    unique_index = models.CharField(max_length=255, unique=True, default=-1)

    def get_val(self):
        return self.value

    class Meta:
        db_table = 'datapoint'


class DocDataPoint(models.Model):
    '''
    For Validation of upload rhizome.
    '''

    document = models.ForeignKey(dm.Document)  # redundant
    indicator = models.ForeignKey(Indicator)
    location = models.ForeignKey(Location)
    campaign = models.ForeignKey(Campaign, null=True)
    data_date = models.DateTimeField(null=True)
    value = models.FloatField(null=True)
    source_submission = models.ForeignKey(dm.SourceSubmission)
    agg_on_location = models.BooleanField()

    class Meta:
        db_table = 'doc_datapoint'


class DataPointEntry(DataPoint):
    """Proxy subclass of DataPoint, for use only in API
    methods used by the manual data entry form. This model
    stores records of all changes in a separate DB table.
    """

    history = HistoricalRecords()

    class Meta:
        proxy = True


class DataPointComputed(models.Model):

    value = models.FloatField()
    cache_job = models.ForeignKey(CacheJob, default=-1)
    indicator = models.ForeignKey(Indicator)
    location = models.ForeignKey(Location)
    campaign = models.ForeignKey(Campaign)
    document = models.ForeignKey(dm.Document)

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
