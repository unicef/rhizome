from django.db import models
from simple_history.models import HistoricalRecords
from autoslug import AutoSlugField

class Indicator(models.Model):

    name = models.CharField(max_length=55,unique=True)
    description = models.CharField(max_length=255)
    is_reported = models.BooleanField(default=True)
    slug = AutoSlugField(populate_from='name',unique=True,max_length=55)
    created_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return unicode(self.name)

    class Meta:
        db_table = 'indicator'

class Office(models.Model):

    name = models.CharField(max_length=55)
    created_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return unicode(self.name)

    class Meta:
        db_table = 'office'

        permissions = (
            ('view_office', 'View office'),
        )

class Region(models.Model):

    full_name = models.CharField(max_length=55,unique=True)
    office = models.ForeignKey(Office)
    shape_file_path  = models.CharField(max_length=255,null=True,blank=True)
    latitude = models.DecimalField(max_digits=12, decimal_places =10,null=True,blank=True)
    longitude = models.DecimalField(max_digits=13, decimal_places =10,null=True,blank=True)
    slug = AutoSlugField(populate_from='full_name',max_length=55)
    created_at = models.DateTimeField(auto_now=True)


    def __unicode__(self):
        return unicode(self.full_name)

    class Meta:
        db_table = 'region'

        permissions = (
            ('view_region', 'View region'),
        )

class Campaign(models.Model):

    name = models.CharField(max_length=255)
    office = models.ForeignKey(Office)
    start_date = models.DateField()
    end_date = models.DateField()
    slug = AutoSlugField(populate_from='get_full_name')
    created_at = models.DateTimeField(auto_now=True)


    def __unicode__(self):
        return unicode(self.start_date.strftime('%Y-%m-%d') + ' to ' +
            self.end_date.strftime('%Y-%m-%d'))

    def get_full_name(self):
        full_name = self.office.name + '-' + self.__unicode__()
        return full_name

    class Meta:
        db_table = 'campaign'

class DataPoint(models.Model):

    indicator = models.ForeignKey(Indicator)
    region = models.ForeignKey(Region)
    campaign = models.ForeignKey(Campaign)
    value = models.DecimalField(max_digits=12, decimal_places =4)
    note = models.CharField(max_length=255,null=True,blank=True)
    changed_by = models.ForeignKey('auth.User')
    created_at = models.DateTimeField(auto_now=True)
    #
    history = HistoricalRecords()

    class Meta:
        db_table = 'datapoint'
        unique_together = ('indicator','region','campaign')

        permissions = (
            ('view_datapoint', 'View datapoint'),
        )


class RegionRelationshipType(models.Model):

    display_name = models.CharField(max_length=55)
    inverse_display_name = models.CharField(max_length=55)
    description = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now=True)


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

    def __unicode__(self):
        return unicode(self.region_0 + '>' + self.region_relationship_type + '>' + self.region_0)

    class Meta:
        db_table = 'region_relationship'


class IndicatorPct(models.Model):

    indicator_part = models.ForeignKey(Indicator,related_name = 'ind_part')
    indicator_whole  = models.ForeignKey(Indicator,related_name = 'ind_whole')
    indicator_pct_display_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return unicode(indicator_pct_display_name)

    class Meta:
        db_table = 'indicator_pct'

class Document(models.Model):

    docfile = models.FileField(upload_to='documents/%Y/%m/%d')

    class Meta:
        db_table = 'document'


class AggregationType(models.Model):

    name = models.CharField(max_length=255,unique=True)
    fn_lookup = models.CharField(max_length=255,unique=True)
    display_name_w_sub = models.CharField(max_length=255,unique=True)
    created_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'aggregation_type'


class AggregationExpectedData(models.Model):

    aggregation_type = models.ForeignKey(AggregationType)
    content_type = models.CharField(max_length=20)
    param_type = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'aggregation_expected_data'
