import sys
import json
from pprint import pprint

from django.db import connection
from datapoints.models import *

class CalcTarget(object):

    def __init__(self):

        # self.cursor = connection.cursor()
        self.global_cache = dict()

        # return self.run_engine(158,0)
        print 'ENGINE IS ABOUT TO RUN!!!'


    def run_engine(self,campaign_id, test_mode):
        """Run the calc and agg engine for a campaign"""
        if test_mode == 1:
            (computed_indicators, regions, datapoints) = load_test_data()
        else:
            (computed_indicators, regions) = self.load_calc_agg_db_data()
            sys.stderr.write("Loading campaign %d datapoints from db...\n" % (campaign_id))
            datapoints = self.get_campaign_datapoints(campaign_id)

        (calc_row_dict, calc_order, region_graph, region_order) = \
            self.make_agg_calc_derived_metadata(computed_indicators, regions)
        sys.stderr.write("Making dict from datapoints...\n")
        output_dict = self.make_datapoint_dict(datapoints)
        sys.stderr.write("Aggregating...\n")
        output_dict = self.aggregate_campaign(output_dict, region_graph, region_order, \
                                        campaign_id)
        sys.stderr.write("Calculating...\n")
        output_dict = self.run_calculations(output_dict, calc_order, calc_row_dict, campaign_id)
        return (output_dict, region_graph, region_order)


    def load_calc_agg_db_data(self):
        """Load initial data for running agg and calc for a campaign"""
        self.global_cache
        sys.stderr.write("Loading calc models from db...\n")
        if "computed_indicators" not in self.global_cache:
            self.global_cache['computed_indicators'] = self.get_computed_indicators()
            sys.stderr.write("Loading regions from db...\n")
            self.global_cache['regions'] = self.get_regions()
        return (self.global_cache['computed_indicators'], self.global_cache['regions'])

    def get_computed_indicators(self):
        """Select indicator components for calculations from db"""

        # indicators = self.cursor.fetchall()

        indicators = CalculatedIndicatorComponent.objects.raw("""
            SELECT
              id
            , indicator_id
            , indicator_component_id
            , calculation
            FROM calculated_indicator_component""")


        return indicators

    def get_regions(self):
        """Select regions from db"""
        regions = Region.objects.raw("SELECT id, office_id, name, parent_region_id FROM region")
        return regions

    def get_campaign_datapoints(self,campaign_id):
        """Select campaign datapoints from db"""

        datapoints = DataPoint.objects.raw("""
            SELECT region_id, indicator_id, value, campaign_id FROM datapoint
            WHERE campaign_id = %d AND value != FLOAT8 'NaN'""",[campaign_id])


        return datapoints

    def make_agg_calc_derived_metadata(self, computed_indicators, regions):
        """Derive metadata for running agg and calc for a campaign"""

        sys.stderr.write("Prepping for calcs...\n")
        if "calc_graph" not in self.global_cache:
            self.global_cache['calc_graph'] = self.make_calc_graph(computed_indicators)
            self.global_cache['calc_row_dict'] = self.make_calc_dict(computed_indicators)
            self.global_cache['calc_order'] = self.get_compute_order(self.global_cache['calc_graph'])
            self.global_cache['region_graph'] = self.make_region_graph(regions)
            self.global_cache['region_order'] = self.get_compute_order(self.global_cache['region_graph'])
        return (self.global_cache['calc_row_dict'],
                self.global_cache['calc_order'], self.global_cache['region_graph'],
                self.global_cache['region_order'])

    def make_calc_graph(self, indicators):
        """Make graph of calculation dependencies."""
        graph = dict()

        for row in indicators:
            # SELECT indicator_id, indicator_component_id, calculation FROM
            ind_id = row.indicator_id
            if ind_id not in graph:
                graph[ind_id] = dict()
            ind_comp_id = row.indicator_component_id
            calc = row.calculation
            #graph dict's values are the set of each indicator's  dependencies
            graph[ind_id][ind_comp_id] = {'calc':calc}
        return graph

    def make_calc_dict(self, indicators):
        """Make an index of row dictionaries for calculations where index keys are indicator_id's"""
        graph = dict()
        for row in indicators:

            ind_id = row.indicator_id
            if ind_id not in graph:
                graph[ind_id] = list()
            graph[ind_id].append(row)
        return graph

    def get_compute_order(self,graph):
        """Calculate traversal order for dependency graph using dfs. Order is simply \
        the node depth in reverse order"""
        #test data to just test the dfs algorithm
        #graph = {'3': set(['1', '2']), '2': set(['1', '0', '4', '5']), '4':set(['0']),
        #   '6': set(['7']), '7': set(['8']),
        #   '9': set(['10', '11']), '10': set(['12']), '11': set(['12'])}

        visited = {b:0 for a in graph for b in graph[a]}
        #starts are calc nodes that do not appear as components for other calcs
        kids = [b for a in graph for b in graph[a]]
        starts = [a for a in graph if a not in kids]
        for start in starts:
            visited[start] = 0
            visited = self.dfs(graph, start, visited, 0)
        dependency_list = [{k:v} for v, k in sorted([(v, k) for k, v in visited.items()], reverse=True)]
        return dependency_list

    def dfs(self, graph, start, visited, depth):
        """Run recursive dfs through a dependency graph. For nodes where multiple paths are \
        possible, the maximum depth is stored"""
        if visited[start] < depth:
            visited[start] = depth
        if start in graph:
            children = graph[start]
            for child in children:
                visited = self.dfs(graph, child, visited, depth+1)
        return visited

    def make_region_graph(self, regions):
        """Make graph of region dependencies."""
        graph = dict()

        for row in regions:
            reg_id = row.id
            if reg_id not in graph:
                if reg_id != None:
                    graph[reg_id] = dict()
            parent_id = (row.parent_region_id)
            if parent_id != None:
                if parent_id not in graph:
                    graph[parent_id] = dict()
                graph[parent_id][reg_id] = dict()
        return graph

    def make_datapoint_dict(self, indicators):
        """Make a two-level index of row dictionaries for datapoints where level1 key is \
        region_id and level 2 is indicator_id"""
        output = dict()
        for row in indicators:
            region_id = row.region_id
            indicator_id = row.indicator_id
            if region_id not in output:
                output[region_id] = dict()
            if indicator_id not in output[region_id]:
                output[region_id][indicator_id] = dict()
            output[region_id][indicator_id] = row
        return output

    def aggregate_campaign(self, output_dict, region_graph, region_order, campaign_id):
        """This function kicks off the aggregation process for a campaign"""
        regions = [b for a in region_order for b in a]
        indicators = set()
        for region in regions:
            if region in output_dict:
                for ind in output_dict[region]:
                    indicators.add(ind)
            else:
                output_dict[region] = dict()
            for indicator in indicators:
                indval = None
                # always use the datapoint if available
                indval = self.find_output_dict_value(output_dict, indicator, region)

                # if datapoint non existent, check children
                if indval == None and region in region_graph:
                    indval = self.aggregate_child_values(region_graph, region, \
                                                            output_dict, \
                                                            indicator, "sum")

                if indval != None:
                    if indicator not in output_dict:
                        output_dict[region][indicator] = {'region_id': region, \
                                                        'indicator_id': indicator, \
                                                        'campaign_id': campaign_id}
                    output_dict[region][indicator]['value'] = indval
        return output_dict


    def find_output_dict_value(self, output_dict, indicator, region):
        """Obtain value for indicator and region in output_dict if it exists"""
        retval = None
        if region in output_dict:
            if indicator in output_dict[region]:
                if 'value' in output_dict[region][indicator]:
                    retval = output_dict[region][indicator]['value']
        return retval

    def aggregate_child_values(self, region_graph, region, output_dict, \
                                        indicator, agg_type="sum"):
        """Aggregate values a level below using aggregation of choice (sum/mean/count)"""
        region_children = region_graph[region]
        retval = None
        child_elems = list()
        if region_children:
            for child_region in region_children:
                if child_region in output_dict:
                    if indicator in output_dict[child_region]:
                        child_row = output_dict[child_region][indicator]
                        if 'value' in child_row:
                            child_elems.append(child_row['value'])
        if agg_type == "sum":
            if len(child_elems) > 0:
                retval = sum(child_elems)
        elif agg_type == "mean":
            if len(child_elems) > 0:
                retval = float(sum(child_elems))/len(child_elems)
        elif agg_type == "count":
            if len(child_elems) > 0:
                retval = len(child_elems)
        return retval


    def run_calculations(self, output_dict, calc_order, calc_row_dict, campaign_id):
        """Kicks off the calculations process for a campaign"""
        calcs = [b for a in calc_order for b in a]
        for region in output_dict:
            print region
            print '======'
            for indicator in calcs:
                indicator_value_exists = False
                #Always use the existing datapoint value if it exists
                if indicator in output_dict[region]:
                    if 'value' in output_dict[region][indicator]:
                        indicator_value_exists = True
                #Otherwise, run the calculation function
                if not indicator_value_exists:
                    calc_value = self.get_indicator_calc_value(output_dict, calc_row_dict, \
                                                        indicator, region)
                    if calc_value != None:
                        if indicator not in output_dict:
                            output_dict[region][indicator] = {'region_id': region, \
                                                             'indicator_id': indicator, \
                                                             'campaign_id': campaign_id}
                        output_dict[region][indicator]['value'] = calc_value
        return output_dict


    def get_indicator_calc_value(self,output_dict, calc_row_dict, indicator, region):
        """Obtain indicator value using calculation specified in db"""
        return_val = None
        if indicator in calc_row_dict:

            calc_components = calc_row_dict[indicator]
            # calc_components = json.loads(calc_components_str)
            # [264, 252, u'PART_TO_BE_SUMMED']
            # [indicator, value, calculation]

            calc_types = {a.calculation for a in calc_components}
            calc_components = self.populate_component_values(output_dict,calc_components,region)
            calc_list = [{a.calculation: a.indicator_component_id} for a in calc_components]# if 'value' in a and 'calculation' in a]

            # calc_list = [{a[2]: a[1]} \
            if 'PART' in calc_types and 'WHOLE' in calc_types:
                return_val = self.get_part_whole(calc_list)
            elif 'PART_TO_BE_SUMMED' in calc_types:
                return_val = self.get_summation(calc_list)
            elif 'WHOLE_OF_DIFFERENCE' in calc_types:
                return_val = self.get_part_whole_of_difference(calc_list)
        return return_val


    def populate_component_values(self, output_dict, calc_components, region):
        """Populate component values for each calculation"""
        for i, component in enumerate(calc_components):

            indicator = component.indicator_component_id
            indicator_component_value = self.find_output_dict_value(output_dict, indicator, region)
            if indicator_component_value != None:
                calc_components[i].value = indicator_component_value
        return calc_components

    def get_summation(self, calc_list):
        """Run summation calculation"""
        retval = None
        values = [a[b] for a in calc_list for b in a if b == "PART_TO_BE_SUMMED"]
        if len(values) > 0:
            retval = sum([float(a) for a in values])
        return retval

    def get_part_whole_of_difference(self, calc_list):
        """Run part whole of difference calculation"""
        retval = None
        simple_dict = {b:a[b] for a in calc_list for b in a}
        if 'PART_OF_DIFFERENCE' in simple_dict and simple_dict['PART_OF_DIFFERENCE'] != None:
            if 'WHOLE_OF_DIFFERENCE' in simple_dict and simple_dict['WHOLE_OF_DIFFERENCE'] != None:
                if 'WHOLE_OF_DIFFERENCE_DENOMINATOR' in simple_dict and \
                    simple_dict['WHOLE_OF_DIFFERENCE_DENOMINATOR'] != 0:
                    retval = float(simple_dict['WHOLE_OF_DIFFERENCE'] - \
                                simple_dict['PART_OF_DIFFERENCE'])
                    retval = float(retval) / float(simple_dict['WHOLE_OF_DIFFERENCE_DENOMINATOR'])
        return retval

    def get_part_whole(self, calc_list):
        """Run part whole calculation"""
        retval = None
        simple_dict = {b:a[b] for a in calc_list for b in a}
        #print "gpw sd", simple_dict
        if 'PART' in simple_dict and simple_dict['PART'] != None:
            if 'WHOLE' in simple_dict and simple_dict['WHOLE'] != None:
                if simple_dict['WHOLE'] != 0:
                    retval = float(simple_dict['PART']) / float(simple_dict['WHOLE'])
        return retval
