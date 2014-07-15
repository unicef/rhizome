from django.db import models

class Indicator(models.Model):
    name = models.CharField(max_length=55)
    description = models.CharField(max_length=255)
    is_reported = models.BooleanField(default=True)
    parent_indicator_id = models.ForeignKey("Indicator",null=True, blank=True)
    created_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return unicode(self.name)


    class Meta:
        db_table = 'indicator'

class Region(models.Model):
    full_name = models.CharField(max_length=255)
    short_name = models.CharField(max_length=55)
    description = models.CharField(max_length=255,null=True)
    parent_region_id = models.ForeignKey("Region",null=True, blank=True)
    shape_file_path  = models.CharField(max_length=255,null=True,blank=True)
    latitude = models.DecimalField(max_digits=12, decimal_places =10,null=True,blank=True)
    longitude = models.DecimalField(max_digits=13, decimal_places =10,null=True,blank=True)
    created_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return unicode(self.short_name)

    class Meta:
        db_table = 'region'


class ReportingPeriod(models.Model):
    start_date = models.DateField()
    end_date = models.DateField()
    note = models.CharField(max_length=255,null=True,blank=True)
    created_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return unicode(self.start_date.strftime('%Y-%m-%d') + ' to ' + self.end_date.strftime('%Y-%m-%d'))
        # return unicode(note)

    class Meta:
        db_table = 'reporting_period'

class DataPoint(models.Model):
    indicator = models.ForeignKey(Indicator)
    region = models.ForeignKey(Region)
    reporing_period = models.ForeignKey(ReportingPeriod,null=True, blank=True)
    value = models.DecimalField(max_digits=12, decimal_places =4)
    note = models.CharField(max_length=255,null=True,blank=True)
    created_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return unicode(self.value)

    class Meta:
        db_table = 'datapoint'

## TO DO ##
# -> Audit Table


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