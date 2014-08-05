from datapoints.models import AggregationExpectedData,AggregationType
from inspect import currentframe, getframeinfo
from datapoints.models import DataPoint, Indicator, Region, Campaign
from django.db.models.query import QuerySet
from tastypie.exceptions import ImmediateHttpResponse
from tastypie.http import HttpBadRequest

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
        indicator_id, region_id, campaign_id = self.parse_slugs_from_url( \
            query_dict)

        expected_data = AggregationExpectedData.objects.filter(
            aggregation_type = aggregation_type_id)

        prepped_data = []
        for d in expected_data:
            expected_data_dict = {}
            expected_data_dict[d.content_type] = [d.param_type]
            prepped_data.append(expected_data_dict)


        return prepped_data

    def parse_slugs_from_url(self,query_dict):

        indicator_id = self.get_id_from_slug_param('indicator_slug', \
            query_dict,Indicator)

        region_id = self.get_id_from_slug_param('region_slug', \
            query_dict,Region)

        campaign_id = self.get_id_from_slug_param('campaign_slug', \
            query_dict,Campaign)

        return indicator_id, region_id, campaign_id

    def get_id_from_slug_param(self,slug_key,query_dict,model):

        try:
            slug = query_dict[slug_key]
            obj_id = model.objects.get(slug=slug).id
        except KeyError:
            obj_id = None
            # there was an no indicator_slug in request
        except ObjectDoesNotExist:
            obj_id = -1
            # TO DO -> APPEND TO THE BUNDLE SOMETHING LIKE 'slug doesnt exist'
            # there was a slug in request but there is no cooresponding object



      #   print 'DEBUG'
      #   frameinfo = getframeinfo(currentframe())
      #   print frameinfo.filename, frameinfo.lineno
      #
      #   for d in expected_data:
      #       line_item_dict = {}
      #       line_item_dict['content_type'] = d.content_type
      #       line_item_dict['param_type'] = d.param_type
      #
      #       if d.param_type == 'SOLO' and d.content_type == 'INDICATOR':
      #           line_item_dict['data'] = indicator_id
      #
      #       if d.param_type == 'SOLO' and d.content_type == 'CAMPAIGN':
      #           line_item_dict['data'] = campaign_id
      #
      # #     if d.param_type == 'SOLO' and d.content_type == 'REGION':
      # #         line_item_dict['data'] = region_id
      #
      #       try:
      #           line_item_dict['data'] is not None
      #       except KeyError:
      #           return data
      #
      #       prepped_data.append(line_item_dict)
      #   fn = self.function_mappings[query_dict['api_method']]
      #   # data = fn(prepped_data)
      #
      #   ## NEED TO GIVE BACK AN OBJECT LIST FROM WHAT WEVE GOTTEN ##




    def calc_pct_single_reg_single_campaign(self,**kwargs):
        pass


    def calc_mean_single_ind_parent_region_single_campaign(self,**kwargs):
        pass


    def calc_mean_single_ind_single_region_array_campaign(self,data):
        pass

    def calc_avg_pct_many_region_solo_campaign(self,prepped_data):
        print 'the function is being called\n' * 10
        b_s_data = {"a":"b"}

        return b_s_data
