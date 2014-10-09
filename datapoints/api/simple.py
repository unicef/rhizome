import pprint as pp
from dateutil import parser

from tastypie.resources import ModelResource, ALL
from tastypie.authorization import Authorization
from tastypie.authentication import ApiKeyAuthentication
from tastypie import fields
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from tastypie.bundle import Bundle

from stronghold.decorators import public

from datapoints.api.base import parse_slugs_from_url,get_id_from_slug_param
from datapoints.models import *

class SimpleApiResource(ModelResource):
    '''
    This is the top level class all other Resource Classes inherit from this.
    The API Key authentication is defined here and thus is required by all
    other resources.  This class enherits fro the Tastyppie "ModelResource"

    See Here: http://django-tastypie.readthedocs.org/en/latest/resources.html?highlight=modelresource
    '''

    class Meta():
        authentication = ApiKeyAuthentication()
        authorization = Authorization()
        always_return_data = True


class RegionResource(SimpleApiResource):
    '''Region Resource'''

    class Meta(SimpleApiResource.Meta):
        queryset = Region.objects.all()
        resource_name = 'region'

class IndicatorResource(SimpleApiResource):
    '''Indicator Resource'''

    class Meta(SimpleApiResource.Meta):
        queryset = Indicator.objects.all()
        resource_name = 'indicator'
        filtering = {
            "slug": ('exact'),
            "id":('exact','gt','lt','range'),
        }

class CampaignResource(SimpleApiResource):
    '''Campaign Resource'''


    class Meta(SimpleApiResource.Meta):
        queryset = Campaign.objects.all()
        resource_name = 'campaign'

class UserResource(SimpleApiResource):
    '''User Resource'''

    class Meta(SimpleApiResource.Meta):
        queryset = User.objects.all()
        resource_name = 'user'
        excludes = ['password', 'username']
        allowed_methods = ['get']

class OfficeResource(SimpleApiResource):
    '''Office Resource'''

    class Meta(SimpleApiResource.Meta):
        queryset = Office.objects.all()
        resource_name = 'office'

    #############################################
    #############################################
    #############################################

class DataPointResource(SimpleApiResource):
    '''Datapoint Resource'''

    region = fields.ToOneField(RegionResource, 'region')
    indicator = fields.ToOneField(IndicatorResource, 'indicator')
    campaign = fields.ToOneField(CampaignResource, 'campaign')
    changed_by_id = fields.ToOneField(UserResource, 'changed_by')


    class Meta(SimpleApiResource.Meta):
        queryset = DataPoint.objects.all()
        resource_name = 'datapoint'
        excludes = ['note']
        filtering = {
            "value": ALL,
            "created_at":ALL,
            "indicator":ALL,
            "region": ALL ,
            "campaign": ALL,
        }
        allowed_methods = ['get']


    def parse_campaign_st_end(self,query_param,query_dict):

        try:
            param = query_dict[query_param]
        except KeyError:
            campaign_list = Campaign.objects.all()

        if query_param == 'campaign_start':

            try:
                campaign_list = Campaign.objects.filter(start_date__gte=param)
            except ValidationError:
                return None

        elif query_param == 'campaign_end':

            try:
                campaign_list = Campaign.objects.filter(end_date__lte=param)
            except ValidationError:
                return None

        campaign_list_ids = [c.id for c in campaign_list]

        print campaign_list_ids
        return campaign_list_ids



    def get_object_list(self, request):
        '''This method contains all custom filtering.
           Specifically, getting datapoints by campaign date range'''

        object_list = super(DataPointResource, self).get_object_list(request)
        query_dict = request.GET

        camp_st_list = self.parse_campaign_st_end('campaign_start',query_dict)
        camp_ed_list = self.parse_campaign_st_end('campaign_end',query_dict)

        campaign_ids = set(camp_st_list).intersection(camp_ed_list)

        filtered_object_list = object_list.filter(campaign_id__in=campaign_ids)


        return filtered_object_list
