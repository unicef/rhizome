import ast
import json
import urllib2
import pprint as pp
import requests
import sys
from datapoints.models import Indicator
from django.test import TestCase

ENDPOINT = 'http://127.0.0.1:8000/api/v1/indicator/'
USERNAME = 'john'
API_KEY  = '3018e5d944e1a37d2e2af952198bef4ab0d9f9fc'

class IndicatorTest(TestCase):

    def test_indicator_POST(self):

        data = '{"name": "this is a testxyzHALLA","description": "this is a test"}'

        payload = ast.literal_eval(data)
        url = ENDPOINT + '?username=' + USERNAME + '&api_key=' + API_KEY
        headers = {'content-type': 'application/json'}

        r = requests.post(url, data=json.dumps(payload), headers=headers)

        print r.status_code

        ## now look this up in the database

        posted_name = payload['name']

        # i = Indicator.objects.get(name=posted_name)

        print
        i = Indicator.objects.all()
        print i

        # print posted_name


    def test_indicator_GET(self):

        url = ENDPOINT + '?username=' + USERNAME + '&api_key=' + API_KEY
        response = requests.get(url)

        status_code = response.status_code
        data = response.text

        return status_code, data

    def do_something():
        print 'hello'

## TO RUN THIS:
# coverage run manage.py test  datapoints.api --settings=polio.settings_test
