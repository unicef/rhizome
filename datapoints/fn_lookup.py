from datapoints.models import AggregationExpectedData,AggregationType
from inspect import currentframe, getframeinfo
from datapoints.models import DataPoint
from django.db.models.query import QuerySet

import pprint as pp

class ResultObject(object):
    '''We need a generic object to shove data in/get data from.
    This object will store either results or errors as dictionary, so we'll lightly
    wrap that with this class'''

    def __init__(self,initial=None):
        print 'this is working\n'
        print initial

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


    def prep_data(self,fn_id,query_dict,indicator_id,region_id, \
            campaign_id):

        print 'START PREP DATA METHOD\n' * 5

        prepped_data = []
        data_is_prepped = True
        error = {}

        data = QuerySet()
        data = []
        myobj = DataPoint.objects.get(id=19)
        # data._result_cache.append(d1)
        data.append(myobj)

        try:
            at = AggregationType.objects.get(id=fn_id)
            fn = at.slug
            expected_data = AggregationExpectedData.objects.filter(
                aggregation_type = fn_id)

        except AggregationExpectedData.DoesNotExist as e:
            error['error_msg']= 'there is no expected data for that agg \
            type.  Please make sure your api_method is correct, and contact \
            your systems administrator for further issues'
            return None

        print 'DEBUG'
        frameinfo = getframeinfo(currentframe())
        print frameinfo.filename, frameinfo.lineno

        for d in expected_data:

            line_item_dict = {}
            line_item_dict['content_type'] = d.content_type
            line_item_dict['param_type'] = d.param_type

            if d.param_type == 'SOLO' and d.content_type == 'INDICATOR':
                line_item_dict['data'] = indicator_id

            if d.param_type == 'SOLO' and d.content_type == 'CAMPAIGN':
                line_item_dict['data'] = campaign_id

      #     if d.param_type == 'SOLO' and d.content_type == 'REGION':
      #         line_item_dict['data'] = region_id

            try:
                line_item_dict['data'] is not None
            except KeyError:
                data_is_prepped = False
                error['error_msg'] = 'can not match expected data with request'
                error['expected_data'] = expected_data
                error['query_dict'] = query_dict


                return data

            prepped_data.append(line_item_dict)


        fn = self.function_mappings[query_dict['api_method']]
        # data = fn(prepped_data)

        ## NEED TO GIVE BACK AN OBJECT LIST FROM WHAT WEVE GOTTEN ##


        print 'WE MADE IT TO THE END OF THE PREP DATA METHOD'
        return data

        # pp.pprint(prepped_data)
        # error = None

    def calc_pct_single_reg_single_campaign(self,**kwargs):
        pass


    def calc_mean_single_ind_parent_region_single_campaign(self,**kwargs):
        pass


    def calc_mean_single_ind_single_region_array_campaign(self,data):
        pass

    def calc_avg_pct_many_region_solo_campaign(self,prepped_data):
        print 'the function is being called\n' * 10
