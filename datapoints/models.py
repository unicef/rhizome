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