from django.contrib import admin
from datapoints.models import DataPoint, DataPointIndicator, Region

admin.site.register(DataPoint)
admin.site.register(DataPointIndicator)
admin.site.register(Region)

# Register your models here.
