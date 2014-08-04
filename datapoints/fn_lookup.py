
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

        print 'PREPPING DATA \n' * 100
        pass

    def calc_pct_single_reg_single_campaign(self):
        pass


    def calc_mean_single_ind_parent_region_single_campaign(self):
        pass


    def calc_mean_single_ind_single_region_array_campaign(self):
        pass


    def calc_avg_pct_many_region_solo_campaign(self):
        pass
