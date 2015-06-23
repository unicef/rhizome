
## NOTE: THIS IS NOT PRODUCTION CODE.  THIS WAS WRITTEN BY MANISH NAG IN ORDER
## TO GENERATE TARTED DATA BASED ON THE CALCULATIONS THAT WE RUN WHEN
## AGGRETATING AND TRANSOFRMING THE RAW DATA INTO CALCULATED INDICATORS.
## THIS IS NOT PROUDCTION CODE, BUT IS IN VERSION CONTROL IN CASE WE NEED TO
## RUN THIS REPORT AGAIN IF WE ARE UNSURE THAT THE BEHAVIOR OF THE CALTULATION
## ENGINE IS CORRECT.

#!/usr/bin/env python
"""Run calculation engine to generate target data. Run in test mode, compare target data
against database, or examine data depth for campaign data"""
import psycopg2
from psycopg2.extras import RealDictCursor
import os
import pprint
import json
import sys
import csv
from joblib import Parallel, delayed
import multiprocessing
import time

def get_computed_indicators(cursor):
    """Select indicator components for calculations from db"""
    cursor.execute("""SELECT indicator_id, indicator_component_id, calculation FROM
                      calculated_indicator_component""")
    indicators = cursor.fetchall()
    return indicators

def make_calc_graph(indicators):
    """Make graph of calculation dependencies."""
    graph = dict()
    for row in indicators:
        ind_id = (row['indicator_id'])
        if ind_id not in graph:
            graph[ind_id] = dict()
        ind_comp_id = row['indicator_component_id']
        calc = row['calculation']
        #graph dict's values are the set of each indicator's  dependencies
        graph[ind_id][ind_comp_id] = {'calc':calc}
    return graph

def make_calc_dict(indicators):
    """Make an index of row dictionaries for calculations where index keys are indicator_id's"""
    graph = dict()
    for row in indicators:
        ind_id = (row['indicator_id'])
        if ind_id not in graph:
            graph[ind_id] = list()
        graph[ind_id].append(row)
    return graph

def get_regions(cursor):
    """Select regions from db"""
    cursor.execute("SELECT id, office_id, name, parent_region_id FROM region")
    indicators = cursor.fetchall()
    return indicators

def make_region_graph(indicators):
    """Make graph of region dependencies."""
    graph = dict()
    for row in indicators:
        reg_id = (row['id'])
        if reg_id not in graph:
            if reg_id != None:
                graph[reg_id] = dict()
        parent_id = (row['parent_region_id'])
        if parent_id != None:
            if parent_id not in graph:
                graph[parent_id] = dict()
            graph[parent_id][reg_id] = dict()
    return graph

def make_datapoint_dict(indicators):
    """Make a two-level index of row dictionaries for datapoints where level1 key is \
    region_id and level 2 is indicator_id"""
    output = dict()
    for row in indicators:
        region_id = row['region_id']
        indicator_id = row['indicator_id']
        if region_id not in output:
            output[region_id] = dict()
        if indicator_id not in output[region_id]:
            output[region_id][indicator_id] = dict()
        output[region_id][indicator_id] = row
    return output

def dfs(graph, start, visited, depth):
    """Run recursive dfs through a dependency graph. For nodes where multiple paths are \
    possible, the maximum depth is stored"""
    if visited[start] < depth:
        visited[start] = depth
    if start in graph:
        children = graph[start]
        for child in children:
            visited = dfs(graph, child, visited, depth+1)
    return visited

def get_campaign_datapoints(cursor, campaign_id):
    """Select campaign datapoints from db"""
    cursor.execute("""SELECT region_id, indicator_id, value, campaign_id FROM datapoint
                      where campaign_id = %d AND value != FLOAT8 'NaN'""" % (campaign_id))
    indicators = cursor.fetchall()
    return indicators

def get_campaigns(cursor):
    """Select campaigns from db"""
    cursor.execute("""SELECT id as campaign_id, slug, office_id FROM campaign ORDER BY start_date""")
    indicators = cursor.fetchall()
    return indicators


