import pprint as pp
from dateutil import parser
import StringIO
import csv
from collections import defaultdict

from tastypie.serializers import Serializer
from tastypie.resources import ModelResource, ALL
from tastypie.authorization import Authorization
from tastypie.authentication import ApiKeyAuthentication
from tastypie import fields
from tastypie.bundle import Bundle
from tastypie.serializers import Serializer

from django.utils.decorators import method_decorator
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from stronghold.decorators import public
import pandas as pd

from datapoints.models import *


class CustomSerializer(Serializer):
    formats = ['json', 'jsonp', 'xml', 'yaml', 'html', 'plist', 'csv']
    content_types = {
        'json': 'application/json',
        'jsonp': 'text/javascript',
        'xml': 'application/xml',
        'yaml': 'text/yaml',
        'html': 'text/html',
        'plist': 'application/x-plist',
        'csv': 'text/csv',
    }

    def to_csv(self, data, options=None):

        options = options or {}
        data = self.to_simple(data, options)

        try:
            objects = data['objects']
            df = pd.DataFrame(objects)
            pivoted = pd.pivot_table(df, values='value', index=['region', 'campaign'],
                     columns=['indicator'],aggfunc = lambda x: x)

        except KeyError as e:
            pass

        csv = StringIO.StringIO(str(pivoted.to_csv()))

        return csv


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
        serializer = CustomSerializer()


    def filter_by_campaign(self,object_list,query_dict):
        ''' using the parse_campaign_st_end find the relevant campaign ids and
        return a result set where datpoitns are filtered by this list'''

        ## Find Start Date IDs ##
        campaigns_to_filter = Campaign.objects.all()


        try:
            c_st = query_dict['campaign_start']
            campaigns_to_filter = campaigns_to_filter.filter(start_date__gte=c_st)
        except KeyError:
             pass # campaigns_to_filter is all
        except ValidationError:
             campaigns_to_filter = []

        ## Find End Date IDs ##

        try:
            c_ed = query_dict['campaign_end']
            campaigns_to_filter = campaigns_to_filter.filter(end_date__lte=c_ed)
        except KeyError:
             pass
        except ValidationError:
             campaigns_to_filter = []

        campaign_ids = [c.id for c in campaigns_to_filter]


        filtered_object_list = object_list.filter(campaign_id__in=campaign_ids)

        return filtered_object_list


    def get_object_list(self, request):
        '''This method contains all custom filtering.
           Specifically, getting datapoints by campaign date range'''

        object_list = super(DataPointResource, self).get_object_list(request)
        query_dict = request.GET

        filtered_object_list = self.filter_by_campaign(object_list,query_dict)

        return filtered_object_list


    def dehydrate(self, bundle):
        ''' depending on the <uri_display> parameter, return to the bundle
        the name, resurce_uri, slug or ID of the resource'''

        fk_columns = {'indicator':bundle.obj.indicator,\
            'campaign':bundle.obj.campaign,\
            'region':bundle.obj.region}


        try: # Default to showing the ID of the resource
            uri_display = bundle.request.GET['uri_display']
        except KeyError:
            for f_str,f_obj in fk_columns.iteritems():
                bundle.data[f_str] = f_obj
            return bundle


        if uri_display == 'slug':
            for f_str,f_obj in fk_columns.iteritems():
                bundle.data[f_str] = f_obj.slug

        elif uri_display == 'id':
            for f_str,f_obj in fk_columns.iteritems():
                bundle.data[f_str] = f_obj.id


        elif uri_display == 'name':
            for f_str,f_obj in fk_columns.iteritems():
                bundle.data[f_str] = f_obj.name

        else: # if there is any other uri_display, return the full uri
            pass


        return bundle
