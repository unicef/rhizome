import sys
from django.db import connection


class CalcTarget(object):

    def __init__(self):

        print 'HELLO'

        self.cursor = connection.cursor()
        self.global_cache = dict()

        x,y,z = self.run_engine(158,0)


    def run_engine(self,campaign_id, test_mode):
        """Run the calc and agg engine for a campaign"""
        if test_mode == 1:
            (computed_indicators, regions, datapoints) = load_test_data()
        else:
            (computed_indicators, regions) = self.load_calc_agg_db_data()
            sys.stderr.write("Loading campaign %d datapoints from db...\n" % (campaign_id))
            datapoints = get_campaign_datapoints(campaign_id)

        (calc_row_dict, calc_order, region_graph, region_order) = \
            make_agg_calc_derived_metadata(computed_indicators, regions)
        sys.stderr.write("Making dict from datapoints...\n")
        output_dict = make_datapoint_dict(datapoints)
        sys.stderr.write("Aggregating...\n")
        output_dict = aggregate_campaign(output_dict, region_graph, region_order, \
                                        campaign_id)
        sys.stderr.write("Calculating...\n")
        output_dict = run_calculations(output_dict, calc_order, calc_row_dict, campaign_id)
        return (output_dict, region_graph, region_order)


    def load_calc_agg_db_data(self):
        """Load initial data for running agg and calc for a campaign"""
        self.global_cache
        sys.stderr.write("Loading calc models from db...\n")
        if "computed_indicators" not in self.global_cache:
            self.global_cache['computed_indicators'] = self.get_computed_indicators()
            sys.stderr.write("Loading regions from db...\n")
            self.global_cache['regions'] = get_regions(cursor)
        return (self.global_cache['computed_indicators'], self.global_cache['regions'])

    def get_computed_indicators(self):
        """Select indicator components for calculations from db"""
        self.cursor.execute("""SELECT indicator_id, indicator_component_id, calculation FROM
                          calculated_indicator_component""")
        indicators = cursor.fetchall()
        return indicators

    def get_regions(self):
        """Select regions from db"""
        cursor.execute("SELECT id, office_id, name, parent_region_id FROM region")
        indicators = self.cursor.fetchall()
        return indicators



if __name__ == "__main__":
    bla = CalcTarget()
