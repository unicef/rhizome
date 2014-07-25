from tastypie.resources import ModelResource
from datapoints.models import *
from tastypie.authorization import Authorization
from tastypie import fields

class RegionResource(ModelResource):

    class Meta:
        queryset = Region.objects.all()
        resource_name = 'region'
        authorization = Authorization()

class IndicatorResource(ModelResource):

    class Meta:
        queryset = Indicator.objects.all()
        resource_name = 'indicator'
        authorization = Authorization()

class DataPointResource(ModelResource):
    region = fields.ForeignKey(RegionResource, 'region')
    indicator = fields.ForeignKey(IndicatorResource, 'indicator')

    class Meta:
        queryset = DataPoint.objects.all()
        resource_name = 'datapoint'
        authorization = Authorization()
