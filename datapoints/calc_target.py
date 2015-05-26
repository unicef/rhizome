
class CalcTarget(object):

    def __init__(self):

        print 'HELLO'

        x,y,z = self.run_engine(158,0)


    def run_engine(self,campaign_id, test_mode):
        """Run the calc and agg engine for a campaign"""
        if test_mode == 1:
            (computed_indicators, regions, datapoints) = load_test_data()
        else:
            (computed_indicators, regions) = self.load_calc_agg_db_data(cursor)
            sys.stderr.write("Loading campaign %d datapoints from db...\n" % (campaign_id))
            datapoints = get_campaign_datapoints(cursor, campaign_id)

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


    def load_calc_agg_db_data(self, cursor):
        """Load initial data for running agg and calc for a campaign"""
        global GLOBAL_CACHE
        sys.stderr.write("Connected to " +db_host+"\n")
        sys.stderr.write("Loading calc models from db...\n")
        if "computed_indicators" not in GLOBAL_CACHE:
            GLOBAL_CACHE['computed_indicators'] = self.get_computed_indicators(cursor)
            sys.stderr.write("Loading regions from db...\n")
            GLOBAL_CACHE['regions'] = get_regions(cursor)
        return (GLOBAL_CACHE['computed_indicators'], GLOBAL_CACHE['regions'])

    def get_computed_indicators(self,cursor):
        """Select indicator components for calculations from db"""
        cursor.execute("""SELECT indicator_id, indicator_component_id, calculation FROM
                          calculated_indicator_component""")
        indicators = cursor.fetchall()
        return indicators


if __name__ == "__main__":
    bla = CalcTarget()