def get_indicators(cursor):
    """Select indicator metadata from db"""
    cursor.execute("""SELECT id as indicator_id, short_name FROM indicator""")
    indicators = cursor.fetchall()
    return indicators

def get_abstracted_data(cursor, campaign_id, region_id):
    """Select abstracted json from db that's used by the api. transform json string to \
    python object"""
    cursor.execute("""SELECT indicator_json FROM datapoint_abstracted where
                    campaign_id = %d AND region_id = %d""" % (campaign_id, region_id))
    json_data = cursor.fetchone()
    if json_data != None and 'indicator_json' in json_data:
        json_txt = json_data['indicator_json']
    else:
        print "Warning: no abstracted data for query: " + \
                "SELECT indicator_json FROM datapoint_abstracted where " + \
                "campaign_id = %d AND region_id = %d" % (campaign_id, region_id)
        return None

    if json_txt != None:
        return json.loads(json_txt)
    else:
        return None

def aggregate_child_values(region_graph, region, output_dict, \
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

def aggregate_campaign(output_dict, region_graph, region_order, campaign_id):
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
            indval = find_output_dict_value(output_dict, indicator, region)

            # if datapoint non existent, check children
            if indval == None and region in region_graph:
                indval = aggregate_child_values(region_graph, region, \
                                                        output_dict, \
                                                        indicator, "sum")

            if indval != None:
                if indicator not in output_dict:
                    output_dict[region][indicator] = {'region_id': region, \
                                                    'indicator_id': indicator, \
                                                    'campaign_id': campaign_id}
                output_dict[region][indicator]['value'] = indval
                #print region, indicator, indval
    return output_dict

def run_calculations(output_dict, calc_order, calc_row_dict, campaign_id):
    """Kicks off the calculations process for a campaign"""
    calcs = [b for a in calc_order for b in a]
    for region in output_dict:
        for indicator in calcs:
            indicator_value_exists = False
            #Always use the existing datapoint value if it exists
            if indicator in output_dict[region]:
                if 'value' in output_dict[region][indicator]:
                    indicator_value_exists = True
            #Otherwise, run the calculation function
            if not indicator_value_exists:
                calc_value = get_indicator_calc_value(output_dict, calc_row_dict, \
                                                    indicator, region)
                if calc_value != None:
                    if indicator not in output_dict:
                        output_dict[region][indicator] = {'region_id': region, \
                                                         'indicator_id': indicator, \
                                                         'campaign_id': campaign_id}
                    output_dict[region][indicator]['value'] = calc_value
    return output_dict

def get_indicator_calc_value(output_dict, calc_row_dict, indicator, region):
    """Obtain indicator value using calculation specified in db"""
    return_val = None
    if indicator in calc_row_dict:
        calc_components_str = json.dumps(calc_row_dict[indicator])
        calc_components = json.loads(calc_components_str)
        calc_types = {a['calculation'] for a in calc_components}
        calc_components = populate_component_values(output_dict, calc_components,
                                                    region)
        calc_list = [{a['calculation']: a['value']} \
                    for a in calc_components if 'value' in a and 'calculation' in a]
        if 'PART' in calc_types and 'WHOLE' in calc_types:
            return_val = get_part_whole(calc_list)
        elif 'PART_TO_BE_SUMMED' in calc_types:
            return_val = get_summation(calc_list)
        elif 'WHOLE_OF_DIFFERENCE' in calc_types:
            return_val = get_part_whole_of_difference(calc_list)
    return return_val

def populate_component_values(output_dict, calc_components, region):
    """Populate component values for each calculation"""
    for i, component in enumerate(calc_components):
        indicator = component['indicator_component_id']
        indicator_component_value = find_output_dict_value(output_dict, indicator, region)
        if indicator_component_value != None:
            calc_components[i]['value'] = indicator_component_value
    return calc_components

def find_output_dict_value(output_dict, indicator, region):
    """Obtain value for indicator and region in output_dict if it exists"""
    retval = None
    if region in output_dict:
        if indicator in output_dict[region]:
            if 'value' in output_dict[region][indicator]:
                retval = output_dict[region][indicator]['value']
    return retval

def get_part_whole(calc_list):
    """Run part whole calculation"""
    retval = None
    simple_dict = {b:a[b] for a in calc_list for b in a}
    #print "gpw sd", simple_dict
    if 'PART' in simple_dict and simple_dict['PART'] != None:
        if 'WHOLE' in simple_dict and simple_dict['WHOLE'] != None:
            if simple_dict['WHOLE'] != 0:
                retval = float(simple_dict['PART']) / float(simple_dict['WHOLE'])
    return retval

def get_summation(calc_list):
    """Run summation calculation"""
    retval = None
    values = [a[b] for a in calc_list for b in a if b == "PART_TO_BE_SUMMED"]
    if len(values) > 0:
        retval = sum([float(a) for a in values])
    return retval

def get_part_whole_of_difference(calc_list):
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

def get_compute_order(graph):
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
        visited = dfs(graph, start, visited, 0)
    dependency_list = [{k:v} for v, k in sorted([(v, k) for k, v in visited.items()], reverse=True)]
    return dependency_list

def compare_dicts(src, dest, tolerance=.00001):
    """Do a shallow diff of values in a dict. Numeric differences can fall within a \
    tolerance"""
    src = {int(a): src[a] for a in src}
    dest = {int(a): dest[a] for a in dest}
    insertions = {a: (None, dest[a]) for a in dest if a not in src}
    deletions = {a: (src[a], None) for a in src if a not in dest}
    matches = {a: (src[a], dest[a]) for a in src if a in dest and dest[a] != None and \
                abs(float(src[a])-float(dest[a])) < tolerance}
    mismatches = {a: (src[a], dest[a])  for a in src if a in dest and (dest[a] == None or \
                    abs(float(src[a])-float(dest[a])) > tolerance)}
    return {'insert': insertions, 'delete': deletions, 'match': matches, \
            'mismatch': mismatches}

def compare_data(current_data, target_data, campaign_id, region_id):
    """Perform diff of target and current data for a camapign and region"""
    sys.stderr.write("Diffing...\n")
    diff_output = compare_dicts(target_data, current_data)
    num_keys = sum([len(diff_output[a].keys()) for a in diff_output])
    diff_output_counts = {a: {'count':len(diff_output[a].keys()), \
                        'pct': round(float(len(diff_output[a].keys()))/num_keys, 4)}  \
                        for a in diff_output}
    #print "Diff Report for DB %s Campaign %s Region %s" % (db_host, campaign_id, region_id)
    #print "COUNTS"
    #pp.pprint(diff_output_counts)
    #print "DETAILS"
    #pp.pprint(diff_output)
    return {'campaign_id': campaign_id, 'counts': diff_output_counts, 'details': diff_output}

def evaluate_data(cursor, output_dict, campaign_id, region_id):
    """Kicks off comparison process for target and current data from abstracted table"""
    target_data = {a['indicator_id']: a['value'] for a in output_dict[region_id].values()}
    sys.stderr.write("Loading abstracted from db...\n")
    current_data = get_abstracted_data(cursor, campaign_id, region_id)
    if current_data:
        return compare_data(current_data, target_data, campaign_id, region_id)
    else:
        return None

def output_target_data(output_dict):
    """Print out target data as python object"""
    sys.stderr.write("outputting target data...\n")
    target_data = [b for a in output_dict for b in output_dict[a].values()]
    pp.pprint(target_data)

def output_target_data_csv(output_dict, keys):
    """Output all calc and agg data as csv"""
    sys.stderr.write("outputting target data as csv...\n")
    target_data = [b for a in output_dict for b in output_dict[a].values()]
    dict_writer = csv.DictWriter(sys.stdout, keys)
    dict_writer.writeheader()
    dict_writer.writerows(target_data)

def output_target_data_csv_natreg(output_dict, file, keys, region_id, region_graph):
    """Output agg and calc data as a csv for region at country and region level only"""
    sys.stderr.write("outputting natreg target data as csv...\n")
    regions = region_graph[region_id].keys()
    regions.append(region_id)
    sys.stderr.write("Filtering by regions:"+str(regions)+"\n")
    target_data = [b for a in regions for b in output_dict[a].values()]
    dict_writer = csv.DictWriter(open(file, "w"), keys)
    dict_writer.writeheader()
    dict_writer.writerows(target_data)

def report_data_presence(output_dict, region_order):
    """Mine data for deepest region where datapoints exist for a campaign"""
    sys.stderr.write("Finding depth of campaign indicators...\n")
    region_order_dict = {b:a[b] for a in region_order for b in a}
    deepest_indicators = dict()
    for region in output_dict:
        for indicator in output_dict[region]:
            ind_depth = region_order_dict[region]
            if indicator not in deepest_indicators:
                deepest_indicators[indicator] = ind_depth
            elif deepest_indicators[indicator] < ind_depth:
                deepest_indicators[indicator] = ind_depth
    return deepest_indicators

def load_test_data():
    """Basic test cases for validating aggregations and calculations"""
    computed_indicators = [{'indicator_id': 99, 'indicator_component_id': 100, \
                                                    'calculation': 'PART'},
                           {'indicator_id': 99, 'indicator_component_id': 101, \
                           'calculation': 'WHOLE'},
                           {'indicator_id': 102, 'indicator_component_id': 99, \
                            'calculation': 'PART_TO_BE_SUMMED'},
                           {'indicator_id': 102, 'indicator_component_id': 103, \
                            'calculation': 'PART_TO_BE_SUMMED'},
                           {'indicator_id': 106, 'indicator_component_id': 99, \
                           'calculation': 'PART'},
                           {'indicator_id': 106, 'indicator_component_id': 102, \
                           'calculation': 'WHOLE'},
                           {'indicator_id': 107, 'indicator_component_id': 100, \
                           'calculation': 'PART_OF_DIFFERENCE'},
                           {'indicator_id': 107, 'indicator_component_id': 6, \
                           'calculation': 'WHOLE_OF_DIFFERENCE'},
                           {'indicator_id': 107, 'indicator_component_id': 6, \
                           'calculation': 'WHOLE_OF_DIFFERENCE_DENOMINATOR'}]
    regions = [{'id': 1, 'office_id': 1, 'name': 1, 'parent_region_id': 4},
               {'id': 2, 'office_id': 1, 'name': 2, 'parent_region_id': 1},
               {'id': 3, 'office_id': 1, 'name': 3, 'parent_region_id': 1},
               {'id': 4, 'office_id': 1, 'name': 4, 'parent_region_id': None}]
    datapoints = [{'region_id': 1, 'indicator_id': 5, 'value': 19, 'campaign_id': 111},
                  {'region_id': 2, 'indicator_id': 5, 'value': 4, 'campaign_id': 111},
                  {'region_id': 2, 'indicator_id': 100, 'value': 3, 'campaign_id': 111},
                  {'region_id': 2, 'indicator_id': 101, 'value': 4, 'campaign_id': 111},
                  {'region_id': 2, 'indicator_id': 103, 'value': 2, 'campaign_id': 111},
                  {'region_id': 3, 'indicator_id': 5, 'value': 7, 'campaign_id': 111},
                  {'region_id': 3, 'indicator_id': 6, 'value': 17, 'campaign_id': 111}]
    return (computed_indicators, regions, datapoints)

def load_calc_agg_db_data(cursor):
    """Load initial data for running agg and calc for a campaign"""
    global GLOBAL_CACHE
    sys.stderr.write("Connected to " +db_host+"\n")
    sys.stderr.write("Loading calc models from db...\n")
    if "computed_indicators" not in GLOBAL_CACHE:
        GLOBAL_CACHE['computed_indicators'] = get_computed_indicators(cursor)
        sys.stderr.write("Loading regions from db...\n")
        GLOBAL_CACHE['regions'] = get_regions(cursor)
    return (GLOBAL_CACHE['computed_indicators'], GLOBAL_CACHE['regions'])

def make_agg_calc_derived_metadata(computed_indicators, regions):
    """Derive metadata for running agg and calc for a campaign"""
    global GLOBAL_CACHE
    sys.stderr.write("Prepping for calcs...\n")
    if "calc_graph" not in GLOBAL_CACHE:
        GLOBAL_CACHE['calc_graph'] = make_calc_graph(computed_indicators)
        GLOBAL_CACHE['calc_row_dict'] = make_calc_dict(computed_indicators)
        GLOBAL_CACHE['calc_order'] = get_compute_order(GLOBAL_CACHE['calc_graph'])
        GLOBAL_CACHE['region_graph'] = make_region_graph(regions)
        GLOBAL_CACHE['region_order'] = get_compute_order(GLOBAL_CACHE['region_graph'])
    return (GLOBAL_CACHE['calc_row_dict'],
            GLOBAL_CACHE['calc_order'], GLOBAL_CACHE['region_graph'],
            GLOBAL_CACHE['region_order'])

def run_engine_prereqs(cursor):
    sys.stderr.write("Running engine prereqs so that data is pre cached")
    (computed_indicators, regions) = load_calc_agg_db_data(cursor)
    (calc_row_dict, calc_order, region_graph, region_order) = \
        make_agg_calc_derived_metadata(computed_indicators, regions)

def run_engine(cursor, campaign_id, test_mode):
    """Run the calc and agg engine for a campaign"""
    if test_mode == 1:
        (computed_indicators, regions, datapoints) = load_test_data()
    else:
        (computed_indicators, regions) = load_calc_agg_db_data(cursor)
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

def run_engine_for_diff(cursor, campaign_id, region_id, test_mode):
    """Run mode for doing a diff between current and target data"""
    sys.stderr.write("== Campaign %s ==\n" % (campaign_id))
    (output_dict, region_graph, region_order) = run_engine(cursor, campaign_id, test_mode)
    return evaluate_data(cursor, output_dict, campaign_id, region_id)

def run_engine_for_target_csv(cursor, campaign_id, region_id, test_mode):
    """Run mode for outputting target data"""
    sys.stderr.write("== Campaign %s ==\n" % (campaign_id))
    (output_dict, region_graph, region_order) = run_engine(cursor, campaign_id, test_mode)
    keys=['value','indicator_id','campaign_id','region_id']
    file=str(campaign_id) + "_target_natreg.csv"
    output_target_data_csv_natreg(output_dict, file, keys, region_id, region_graph)

def run_engine_for_data_depth(cursor, campaign_id, test_mode):
    """Run mode for examining data depth"""
    (output_dict, region_graph, region_order) = run_engine(cursor, campaign_id, test_mode)
    return report_data_presence(output_dict, region_order)

def run_engine_for_parallel_calcs(campaign_id, test_mode):
    """Run mode for simply calculating"""
    conn = psycopg2.connect("host = 'localhost' port = " + str(forwarded_port) + \
                            " dbname = 'polio' user = 'djangoapp' password = 'w3b@p01i0'")
    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    print "REC cursor", cursor
    (output_dict, region_graph, region_order) = run_engine(cursor, campaign_id, test_mode)
    with open("camp_"+str(campaign_id) + "_py_output.txt", 'wt') as out:
        pprint.pprint(output_dict, stream=out)
    return campaign_id

def run_engine_for_parallel_diff(campaign_id, region_id, test_mode):
    """Run mode for doing a diff between current and target data"""
    conn = psycopg2.connect("host = 'localhost' port = " + str(forwarded_port) + \
                            " dbname = 'polio' user = 'djangoapp' password = 'w3b@p01i0'")
    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    sys.stderr.write("== Campaign %s ==\n" % (campaign_id))
    (output_dict, region_graph, region_order) = run_engine(cursor, campaign_id, test_mode)
    return evaluate_data(cursor, output_dict, campaign_id, region_id)

def run_engine_for_parallel_natreg_csv(campaign_id, region_id, test_mode):
    """Run mode for outputting target data"""
    conn = psycopg2.connect("host = 'localhost' port = " + str(forwarded_port) + \
                            " dbname = 'polio' user = 'djangoapp' password = 'w3b@p01i0'")
    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    sys.stderr.write("== Campaign %s ==\n" % (campaign_id))
    (output_dict, region_graph, region_order) = run_engine(cursor, campaign_id, test_mode)
    keys=['value','indicator_id','campaign_id','region_id']
    file=str(campaign_id) + "_target_natreg.csv"
    output_target_data_csv_natreg(output_dict, file, keys, region_id, region_graph)

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--save-graph', dest='filename',
                        help='Write the graph as JSON to a file')

    args = parser.parse_args()
    pp = pprint.PrettyPrinter(indent=4)

    #PROD SETTINGS
    db_host = "54.173.197.157"
    forwarded_port = 8801

    # DEV SETTINGS
    #db_host = "uf04.seedscientific.com"
    #forwarded_port = 8800
    GLOBAL_CACHE = dict()
    _num_cores = multiprocessing.cpu_count()
    _test_mode = 0 # 1 (test mode) or 0 (non test mode)
    _cursor = None
    if _test_mode == 0:
        os.system('ssh -i ~/.ssh/awspolio.pem -f ubuntu@'+db_host+' -L ' + \
                str(forwarded_port)+ ':localhost:5432 -N')
        conn = psycopg2.connect("host = 'localhost' port = " + str(forwarded_port) + \
                            " dbname = 'polio' user = 'djangoapp' password = 'w3b@p01i0'")
        _cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        run_engine_prereqs(_cursor)
    else:
        _output_dict = run_engine(_cursor, None, _test_mode)
        pp.pprint(_output_dict)
        quit()

    # list of campaigns to run engine for basic data validation at country level
    campaigns = [{'campaign_id': 111, 'office_id':1},{'campaign_id': 139, 'office_id':2},{'campaign_id': 174, 'office_id':3}]
    office_regions=[12907,12908,12909]

    #use this for parallel processing
    campaigns = get_campaigns(_cursor)
    start=time.time()

    # Simply run and output calc engine
    #output_array=Parallel(n_jobs=_num_cores)(delayed(run_engine_for_parallel_calcs)(i['campaign_id'],_test_mode) for i in campaigns)

    # Generate national/regional level data for campaigns
    output_array=Parallel(n_jobs=_num_cores)(delayed(run_engine_for_parallel_natreg_csv)(c['campaign_id'], office_regions[int(c['office_id'])-1], _test_mode) for c in campaigns)

    #Perform diff for campaigns with abstracted table
    #output_array=Parallel(n_jobs=_num_cores)(delayed(run_engine_for_parallel_diff)(c['campaign_id'], office_regions[int(c['office_id'])-1], _test_mode) for c in campaigns)
    #campaign_diffs = {x['campaign_id']: x for x in output_array}
    #print "from decimal import Decimal\ndiff_dict =",campaign_diffs
    end=time.time()
    sys.stderr.write("Elapsed "+ str(end-start))

    #Use this if mining for maximum data depth
    #campaigns = get_campaigns(_cursor)
    #campaign_ind_depth = dict()
    #for c in campaigns:
    #    campaign_ind_depth[c['campaign_id']] = run_engine_for_data_depth(_cursor, c['campaign_id'],                                                       _test_mode)
    #print 'campaign_depths =',campaign_ind_depth
    # After this step, output data to variable called campaign_depths on a file called
    # ind_depth_data. Then run script output_ind_depths.py to output csv
