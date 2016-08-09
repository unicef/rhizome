from django.db import models
from jsonfield import JSONField


class Indicator(models.Model):
    '''
    The type of data that we are tracing, for instance
     - Number of children missed due to religious locations
     - Number of vaccinators paid on time
     - Number of iVDPV cases
     - Percentage of children missed due to religious locations.

    Note that both calculated and raw indicators are stored in this table.  For
    more information on how indicicators are used to calculated data for more
    indicators take a look at the CalculatedIndicatorComponent model.
    '''

    short_name = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255, unique=True)
    description = models.CharField(max_length=255)
    is_reported = models.BooleanField(default=True)
    data_format = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now=True)
    bound_json = JSONField(default=[])
    tag_json = JSONField(default=[])
    good_bound = models.FloatField(null=True)
    bad_bound = models.FloatField(null=True)
    source_name = models.CharField(max_length=55)  # to do: make this a FK
    resource_name = models.CharField(max_length=10)  # data_date or campaign

    def __unicode__(self):
        return unicode(self.name)

    class Meta:
        db_table = 'indicator'
        ordering = ('name',)


class CalculatedIndicatorComponent(models.Model):
    '''
    The indicator is for example "pct missed due to refusal," the component
    "total missed" and calculation is "denominator"

    A dba can create new calculations by inserting rows here.  The
    cache_refresh job that happens every minute will take these new indicator
    definitions and use these values to calucate data for the new calculated
    lintindicators.

    Notice however that calculations are multi layered, for instance certain
    percentage calculations, use an indicator that is calculated from the sum
    of a set of other indicators as it's denominator.  This means, that the
    order in which we calculated datapoints matters.  For more on how this
    works check out the calc_datapoint() method.
    '''

    indicator = models.ForeignKey(Indicator, related_name='indicator_master')
    indicator_component = models.ForeignKey(
        Indicator, related_name='indicator_component')
    calculation = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return unicode(self.indicator.name)

    class Meta:
        db_table = 'calculated_indicator_component'


class IndicatorBound(models.Model):
    '''
    If a Low / High reporesents an error, or a particular grouping of values
    i.e. (good, ok, bad) we have how ever many rows for an indicator as their
    are groupings for that indicator's values.
    '''

    indicator = models.ForeignKey(Indicator)
    mn_val = models.FloatField(null=True)
    mx_val = models.FloatField(null=True)
    bound_name = models.CharField(max_length=255)
    direction = models.IntegerField(default=1)

    def __unicode__(self):
        return unicode(self.bound_name)

    class Meta:
        db_table = 'indicator_bound'


class IndicatorTag(models.Model):
    '''
    The list of tags that can be associated to an indicator.  For instance:
        - ODK indicators
        - WHO independent monitoring
        - Management Dashbaord Indicators

    These are stored in a heirarchy so we can build a tree on the indicator
    drop down which gives the user a nicer, more organized breakdown of the
    indicators available to the system.
    '''

    tag_name = models.CharField(max_length=255)
    parent_tag = models.ForeignKey("self", null=True)

    def __unicode__(self):
        return unicode(self.tag_name)

    class Meta:
        db_table = 'indicator_tag'

class IndicatorToTag(models.Model):
    '''
    Tagging an indicator. One indicator can have many tags.
    '''

    indicator = models.ForeignKey(Indicator)
    indicator_tag = models.ForeignKey(IndicatorTag)

    class Meta:
        db_table = 'indicator_to_tag'
        unique_together = ('indicator', 'indicator_tag')
        ordering = ('-id',)
