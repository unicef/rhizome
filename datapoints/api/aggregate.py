from datapoints.models import AggregationExpectedData,AggregationType
from datapoints.models import DataPoint, Indicator, Region, Campaign
from datapoints.api.simple import *

from django.db.models.query import QuerySet
from django.core.exceptions import ObjectDoesNotExist
from tastypie.exceptions import ImmediateHttpResponse
from tastypie.resources import ModelResource,Resource, ALL
from tastypie.bundle import Bundle
from tastypie.http import HttpBadRequest
from tastypie import fields
from tastypie.authorization import Authorization
from tastypie.authentication import ApiKeyAuthentication

import pprint as pp


class ParentRegionAggResource(SimpleApiResource):

    parent_region = fields.ToOneField(RegionResource, 'parent_region')
    indicator = fields.ToOneField(IndicatorResource, 'indicator')
    campaign = fields.ToOneField(CampaignResource, 'campaign')


    class Meta(SimpleApiResource.Meta):
        queryset = ParentRegionAgg.objects.all()
        resource_name = 'parent_region_agg'
        filtering = {
            "indicator": ALL,
            "parent_region":ALL,
            "campaign":ALL,
        }
        allowed_methods = ['get']
        serializer = CustomSerializer()
        max_limit = None


    def obj_get_list(self, bundle, **kwargs):
        ''' overriden from tastypie '''

        return self.get_object_list(bundle.request)

    def get_object_list(self, request):

        query_dict = request.GET
        query_kwargs = self.parse_query_params(query_dict)

        object_list = ParentRegionAgg.objects.filter(**query_kwargs)

        return object_list

    def parse_query_params(self,query_dict):

        query_kwargs = {}

        try:
            indicator__in = query_dict['indicator__in'].split(',')
            query_kwargs['indicator__in'] = indicator__in
        except KeyError:
            pass

        try:
            campaign__in = query_dict['campaign__in'].split(',')
            query_kwargs['campaign__in'] = campaign__in
        except KeyError:
            pass

        try:
            parent_region = query_dict['parent_region']
            query_kwargs['parent_region'] = parent_region
        except KeyError:
            pass


        return query_kwargs

    def dehydrate(self, bundle):
        '''
        # Depending on the <uri_display> parameter, return to the bundle
        # the name, resurce_uri, slug or ID of the resource
        # '''

        fk_columns = {'indicator':bundle.obj.indicator,\
            'campaign':bundle.obj.campaign,\
            'parent_region':bundle.obj.parent_region}


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


## ALL OF THIS BELOW IS OLD CODE BUT IS A GOOD EXAMPLE OF HOW TO CONSTRUCT ##
    ## AN API WITH MUCH MORE CONTROL THEN TASTYPIE GIVES OUT OF THE BOX ##

