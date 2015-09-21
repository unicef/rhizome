#!/usr/bin/env python
import csv
import json
import psycopg2
import time
import urllib2

from datetime import datetime
from urllib2 import Request, urlopen
from urllib import urlencode

def main():
    '''
    Pull 2015 for Top Level Regions and Save as a CSV...
    '''

    location_id_list = get_locations()
    # campaign_id_list = get_campaigns(location_id_list)

    # for location_id, campaign_id in zip(location_id_list,campaign_id_list):
    #     csv_row = get_datapoints

    print objects


def get_locations():
    '''
    Customize this based on what campaigns, regions and indicators you want.
    '''

    filters = {
        'parent_location_id': -1,
    }

    query_string = 'location/?' + urlencode(filters)
    data = query_api(query_string)

    print '=='
    print data

def get_campaigns(self,location_id_list):
    '''
    Customize this based on what campaigns, regions and indicators you want.
    '''

    pass

def get_datapoints(location_id,campaign_id):
    '''
    Get all indicator data for location/campaign combo
    '''

    pass


def query_api(query_string):

    HOST = 'http://localhost:8000/api/v1/'

    auth = {
        'username': 'demo_user',
        'api_key': 'e12866a229d8dea305a681886aeaadefdd95cfa0'
    }

    url = HOST + query_string + '&' + urlencode(auth)

    print url
    response = urlopen(url)
    objects = json.loads(response.read())['objects']

    return objects

if __name__ == "__main__":
    main()

    print 'YAAAS'
