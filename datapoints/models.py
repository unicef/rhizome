from django.db import models
from simple_history.models import HistoricalRecords

class Indicator(models.Model):
    name = models.CharField(max_length=55)
    description = models.CharField(max_length=255)
    is_reported = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now=True)
    #
    history = HistoricalRecords()

    def __unicode__(self):
        return unicode(self.name)


    class Meta:
        db_table = 'indicator'

class Region(models.Model):
    full_name = models.CharField(max_length=255)
    short_name = models.CharField(max_length=55)
    description = models.CharField(max_length=255,null=True)
    shape_file_path  = models.CharField(max_length=255,null=True,blank=True)
    latitude = models.DecimalField(max_digits=12, decimal_places =10,null=True,blank=True)
    longitude = models.DecimalField(max_digits=13, decimal_places =10,null=True,blank=True)
    created_at = models.DateTimeField(auto_now=True)
    #
    history = HistoricalRecords()


    def __unicode__(self):
        return unicode(self.full_name)

    class Meta:
        db_table = 'region'


class ReportingPeriod(models.Model):
    start_date = models.DateField()
    end_date = models.DateField()
    note = models.CharField(max_length=255,null=True,blank=True)
    created_at = models.DateTimeField(auto_now=True)
    #
    history = HistoricalRecords()


    def __unicode__(self):
        return unicode(self.start_date.strftime('%Y-%m-%d') + ' to ' + self.end_date.strftime('%Y-%m-%d'))

    class Meta:
        db_table = 'reporting_period'

class DataPoint(models.Model):
    indicator = models.ForeignKey(Indicator)
    region = models.ForeignKey(Region)
    reporting_period = models.ForeignKey(ReportingPeriod)
    value = models.DecimalField(max_digits=12, decimal_places =4)
    note = models.CharField(max_length=255,null=True,blank=True)
    created_at = models.DateTimeField(auto_now=True)
    #
    history = HistoricalRecords()

    def __unicode__(self):
        return unicode(self.value)

    class Meta:
        db_table = 'datapoint'

class IndicatorRelationshipType(models.Model):
    display_name = models.CharField(max_length=55)
    inverse_display_name = models.CharField(max_length=55)
    description = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now=True)
    #
    history = HistoricalRecords()

    def __unicode__(self):
        return unicode(self.display_name)

    class Meta:
        db_table = 'indicator_relationship_type'


class IndicatorRelationship(models.Model):
    indicator_0 = models.ForeignKey(Indicator, related_name='ind_0')
    indicator_1 = models.ForeignKey(Indicator, related_name='ind_1')
    indicator_relationship_type = models.ForeignKey(IndicatorRelationshipType)
    note = models.CharField(max_length=255,null=True,blank=True)
    created_at = models.DateTimeField(auto_now=True)
    # AUDIT #
    history = HistoricalRecords()


    def __unicode__(self):
        return unicode(self.indicator_0 + '>' + self.indicator_relationship_type + '>' + self.indicator_1)

    class Meta:
        db_table = 'indicator_relationship'


class RegionRelationshipType(models.Model):
    display_name = models.CharField(max_length=55)
    inverse_display_name = models.CharField(max_length=55)
    description = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now=True)
    # AUDIT #
    history = HistoricalRecords()


    def __unicode__(self):
        return unicode(self.display_name)

    class Meta:
        db_table = 'region_relationship_type'


class RegionRelationship(models.Model):
    region_0 = models.ForeignKey(Region, related_name='ind_0')
    region_1 = models.ForeignKey(Region, related_name='ind_1')
    region_relationship_type = models.ForeignKey(RegionRelationshipType)
    note = models.CharField(max_length=255,null=True,blank=True)
    created_at = models.DateTimeField(auto_now=True)
    # AUDIT #
    history = HistoricalRecords()


    def __unicode__(self):
        return unicode(self.region_0 + '>' + self.region_relationship_type + '>' + self.region_0)

    class Meta:
        db_table = 'region_relationship'



### DataPoint Extras ###
    # status_id
    # geography # change to geo_id
    # source_id
    # time_period 
    # updated_by_user_id
    # group_id 


### Indicator Extras ###    
    # time_interval 
    # evaluation_levels
    # aggregation_details