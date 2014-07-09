from django.db import models

class DataPointIndicator(models.Model):
    name = models.CharField(max_length=55)
    description = models.CharField(max_length=255)
    is_reported = models.BooleanField(default=True)
    parent_indicator_id = models.IntegerField(null=True)

    class Meta:
        db_table = 'datapoint_indicator'


class DataPoint(models.Model):
    indicator = models.ForeignKey(DataPointIndicator)
    value = models.IntegerField(default=0)
    note = models.CharField(max_length=255)

    class Meta:
        db_table = 'datapoint'

class Region(models.Model):
    full_name = models.CharField(max_length=255)
    short_name = models.CharField(max_length=55)
    description = models.CharField(max_length=255)
    parent_region_id = models.IntegerField(null=True)
    shape_file_path  = models.CharField(max_length=255)
    latitude = models.DecimalField(max_digits=12, decimal_places =10)
    longitude = models.DecimalField(max_digits=13, decimal_places =10)

    class Meta:
        db_table = 'region'

## TO DO ##
# -> Time Stamps
# -> Audit Table
# -> Self Referential FKs (parent_region_id, parent_indicator_id)


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