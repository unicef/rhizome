
import pprint as pp
from dateutil import parser
import StringIO
import csv,json,math
import numpy as np
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
from django.http import HttpResponse
from django.db.models import Sum

from stronghold.decorators import public
import pandas as pd

from datapoints.models import *


class CustomSerializer(Serializer):
    formats = ['json', 'csv']
    content_types = {
        'json': 'application/json',
        'csv': 'text/csv',
    }

    def campaign_region_pivot(self,list_of_dicts):

        meta = None

        try:
            objects = list_of_dicts['objects']
        except KeyError as e:
            objects = []

        if not meta:
            try:
                meta = list_of_dicts['meta']
            except KeyError as e:
                pass

        df = pd.DataFrame(objects)

        try: # this block is used to pivot the parent region aggregate query
            pivoted = pd.pivot_table(df, values='the_sum', index=['parent_region', 'campaign'],
                     columns=['indicator'],aggfunc = lambda x: x)

            return pivoted, meta

        except KeyError as err:
            pass

        try: # this block is used to pivot basic api requests
            pivoted = pd.pivot_table(df, values='value', index=['region', 'campaign'],
                     columns=['indicator'],aggfunc = lambda x: x)
        except KeyError:
            pivoted = pd.DataFrame()

        return pivoted, meta


    def to_csv(self, data, options=None):

        options = options or {}
        data = self.to_simple(data, options)

        pivoted,meta = self.campaign_region_pivot(data)

        csv = StringIO.StringIO(str(pivoted.to_csv()))

        return csv


    def to_json(self, data, options=None):
        ## This needs to get Cleaned up
        ## also need a param that gives one obj per datapoint record
        response = {}
        response_objects = []

        options = options or {}
        data = self.to_simple(data, options)

        pivoted,meta = self.campaign_region_pivot(data)

        # replace NaN with None
        cleaned = pivoted.astype(object).replace(np.nan, 'None')
        # df1 = df.astype(object).replace(np.nan, 'None')

        for r_c in cleaned.iterrows():

            r_c_dict = {}

            rows = r_c[1] # zero = COLUMNS ; one = ROWS

            ix = rows.index # the index is the indicator

            indicator_list = []

            for i,(value) in enumerate(rows):
                ind_dict = {}

                ind_dict['indicator'] = ix[i]

                if value == 'None':
                    value = None

                ind_dict['value'] = value

                indicator_list.append(ind_dict)

            r_c_dict['indicators'] = indicator_list

            region,campaign = r_c[0][0],r_c[0][1]

            r_c_dict['region'] = region
            r_c_dict['campaign'] = campaign

            response_objects.append(r_c_dict)

        response['meta'] = meta

        response['objects'] = response_objects

        return json.dumps(response)
        # return json.dumps(data)



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

class OfficeResource(SimpleApiResource):
    '''Office Resource'''


    class Meta(SimpleApiResource.Meta):
        queryset = Office.objects.all()
        resource_name = 'office'
        filtering = {
            "slug": ('exact'),
            "id": ALL,
        }


class RegionResource(SimpleApiResource):
    '''Region Resource'''

    parent_region = fields.ForeignKey('datapoints.api.simple.RegionResource', 'parent_region', full=False, null=True)
    office = fields.ToOneField(OfficeResource, 'office')


    class Meta(SimpleApiResource.Meta):
        queryset = Region.objects.all()
        resource_name = 'region'
        filtering = {
            "slug": ('exact'),
            "id": ALL,
            "office": ALL,
            "region_type": ALL,
        }


class IndicatorResource(SimpleApiResource):
    '''Indicator Resource'''

    class Meta(SimpleApiResource.Meta):
        queryset = Indicator.objects.all()
        resource_name = 'indicator'
        filtering = {
            "slug": ('exact'),
            "id": ALL,
        }

