from datapoints.models import AggregationExpectedData,AggregationType
from datapoints.models import DataPoint, Indicator, Region, Campaign, RegionRelationship
from datapoints.api.base import parse_slugs_from_url,get_id_from_slug_param

from django.db.models.query import QuerySet
from django.core.exceptions import ObjectDoesNotExist


from tastypie.exceptions import ImmediateHttpResponse
from tastypie.resources import ModelResource,Resource, ALL
from tastypie.bundle import Bundle
from tastypie.http import HttpBadRequest
from tastypie import fields


import pprint as pp

class ResultObject(object):
    '''
    We need a generic object to shove data in/get data from.
    This object will store either results or errors as dictionary, so we'll lightly
    wrap that with this class
    '''

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

    def _query(self):
        pass

class AggregateResource(Resource):
    '''
    This resource is our own resource that we wrote from scratch to implement
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
          'calc_pct_solo_region_solo_campaign' :
              self.calc_pct_solo_region_solo_campaign,
          'calc_pct_parent_region_solo_campaign' :
              self.calc_pct_parent_region_solo_campaign
        }

    class Meta:
        resource_name = 'aggregate'
        object_class = ResultObject
        allowed_methods = ['get']


    def get_object_list(self, request):
        '''
        in this method we pass the query dictionary to the prep data method
        which prepares the data to be aggregated, and then passes the relevant
        IDs to the api_method in the request.
        '''

        cust_object_list = []

        err, data = self.prep_data(request.GET)


        if err:

            error_obj = ResultObject()
            error_obj.key = 'ERROR'
            error_obj.value = err

            cust_object_list.append(error_obj)

        elif data:

            data_obj = ResultObject()
            data_obj.key = 'DATA'
            data_obj.value = data

            cust_object_list.append(data_obj)



        return cust_object_list


    ### THE METHODS ABOVE ARE OVERRIDDEN FROM THE TASTYPIE RESOURCE CLASS ###
            ### PREP DATA AND MATCH DATA ARE MY OWN METHODS ###

    def prep_data(self,query_dict):


        prepped_data = {}

        ## Ensure that the request has an api_method argument ##
        try:
            request_api_method = query_dict['api_method']
        except KeyError as e:
            err = "'api_method' is a required parameter for the aggregate resource.  Please try again specifing the api_method you would like to aggregate on or more information see https://clients.seedscientific.com/uf/UF04/polio/docs/_build/html/aggregate_api.html"
            return err, None

        ## Ensure that the api method exists in the database ##
        try:
            at = AggregationType.objects.get(slug=request_api_method)
        except AggregationType.DoesNotExist as e:
            err =  "'" + request_api_method + "'" + " is not a recognized api method. Please check your request and try again"
            return err, None

        ## Find the Data expected by that api method
        expected_data = AggregationExpectedData.objects.filter(
            aggregation_type = at.id)

        ## Make sure all of the params were passed by comparing the request
        ## to the expected data for that api method
        for ed in expected_data:

            try:
                expected_data_id = query_dict[ed.slug]
                prepped_data[ed.slug] = expected_data_id
            except KeyError as e:
                err = 'Missing Parameter. The api method "' + request_api_method + '" requires the '  + str(e) + ' parameter.'
                return err, None

        err, final_data = self.calc_value(prepped_data,request_api_method)

        return err, final_data

    def calc_value(self,prepped_data,request_api_method):

        fn = self.function_mappings[request_api_method]
        err, value = fn(prepped_data)

        return err, value


    #####################################################
    #### THESE ARE ALL OF THE AGGREGATION FUNCTINOS #####
    #####################################################

    def calc_pct_solo_region_solo_campaign(self, prepped_data):

        region_id = prepped_data['region_solo']
        campaign_id = prepped_data['campaign_solo']

        part = DataPoint.objects.get(
          region_id = region_id,
          campaign_id = campaign_id,
          indicator_id = prepped_data['indicator_part']
        ).value

        whole = DataPoint.objects.get(
          region_id = region_id,
          campaign_id = campaign_id,
          indicator_id = prepped_data['indicator_whole']
        ).value

        result = part / whole

        return None, result

    def calc_pct_parent_region_solo_campaign(self, prepped_data):

        region_list = self.get_sub_regions(prepped_data['region_parent'])
        campaign_id = prepped_data['campaign_solo']

        parts = DataPoint.objects.filter(
          region_id__in=region_list,
          campaign_id = campaign_id,
          indicator_id = prepped_data['indicator_part']
        )

        wholes = DataPoint.objects.filter(
          region_id__in=region_list,
          campaign_id = campaign_id,
          indicator_id = prepped_data['indicator_whole']
        )


        part_val = 0
        for part in parts:
            part_val += part.value


        whole_val = 0
        for whole in wholes:
            whole_val += whole.value

        print 'PART VAL: ' + str(part_val)
        print 'WHOLE VAL: ' + str(whole_val)


        result = part_val / whole_val


        return None, result

    def get_sub_regions(self,parent_region_id):

        rrs = RegionRelationship.objects.filter(region_0 = parent_region_id)

        regions = []

        # This is going to need to be RECURSIVE #
        for r in rrs:
            regions.append(r.region_1_id)

        return regions





    ## TASTY PIE MODEL RESOURCE PARAMS THAT I AM OVERRIDING ##

    def build_bundle(self, obj=None, data=None, request=None, objects_saved=None):
        """
        I AM OVERIDING THIS METHOD, BUT DO NOT THINK I NEED TO.  I SPENT ALOT
        OF TIME TRYING TO FIGURE OUR HOW AND WHY I WAS NOT GETTING DATA BACK
        FROM the FULL_DEHYDRATE METHOD IN THIS CUSTOM IMPLEMENTATION
        """
        if obj is None and self._meta.object_class:
            obj = self._meta.object_class()

        custom_data = {}
        custom_data[obj.key] = obj.value

        return Bundle(
            obj=obj,
            data=custom_data,
            request=request,
            objects_saved=objects_saved
        )


    def full_dehydrate(self,bundle,for_list):
        '''
        When i dont overide this method, i get a maximum recursion error.
        http://stackoverflow.com/questions/11570443/django-tastypie-throws-a-maximum-recursion-depth-exceeded-when-full-true-on-re
        '''
        return bundle


    def obj_get_list(self, bundle, **kwargs):
        return self.get_object_list(bundle.request)

    def obj_get(self,bundle, **kwargs):
        return bundle



## for testing: http://localhost:8000/api/v1/aggregate/?api_key=3018e5d944e1a37d2e2af952198bef4ab0d9f9fc&format=json&username=john&api_method=calc_avg_pct_many_region_solo_campaign&region_slug=11-lpds-of-south-region&indicator_part=number-of-children-missed-due-to-refusal-to-accept-opv&indicator_whole=number-of-children-missed-total&campaign_slug=nigeria-2019-10-01
