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


    def prep_data(self,api_method,query_dict,indicator_id,region_id, \
        campaign_id):

        prepped_data = []

        try:
            at = AggregationType.objects.get(fn_lookup=api_method)
            agg_type_id, fn = at.id, at.fn_lookup
            expected_data = AggregationExpectedData.objects.filter(aggregation_type\
                 = agg_type_id)

        except AggregationType.DoesNotExist:
            expected_data = []
            # somehow report this to the results for the get request


        data_is_prepped = True
        for d in expected_data:

            line_item_dict = {}

            if d.param_type == 'SOLO' and d.content_type == 'INDICATOR':
                line_item_dict['data'] = indicator_id

            if d.param_type == 'SOLO' and d.content_type == 'REGION':
                line_item_dict['data'] = region_id

            if d.param_type == 'SOLO' and d.content_type == 'CAMPAIGN':
                line_item_dict['data'] = campaign_id


            line_item_dict['content_type'] = d.content_type
            line_item_dict['param_type'] = d.param_type

            try:
                line_item_dict['data'] = query_dict[d.slug]
            except KeyError:
                data_is_prepped = False

            prepped_data.append(line_item_dict)

        if data_is_prepped:
            fn = self.function_mappings[api_method]
            fn(prepped_data)

        pp.pprint(prepped_data)

        data = {'data':'hello world!'}
        error = None


    def calc_pct_single_reg_single_campaign(self,**kwargs):
        pass


    def calc_mean_single_ind_parent_region_single_campaign(self,**kwargs):
        pass


    def calc_mean_single_ind_single_region_array_campaign(self,**kwargs):
        pass

    def calc_avg_pct_many_region_solo_campaign(self,prepped_data):
        print 'the function is being called\n' * 10
