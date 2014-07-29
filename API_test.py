import ast
import json
import urllib2
import pprint as pp
import requests
import sys

ENDPOINT = 'http://127.0.0.1:8000/api/v1/datapoint/'
USERNAME = 'john'
API_KEY  = '3018e5d944e1a37d2e2af952198bef4ab0d9f9fc'

def test_datapoint_POST(self):

    data = '{"indicator": "8","region": "6"}'

    payload = ast.literal_eval(data)
    url = ENDPOINT + '?username=' + USERNAME + '&api_key=' + API_KEY
    headers = {'content-type': 'application/json'}

    r = requests.post(url, data=json.dumps(payload), headers=headers)

    print r.status_code

    ## now look this up in the database



def test_datapoint_GET(self):

    url = ENDPOINT + '?username=' + USERNAME + '&api_key=' + API_KEY
    response = requests.get(url)

    status_code = response.status_code
    data = response.text

    return status_code, data


## TO RUN THIS:
# coverage run manage.py test  datapoints.api --settings=polio.settings_test
