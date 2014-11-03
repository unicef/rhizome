from django.db import models
from autoslug import AutoSlugField
from simple_history.models import HistoricalRecords


class Source(models.Model):
    source_name = models.CharField(max_length=55,unique=True)
    source_description = models.CharField(max_length=255,unique=True)

    def __unicode__(self):
        return unicode(self.source_name)

    class Meta:
        db_table = 'source'

class Indicator(models.Model):

    short_name = models.CharField(max_length=55,unique=False) # FIX UNIQUE HERE!
    name = models.CharField(max_length=255,unique=True)
    description = models.CharField(max_length=255)
    is_reported = models.BooleanField(default=True)
    slug = AutoSlugField(populate_from='name',unique=True,max_length=255)
    created_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return unicode(self.name)

    class Meta:
        db_table = 'indicator'
        ordering = ('name',)

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

    name = models.CharField(max_length=55,unique=True)
    region_code = models.CharField(max_length=10,unique=True)
    region_type = models.CharField(max_length=55)
    office = models.ForeignKey(Office)
    shape_file_path  = models.CharField(max_length=255,null=True,blank=True)
    latitude = models.DecimalField(max_digits=12, decimal_places =10,null=True,blank=True)
    longitude = models.DecimalField(max_digits=13, decimal_places =10,null=True,blank=True)
    slug = AutoSlugField(populate_from='name',max_length=55)
    created_at = models.DateTimeField(auto_now=True)
    source = models.ForeignKey(Source)
    source_guid = models.CharField(max_length=255)
    is_high_risk = models.BooleanField(default=False)

    def __unicode__(self):
        return unicode(self.name)



    class Meta:
        db_table = 'region'

        permissions = (
            ('view_region', 'View region'),
        )

        unique_together = ('source','source_guid')

        ordering = ('name',)



class Campaign(models.Model):

    name = models.CharField(max_length=255)
    office = models.ForeignKey(Office)
    start_date = models.DateField(unique=True)
    end_date = models.DateField(unique=True)
    slug = AutoSlugField(populate_from='get_full_name')
    created_at = models.DateTimeField(auto_now=True)


    def __unicode__(self):
        return unicode(self.name)


    def get_full_name(self):
        full_name = self.office.name + '-' + self.__unicode__()
        return full_name

    class Meta:
        db_table = 'campaign'
        ordering = ('-start_date',)

class DataPoint(models.Model):

    indicator = models.ForeignKey(Indicator)
    region = models.ForeignKey(Region)
    campaign = models.ForeignKey(Campaign)
    value = models.DecimalField(max_digits=12, decimal_places =4)
    note = models.CharField(max_length=255,null=True,blank=True)
    changed_by = models.ForeignKey('auth.User')
    created_at = models.DateTimeField(auto_now=True)
    source_datapoint = models.ForeignKey('source_data.SourceDataPoint')

    # history = HistoricalRecords()

    def get_val(self):

        return self.value


    class Meta:
        db_table = 'datapoint'
        unique_together = ('indicator','region','campaign')

        permissions = (
            ('view_datapoint', 'View datapoint'),
        )

class Responsibility(models.Model):

    user = models.ForeignKey('auth.User')
    indicator = models.ForeignKey(Indicator)
    region = models.ForeignKey(Region)

    class Meta:
        db_table = 'responsibility'
        ordering = ('indicator',)
        unique_together = ('user','indicator','region')



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


    class Meta:
        db_table = 'region_relationship'


class AggregationType(models.Model):

    name = models.CharField(max_length=255,unique=True)
    slug = models.CharField(max_length=255,unique=True)
    display_name_w_sub = models.CharField(max_length=255,unique=True)
    created_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return unicode(self.name)

    class Meta:
        db_table = 'aggregation_type'


class AggregationExpectedData(models.Model):

    aggregation_type = models.ForeignKey(AggregationType)
    content_type = models.CharField(max_length=20)
    param_type = models.CharField(max_length=20)
    slug = AutoSlugField(populate_from=('aggregation_type','content_type'),max_length=55)
    created_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'aggregation_expected_data'
