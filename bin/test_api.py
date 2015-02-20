# How to use:
# python test_api.py <API url base>
# If no <API url base> is not included, it defaults to http://localhost:8000/
# currently tests /initialize/ and /drivedata/ with all of the signals (no filters or segments yet)
import sys
import json
import urllib2
from pprint import pprint
from pandas import read_csv

api_suffix = "api/v1/"
api_url = "http://localhost:8000/"

if len(sys.argv) > 1:
    api_url = sys.argv[1]

api_url += api_suffix

print "****************\nTesting API: %s\n****************\n\n" % api_url

def test_url(url, target_value):

    response = None
    passed = True

    # HTTP test
    try:
        response = urllib2.urlopen(url)
    except urllib2.HTTPError, e:
        print "HTTP Error: %s %s" % (str(e.code), str(e.reason))
        passed = False

    # test JSON parsing
    try:
        response =  json.load(response)
    except:
        print "Error parsing JSON"
        passed = False

    if response is not None:

        # parse_value #
        try:
            response_value = response["objects"]#[0]["indicators"][0]["value"]
            print response_value
            print target_value
        except Exception as err:
            print err
            passed = False
            return None

        if target_value == response_value:
            passed = True

    if passed is True:
        print "Passed test"
        return response
    else:
        return None


def test_nco_dash():

    ng_dash_df = read_csv('/Users/johndingee_seed/code/UF04/polio/datapoints/tests/_data/ngo_dash.csv')
    campaign_id = 100

    signals_passed = 0

    for row_ix, row_data in ng_dash_df.iterrows():

        if row_data.indicator_id == 264:
            url_string = "http://localhost:8000/api/v1/datapoint/?indicator__in=%s&region__in=%s&campaign__in=%s" % (row_data.indicator_id,row_data.region_id\
                ,campaign_id)

            if test_url(url_string,row_data.value):

                signals_passed += 1

            print "\n\n****************** Passed %d out of %d signal tests" % (signals_passed, len(ng_dash_df))


if __name__ == "__main__":
    print 'hello'
    test_nco_dash()
