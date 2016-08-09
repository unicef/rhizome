from django.db import models

from rhizome.models.location_models import Location
from rhizome.models.indicator_models import Indicator
from rhizome.models.campaign_models import Campaign
from rhizome.models.document_models import Document, SourceSubmission


class DocDataPoint(models.Model):
    '''
    For Validation of upload rhizome.
    '''

    document = models.ForeignKey(Document)  # redundant ( see source submission )
    indicator = models.ForeignKey(Indicator)
    location = models.ForeignKey(Location)
    campaign = models.ForeignKey(Campaign, null=True)
    data_date = models.DateTimeField(null=True)
    value = models.FloatField(null=True)
    source_submission = models.ForeignKey(SourceSubmission)
    agg_on_location = models.BooleanField()

    class Meta:
        db_table = 'doc_datapoint'


class DataPoint(models.Model):
    '''
    The core table of the application.  This is where the raw data is stored
    and brought together from data entry, ODK and csv upload.

    Note that this table does not store the aggregated or calculated data, only
    the raw data that we get from the source.

    The source_submission shows the original source of the data in the
    source_submission.  The source_submission is -1 in the case of data
    entry.

    '''

    indicator = models.ForeignKey(Indicator)
    location = models.ForeignKey(Location)
    campaign = models.ForeignKey(Campaign, null=True)
    data_date = models.DateTimeField(null=True)
    value = models.FloatField(null=True)
    created_at = models.DateTimeField(auto_now=True)
    source_submission = models.ForeignKey(SourceSubmission)
    unique_index = models.CharField(max_length=255, unique=True, default=-1)

    def get_val(self):
        return self.value

    class Meta:
        db_table = 'datapoint'
