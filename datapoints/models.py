from django.db import models

class DataPointIndicator(models.Model):
    name = models.CharField(max_length=55)
    description = models.CharField(max_length=255)
    is_reported = models.BooleanField(default=True)
    parent_indicator_id = models.ForeignKey("DataPointIndicator",null=True)
    created_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = 'datapoint_indicator'

class Region(models.Model):
    full_name = models.CharField(max_length=255)
    short_name = models.CharField(max_length=55)
    description = models.CharField(max_length=255,null=True)
    parent_region_id = models.ForeignKey("Region",null=True)
    shape_file_path  = models.CharField(max_length=255,null=True)
    latitude = models.DecimalField(max_digits=12, decimal_places =10,null=True)
    longitude = models.DecimalField(max_digits=13, decimal_places =10,null=True)
    created_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.short_name

    class Meta:
        db_table = 'region'

class DataPoint(models.Model):
    indicator = models.ForeignKey(DataPointIndicator)
    region = models.ForeignKey(Region)
    value = models.IntegerField(default=0)
    note = models.CharField(max_length=255,null=True)
    created_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.value

    class Meta:
        db_table = 'datapoint'


## TO DO ##
# -> Audit Table


### DataPoiint Extras ###
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