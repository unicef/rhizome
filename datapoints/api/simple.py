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

        all_data = ''

        header = ['region','campaign']
        tuple_dict = {}

        try:
            objects = data['objects']

            ## Build Header
            for row in objects:
                indicator_name = Indicator.objects.get(id=row['indicator']).name
                header.append(str(indicator_name))

                tuple_dict[row['region'],row['campaign']] = { Indicator.objects.get(id=row['indicator']).name : row['value'] }

            distinct_headers = list(set(header))
            all_data = all_data + str(distinct_headers).replace('[','').replace(']','') + '\n'

            for k,v in tuple_dict.iteritems():
                # K is a tuple with (campaign,region)
                # V is a dictionary with {indicator : value}

                to_write = ''

                # evaluate the key by interating over the headers
                for h in distinct_headers:
                    to_write = to_write + v[h]

                    print type(h)
                    print h

                to_write = to_write + str(k).replace('(','').replace(')','')

                all_data = all_data + to_write + '\n'

        except KeyError as e:
            print e
            pass
        except Exception as e:
            print 'ERROR ALERT'
            print e

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