class CampaignResource(SimpleApiResource):
    '''Campaign Resource'''

    office = fields.ToOneField(OfficeResource, 'office')


    class Meta(SimpleApiResource.Meta):
        queryset = Campaign.objects.all()
        resource_name = 'campaign'
        filtering = {
            "slug": ('exact'),
            "id": ALL,
            "office": ALL,
        }


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
        filtering = {
            "slug": ('exact'),
            "id": ALL,
        }


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
        max_limit = None


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

        return campaign_ids

    def parse_url_params(self,query_dict):


        ## ABSTRACT THIS USING THE DICTIONARY BELOW ##

        # region__in, campaign__in, indicator__in, the_limit = [],[],[],[]
        # expected_params = { 'the_limit':the_limit,'region__in':region__in,\
        #     'campaign__in':campaign__in,'indicator__in':indicator__in\,
        #     'the_offset':the_ofset }

        try:
            the_offset = int(query_dict['the_offset'])
        except KeyError:
            the_offset = 0

        try:
            the_limit = int(query_dict['the_limit'])
        except KeyError:
            the_limit = 10

        try:
            region_in = query_dict['region__in']
        except KeyError:
            region_in = []

        try:
            campaign_in = query_dict['campaign__in']
        except KeyError:
            campaign_in = []

        try:
            indicator_in = query_dict['indicator__in']
        except KeyError:
            indicator_in = []


        return region_in, campaign_in, indicator_in, the_limit, the_offset

    def get_regions_and_campaigns_to_filter(self,query_dict):
        '''
        Applying the limit to the region / campaign combo/
        THis needs alot of cleanup
        '''
        # get the params from the query dict
        regions, campaigns, indicators, the_limit, the_offset = \
            self.parse_url_params(query_dict)

        start_at = the_offset * the_limit
        end_at = the_offset * the_limit + the_limit


        # find all of the distinct regions / campaigns in the db
        if isinstance(indicators,list):
            # this means the indicator request is null
            indicator_list = indicators
            all_region_campaign_tuples = DataPoint.objects.values_list('region',\
                'campaign').distinct()

        else:
            # find the distinct campaing / region tuples for those indicators
            indicator_list = [int(ind) for ind in indicators.split(',')]

            all_region_campaign_tuples =DataPoint.objects.filter(indicator__in=\
                indicator_list).values_list('region','campaign').distinct()

        # if there was no region or campaign passed in just take the first
        # x elements in the list ( where x is the_limit ) and return that

        if len(regions) == 0 and len(campaigns) == 0:
            return all_region_campaign_tuples[start_at:end_at], indicator_list

        final_region_campaign_tuples = []

        # loop through all of the distinct campaigns/regions in the db and if
        # the request matches then add to the array that will be returned


        for i, (r,c) in enumerate(all_region_campaign_tuples):

            if start_at <= i <= end_at:

                if len(final_region_campaign_tuples) == the_limit:
                    return final_region_campaign_tuples, indicator_list

                elif str(r) in regions and str(c) in campaigns:
                    final_region_campaign_tuples.append((r,c))

                elif str(r) in regions and len(campaigns) == 0:
                    final_region_campaign_tuples.append((r,c))

                elif len(regions) == 0 and str(c) in campaigns:
                    final_region_campaign_tuples.append((r,c))

                else:
                    pass


        return final_region_campaign_tuples, indicator_list

    def alter_list_data_to_serialize(self, request, data):

        query_dict = dict(request.GET)
        query_dict.pop("username",None)
        query_dict.pop("api_key",None)
        data['meta']['query_dict'] = query_dict

        data['meta'].pop("limit",None)
        data['meta'].pop("offset",None)

        return data

    def obj_get_list(self, bundle, **kwargs):
        '''
        Overriding this method because if i dont, the filters are applied
        to the aggregate and because of whcih i get no data
        '''
        # Filtering disabled for brevity...
        return self.get_object_list(bundle.request)


    def get_object_list(self, request):
        '''
        Evan needs ot be able to limit by region/campaign pairs so here
        i override the get object list with a method that finds the regions
        and campaigns that coorespond with the limit passed in conjunction
        with the campaign / region list
        '''
        query_dict = request.GET
        region_campaign_tuples, indicators = self.get_regions_and_campaigns_to_filter(query_dict)

        regions = list(set([rc[0] for rc in region_campaign_tuples]))
        campaigns = list(set([rc[1] for rc in region_campaign_tuples]))

        if len(indicators) > 0:

            object_list = DataPoint.objects.filter(
                region__in = regions,
                campaign__in = campaigns,
                indicator__in = indicators
            )

        else:
            object_list = DataPoint.objects.filter(
                region__in = regions,
                campaign__in = campaigns,
            )



        return object_list


    def dehydrate(self, bundle):
        '''
        Depending on the <uri_display> parameter, return to the bundle
        the name, resurce_uri, slug or ID of the resource
        '''

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
