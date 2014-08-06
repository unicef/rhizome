from datapoints.models import AggregationExpectedData,AggregationType
from inspect import currentframe, getframeinfo
from datapoints.models import DataPoint, Indicator, Region, Campaign
from django.db.models.query import QuerySet
from django.core.exceptions import ObjectDoesNotExist
from tastypie.exceptions import ImmediateHttpResponse
# from tastypie.resources import ModelResource,Resource, ALL
from tastypie.http import HttpBadRequest
from tastypie import fields
from django.utils.decorators import method_decorator

from datapoints.api.base import BaseApiResource

import pprint as pp

class ResultObject(object):
    '''We need a generic object to shove data in/get data from.
    This object will store either results or errors as dictionary, so we'll lightly
    wrap that with this class'''

    def __init__(self,initial=None):

        self.__dict__['_data'] = {}

        if hasattr(initial, 'items'):
            self.__dict__['_data'] = initial


    def __getattr__(self, name):
        return self._data.get(name, None)

    def __setattr__(self, name, value):
        self.__dict__['_data'][name] = value

    def to_dict(self):
        return self._data

class AggregateResource(BaseApiResource):
    '''This resource is our own resource that we wrote from scratch to implement
    complex aggregate queries that dont just rely on the "model resource" class
    from tastypie.  Here Just like a Django ``Form`` or ``Model``, we're
    defining all the fields we're going to handle with the API here. for more
    information on how i built this resource see
    http://django-tastypie.readthedocs.org/en/latest/non_orm_data_sources.html
    '''

    key = fields.CharField(attribute='key')
    value = fields.CharField(attribute='value')

    def __init__(self):
        self.function_mappings = {
          'calc_pct_single_reg_single_campaign' :
              self.calc_pct_single_reg_single_campaign,
          'calc_mean_single_ind_parent_region_single_campaign' :
              self.calc_mean_single_ind_parent_region_single_campaign,
          'calc_mean_single_ind_single_region_array_campaign' :
              self.calc_mean_single_ind_single_region_array_campaign,
          'calc_avg_pct_many_region_solo_campaign' :
              self.calc_avg_pct_many_region_solo_campaign
        }

    class Meta(BaseApiResource.Meta):
        resource_name = 'aggregate'
        object_class = ResultObject
        allowed_methods = ['get']


    def detail_uri_kwargs(self, bundle_or_obj):
        kwargs = {}

        # if isinstance(bundle_or_obj, Bundle):
        #     kwargs['pk'] = bundle_or_obj.obj.uuid
        # else:
        #     kwargs['pk'] = bundle_or_obj.uuid

        return kwargs

    def full_dehydrate(self,bundle,for_list):
        return bundle

    def get_object_list(self, request):
        '''in this method we pass the query dictionary to the prep data method
        which prepares the data to be aggregated, and then passes the relevant
        data to the api_method in the request.'''

        cust_object_list = []
        aggregate_data = self.prep_data(request.GET)

        print 'AGG DATA'
        pp.pprint(aggregate_data)

        for k,v in aggregate_data.iteritems():

            new_obj = ResultObject(initial='some_data')
            new_obj.key = k
            new_obj.value = v

            cust_object_list.append(new_obj)

        return cust_object_list


    def obj_get_list(self, bundle, **kwargs):
        # Filtering disabled for brevity...
        return self.get_object_list(bundle.request)

    def obj_get(self):
        bucket = self._bucket()
        message = bucket.get(kwargs['pk'])
        return AggregateObject(initial=message.get_data())

    def rollback(self):
        pass

    def prep_data(self,query_dict):

        ## Ensure that the request has an api_method argument ##
        try:
            request_api_method = query_dict['api_method']
        except KeyError as e:
            # data = {}
            raise ImmediateHttpResponse(HttpBadRequest('"api_method" is a \
            required parameter for the aggregate resource.  Please try again \
            specifing the api_method you would like to aggregate on\
            for more information see <LINK TO DOCS>'))

        ## Ensure that the api method exists in the database ##
        try:
            at = AggregationType.objects.get(slug=request_api_method)
            fn = self.function_mappings[at.slug]
        except AggregationType.DoesNotExist as e:
            raise ImmediateHttpResponse(HttpBadRequest('"' + request_api_method\
            + ' is not a recognized api method. Please check your request \
            and try again'))

        prepped_data = self.match_data(query_dict, at.id)
        final_data = fn(prepped_data)

        print 'FINAL DATA: ' + str(final_data)

        return final_data

    def match_data(self,query_dict,aggregation_type_id):

        ## parse the slugs and find the relevant IDs
        indicator_id, region_id, campaign_id, indicator_part_id, \
          indicator_whole_id = self.parse_slugs_from_url(query_dict)

        expected_data = AggregationExpectedData.objects.filter(
            aggregation_type = aggregation_type_id)

        prepped_data = []

        for d in expected_data:
            expected_data_dict = {}
            expected_data_dict[d.content_type] = [d.param_type]

            if d.content_type == 'INDICATOR' and indicator_id:
                expected_data_dict['pk'] = indicator_id

            if d.slug == 'indicator-part' and indicator_part_id:
                expected_data_dict['pk'] = indicator_part_id

            if d.slug == 'indicator-whole' and indicator_whole_id:
                expected_data_dict['pk'] = indicator_whole_id

            if d.content_type == 'REGION' and region_id:
                expected_data_dict['pk'] = region_id

            if d.content_type == 'CAMPAIGN' and campaign_id:
                expected_data_dict['pk'] = campaign_id

            prepped_data.append(expected_data_dict)

        pp.pprint(prepped_data)
        return prepped_data


    #####################################################
    #### THESE ARE ALL OF THE AGGREGATION FUNCTINOS #####
    #####################################################


    def calc_pct_single_reg_single_campaign(self , prepped_data):

        b_s_data = {"x","y"}

        return b_s_data

    def calc_mean_single_ind_parent_region_single_campaign(self,**kwargs):
        pass


    def calc_mean_single_ind_single_region_array_campaign(self,data):
        pass

    def calc_avg_pct_many_region_solo_campaign(self,prepped_data):

        b_s_data = {"calc_avg_pct_many_region_solo_campaign":"is being called"}
        print b_s_data
        print b_s_data
        print b_s_data
        print b_s_data
        print b_s_data


        return b_s_data


## for testing: http://localhost:8000/api/v1/aggregate/?api_key=3018e5d944e1a37d2e2af952198bef4ab0d9f9fc&format=json&username=john&api_method=calc_avg_pct_many_region_solo_campaign&region_slug=11-lpds-of-south-region&indicator_part=number-of-children-missed-due-to-refusal-to-accept-opv&indicator_whole=number-of-children-missed-total&campaign_slug=nigeria-2019-10-01
