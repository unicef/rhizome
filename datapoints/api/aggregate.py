from datapoints.models import AggregationExpectedData,AggregationType
from inspect import currentframe, getframeinfo
from datapoints.models import DataPoint, Indicator, Region, Campaign
from django.db.models.query import QuerySet
from tastypie.exceptions import ImmediateHttpResponse
from tastypie.http import HttpBadRequest
from django.core.exceptions import ObjectDoesNotExist

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

    def _query(self):
        pass


class FnLookUp(object):

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

    def parse_slugs_from_url(self,query_dict):

        indicator_id = self.get_id_from_slug_param('indicator_slug', \
            query_dict,Indicator)

        region_id = self.get_id_from_slug_param('region_slug', \
            query_dict,Region)

        campaign_id = self.get_id_from_slug_param('campaign_slug', \
            query_dict,Campaign)

        indicator_part_id = self.get_id_from_slug_param('indicator_part', \
            query_dict,Indicator)

        indicator_whole_id = self.get_id_from_slug_param('indicator_whole', \
            query_dict,Indicator)


        return indicator_id, region_id, campaign_id, indicator_part_id \
            ,indicator_whole_id

    def get_id_from_slug_param(self,slug_key,query_dict,model):

        try:
            slug = query_dict[slug_key]
            obj_id = model.objects.get(slug=slug).id
        except KeyError:
            obj_id = None
            # there was an no indicator_slug in request
        except ObjectDoesNotExist:
            obj_id = None

        return obj_id

    #####################################################
    #### THESE ARE ALL OF THE AGGREGATION FUNCTINOS #####
    #####################################################


    def calc_pct_single_reg_single_campaign(self,**kwargs):
        pass


    def calc_mean_single_ind_parent_region_single_campaign(self,**kwargs):
        pass


    def calc_mean_single_ind_single_region_array_campaign(self,data):
        pass

    def calc_avg_pct_many_region_solo_campaign(self,prepped_data):

        b_s_data = {"calc_avg_pct_many_region_solo_campaign":"is being called"}

        return b_s_data


## for testing: http://localhost:8000/api/v1/aggregate/?api_key=3018e5d944e1a37d2e2af952198bef4ab0d9f9fc&format=json&username=john&api_method=calc_avg_pct_many_region_solo_campaign&region_slug=11-lpds-of-south-region&indicator_part=number-of-children-missed-due-to-refusal-to-accept-opv&indicator_whole=number-of-children-missed-total&campaign_slug=nigeria-2019-10-01
