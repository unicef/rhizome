from tastypie.resources import ModelResource, ALL
from datapoints.models import *
from tastypie.authorization import Authorization
from tastypie.authentication import ApiKeyAuthentication
from tastypie import fields
from django.utils.decorators import method_decorator
from stronghold.decorators import public


class ApiResource(ModelResource):
    '''
    This is the top level class all other Resource Classes inherit from this.
    The API Key authentication is defined here and thus is required by all
    other resources.  This class enherits fro the Tastyppie "ModelResource"

    See Here: http://django-tastypie.readthedocs.org/en/latest/resources.html?highlight=modelresource
    '''

    class Meta:
        authentication = ApiKeyAuthentication()
        authorization = Authorization()

    @method_decorator(public)
    def dispatch(self, *args, **kwargs):
        return super(ApiResource, self).dispatch(*args, **kwargs)


class RegionResource(ApiResource):
    '''Region Resource'''

    class Meta(ApiResource.Meta):
        queryset = Region.objects.all()
        resource_name = 'region'

class IndicatorResource(ApiResource):
    '''Indicator Resource'''

    class Meta(ApiResource.Meta):
        queryset = Indicator.objects.all()
        resource_name = 'indicator'

class CampaignResource(ApiResource):
    '''Campaign Resource'''


    class Meta(ApiResource.Meta):
        queryset = Campaign.objects.all()
        resource_name = 'campaign'

class DataPointResource(ApiResource):
    '''Datapoint Resource'''

    region = fields.ForeignKey(RegionResource, 'region')
    indicator = fields.ForeignKey(IndicatorResource, 'indicator')
    campaign = fields.ForeignKey(CampaignResource, 'campaign')

    class Meta(ApiResource.Meta):
        queryset = DataPoint.objects.all()
        resource_name = 'datapoint'
        excludes = ['note']


class OfficeResource(ApiResource):
    '''Office Resource'''


    class Meta(ApiResource.Meta):
        queryset = Office.objects.all()
        resource_name = 'office'


#### INTERACTING W THE API FROM CURL ####
# curl --dump-header - -H "Content-Type: application/json" -X POST --data '{"name": "hello", "description": "world"}' http://localhost:8000/api/v1/indicator/?username=john&password=Dinginator06
  ## ^^ this doesnt work because the request needs to be logged in...


## CREATING AN API KEY ##
# from tastypie.models import ApiKey
# from django.contrib.auth.models import User
# john = User.objects.get(username='john')
# api_key = ApiKey.objects.create(user=john)

# http://127.0.0.1:8000/api/v1/datapoint/?username=john&api_key=3018e5d944e1a37d2e2af952198bef4ab0d9f9fc&format=json
