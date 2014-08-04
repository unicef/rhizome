from datapoints.models import AggregationExpectedData,AggregationType
import pprint as pp

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


    def prep_data(self,api_method,query_dict):

        prepped_data = []

        expected_data = AggregationExpectedData.objects.filter(aggregation_type = api_method.id)

        for d in expected_data:
            line_item_dict = {}
            line_item_dict['content_type'] = d.content_type
            line_item_dict['param_type'] = d.param_type

            try:
                line_item_dict['data'] = query_dict[d.param_type]
            except KeyError:
                pass

            prepped_data.append(line_item_dict)

        # pp.pprint(expected_data)
        fn = self.function_mappings[api_method.fn_lookup]
        fn(prepped_data)




    def calc_pct_single_reg_single_campaign(self,**kwargs):
        pass


    def calc_mean_single_ind_parent_region_single_campaign(self,**kwargs):
        pass


    def calc_mean_single_ind_single_region_array_campaign(self,**kwargs):
        pass


    def calc_avg_pct_many_region_solo_campaign(self,prepped_data):
        pp.pprint(prepped_data)
