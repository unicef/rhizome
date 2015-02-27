from django.contrib import admin
from datapoints.models import DataPoint, Indicator, Region

admin.site.register(DataPoint)
admin.site.register(Indicator)
admin.site.register(Region)