#
# class ResultObject(object):
#     '''
#     We need a generic object to shove data in/get data from.
#     This object will store either results or errors as dictionary, so we'll lightly
#     wrap that with this class
#     '''
#
#     def __init__(self,initial=None):
#
#         self.__dict__['_data'] = {}
#
#         if hasattr(initial, 'items'):
#             self.__dict__['_data'] = initial
#
#
#     def __getattr__(self, name):
#         return self._data.get(name, None)
#
#     def __setattr__(self, name, value):
#         self.__dict__['_data'][name] = value
#
#     def to_dict(self):
#         return self._data
#
#     def _query(self):
#         pass
#
# class AggregateResource(Resource):
#     '''
#     This resource is our own resource that we wrote from scratch to implement
#     complex aggregate queries that dont just rely on the "model resource" class
#     from tastypie.  Here Just like a Django ``Form`` or ``Model``, we're
#     defining all the fields we're going to handle with the API here. for more
#     information on how i built this resource see
#     http://django-tastypie.readthedocs.org/en/latest/non_orm_data_sources.html
#     '''
#
#     key = fields.CharField(attribute='key')
#     value = fields.CharField(attribute='value')
#
#     def __init__(self):
#         self.function_mappings = {
#           'calc_pct_solo_region_solo_campaign' :
#               self.calc_pct_solo_region_solo_campaign,
#           'calc_pct_parent_region_solo_campaign' :
#               self.calc_pct_parent_region_solo_campaign
#         }
#
#     class Meta:
#         resource_name = 'aggregate'
#         object_class = ResultObject
#         allowed_methods = ['get']
#         authentication = ApiKeyAuthentication()
#         authorization = Authorization()
#         always_return_data = True
#
#
#     def get_object_list(self, request):
#         '''
#         in this method we pass the query dictionary to the prep data method
#         which prepares the data to be aggregated, and then passes the relevant
#         IDs to the api_method in the request.
#         '''
#
#         cust_object_list = []
#
#         err, data = self.prep_data(request.GET)
#
#
#         if err:
#
#             error_obj = ResultObject()
#             error_obj.key = 'ERROR'
#             error_obj.value = err
#
#             cust_object_list.append(error_obj)
#
#         elif data:
#
#             data_obj = ResultObject()
#             data_obj.key = 'DATA'
#             data_obj.value = data
#
#             cust_object_list.append(data_obj)
#
#
#
#         return cust_object_list
#
#
#     ### THE METHODS ABOVE ARE OVERRIDDEN FROM THE TASTYPIE RESOURCE CLASS ###
#             ### PREP DATA AND MATCH DATA ARE MY OWN METHODS ###
#
#     def prep_data(self,query_dict):
#
#
#         prepped_data = {}
#
#         ## Ensure that the request has an api_method argument ##
#         try:
#             request_api_method = query_dict['api_method']
#         except KeyError as e:
#             err = "'api_method' is a required parameter for the aggregate resource.  Please try again specifing the api_method you would like to aggregate on or more information see https://clients.seedscientific.com/uf/UF04/polio/docs/_build/html/aggregate_api.html"
#             return err, None
#
#         ## Ensure that the api method exists in the database ##
#         try:
#             at = AggregationType.objects.get(slug=request_api_method)
#         except AggregationType.DoesNotExist as e:
#             err =  "'" + request_api_method + "'" + " is not a recognized api method. Please check your request and try again"
#             return err, None
#
#         ## Find the Data expected by that api method
#         expected_data = AggregationExpectedData.objects.filter(
#             aggregation_type = at.id)
#
#         if len(expected_data) < 1:
#             err = 'Aggregation Expected data is empty!  Please talk to your DB Admin to have the meta data inserted.'
#             return err, None
#
#         ## Make sure all of the params were passed by comparing the request
#         ## to the expected data for that api method
#         for ed in expected_data:
#
#             try:
#                 expected_data_id = query_dict[ed.slug]
#                 prepped_data[ed.slug] = expected_data_id
#             except KeyError as e:
#                 err = 'Missing Parameter. The api method "' + request_api_method + '" requires the '  + str(e) + ' parameter.'
#                 return err, None
#
#         err, final_data = self.calc_value(prepped_data,request_api_method)
#
#         return err, final_data
#
#     def calc_value(self,prepped_data,request_api_method):
#
#         fn = self.function_mappings[request_api_method]
#         err, value = fn(prepped_data)
#
#         return err, value
#
#
#     #####################################################
#     #### THESE ARE ALL OF THE AGGREGATION FUNCTINOS #####
#     #####################################################
#
#     def calc_pct_solo_region_solo_campaign(self, prepped_data):
#
#         try:
#             region_id = prepped_data['region_solo']
#             campaign_id = prepped_data['campaign_solo']
#
#             part = DataPoint.objects.get(
#               region_id = region_id,
#               campaign_id = campaign_id,
#               indicator_id = prepped_data['indicator_part']
#             ).value
#
#             whole = DataPoint.objects.get(
#               region_id = region_id,
#               campaign_id = campaign_id,
#               indicator_id = prepped_data['indicator_whole']
#             ).value
#
#             result = part / whole
#
#         except Exception as err:
#
#             return err, None
#
#         return None, result
#
#     def calc_pct_parent_region_solo_campaign(self, prepped_data):
#
#         try:
#
#             region_list = self.get_sub_regions(prepped_data['region_parent'])
#             campaign_id = prepped_data['campaign_solo']
#
#             parts = DataPoint.objects.filter(
#               region_id__in=region_list,
#               campaign_id = campaign_id,
#               indicator_id = prepped_data['indicator_part']
#             )
#
#             wholes = DataPoint.objects.filter(
#               region_id__in=region_list,
#               campaign_id = campaign_id,
#               indicator_id = prepped_data['indicator_whole']
#             )
#
#
#             part_val = 0
#             for part in parts:
#                 part_val += part.value
#
#
#             whole_val = 0
#             for whole in wholes:
#                 whole_val += whole.value
#
#             print 'PART VAL: ' + str(part_val)
#             print 'WHOLE VAL: ' + str(whole_val)
#
#             result = part_val / whole_val
#
#         except Exception as err:
#
#             return err, None
#
#
#         return None, result
#
#     def get_sub_regions(self,parent_region_id):
#         ''' FIX ME '''
#
#         regions = []
#
#         return regions
# 
#
#     ## TASTY PIE MODEL RESOURCE PARAMS THAT I AM OVERRIDING ##
#
#     def build_bundle(self, obj=None, data=None, request=None, objects_saved=None):
#         """
#         I AM OVERIDING THIS METHOD, BUT DO NOT THINK I NEED TO.  I SPENT ALOT
#         OF TIME TRYING TO FIGURE OUR HOW AND WHY I WAS NOT GETTING DATA BACK
#         FROM the FULL_DEHYDRATE METHOD IN THIS CUSTOM IMPLEMENTATION
#         """
#         if obj is None and self._meta.object_class:
#             obj = self._meta.object_class()
#
#         custom_data = {}
#         custom_data[obj.key] = obj.value
#
#         return Bundle(
#             obj=obj,
#             data=custom_data,
#             request=request,
#             objects_saved=objects_saved
#         )
#
#
#     def full_dehydrate(self,bundle,for_list):
#         '''
#         When i dont overide this method, i get a maximum recursion error.
#         http://stackoverflow.com/questions/11570443/django-tastypie-throws-a-maximum-recursion-depth-exceeded-when-full-true-on-re
#         '''
#         return bundle
#
#
#     def obj_get_list(self, bundle, **kwargs):
#         return self.get_object_list(bundle.request)
#
#     def obj_get(self,bundle, **kwargs):
#         return bundle
