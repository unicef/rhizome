#!/usr/bin/env python
import csv
import json
import psycopg2
import time
import urllib2

from datetime import datetime
from urllib2 import Request, urlopen
from urllib import urlencode
from pprint import pprint

def main():
    '''
    Pull 2015 for Top Level Regions and Save as a CSV...
    '''

    location_id = get_location()
    indicator_id_list = get_indicators()
    all_data = get_datapoints(location_id,indicator_id_list)

def get_location():
    '''
    Customize this based on what campaigns, regions and indicators you want.
    '''

    filters = {
        'parent_location_id': -1,
    }

    query_string = 'location/?' + urlencode(filters)
    data = query_api(query_string)
    location_id = data[-1][u'id']

    return location_id

def get_indicators():
    '''
    '''

    filters = {
        'name__startswith': 'ODK',
    }

    query_string = 'indicator/?' + urlencode(filters)
    data = query_api(query_string)
    indicator_ids = [unicode(indicator[u'id']) for indicator in data]

    return indicator_ids

def get_datapoints(location_id,indicator_id_list):
    '''
    Get all indicator data for location/campaign combo
    '''
    filters = {
        'location__in': location_id,
        'indicator__in': ",".join(indicator_id_list),
        'campaign_start': '2015-01-01',
    }

    query_string = 'datapoint/?' + urlencode(filters)
    data = query_api(query_string)

    for row in data:
        print row


def query_api(query_string):

    HOST = 'http://rhizome.work/api/v1/'

    auth = {
        'username': '', ## FILL ME IN
        'api_key': '' ## FILL ME IN !
    }

    url = HOST + query_string + '&' + urlencode(auth)

    response = urlopen(url)
    objects = json.loads(response.read())['objects']

    return objects

if __name__ == "__main__":
    main()
