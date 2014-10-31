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



class CSVSerializer(Serializer):
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

        all_data = 'region,campaign'
        header = []
        tuple_dict = defaultdict(list)


        try:
            objects = data['objects']
            df = pd.DataFrame(objects)
            grouped = df.groupby(['region', 'campaign'])
            inds = [i[0] for i in df.groupby('indicator')] # distinct list of indicatorIDs

            for i in inds: # writing the header
                all_data += ',' + str(i)

            all_data +='\n'

            for g in grouped:
                grouped_key, grouped_data = g[0],g[1]
                all_data += str(grouped_key)
                all_data +=  '\n'

                i_care = grouped_data[['indicator','value']]

                print type(i_care)
                pp.pprint(i_care)


        except KeyError as e:
            print 'KEY ERROR'
            print e

        except Exception as e:
            print 'ERRRRRROR'
            print e


        all_data = all_data.replace('(','').replace(')','').replace('[','')\
            .replace(']','').replace("u'",'').replace("'",'')

        csv = StringIO.StringIO(str(all_data))

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
        serializer = CSVSerializer()


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

        bundle.data['indicator'] = bundle.obj.indicator.id
        bundle.data['campaign'] = bundle.obj.campaign.id
        bundle.data['region'] = bundle.obj.region.id
        bundle.data['changed_by_id'] = bundle.obj.changed_by.id


        return bundle
