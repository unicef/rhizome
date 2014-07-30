import ast
import json
import urllib2
import pprint as pp
import requests
import sys

ENDPOINT = 'http://127.0.0.1:8000/api/v1/datapoint/'
USERNAME = 'john'
API_KEY  = '3018e5d944e1a37d2e2af952198bef4ab0d9f9fc'

    ##############
      
    ##############

def test_datapoint_POST():

    data = '{"indicator": "/api/v1/indicator/48/" \
    ,"region": "/api/v1/region/9/" \
    ,"campaign": "/api/v1/campaign/1/" \
    ,"value": "1.00" \
    ,"changed_by_id": "/api/v1/user/1/"}'

  # header: application/json
  # URL : http://127.0.0.1:8000/api/v1/datapoint/?username=john&
    # api_key=3018e5d944e1a37d2e2af952198bef4ab0d9f9fc


    payload = ast.literal_eval(data)
    url = ENDPOINT + '?username=' + USERNAME + '&api_key=' + API_KEY
    headers = {'content-type': 'application/json'}

    r = requests.post(url, data=json.dumps(payload), headers=headers)

    print r.status_code

    ## now look this up in the database to make sure it got inserted


def test_datapoint_GET():

    url = ENDPOINT + '?username=' + USERNAME + '&api_key=' + API_KEY
    response = requests.get(url)

    status_code = response.status_code
    data = response.text

    print data
    # return status_code, data

    ################
    ## INDICATORS ##
    ################


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


## TO RUN THIS:
# coverage run manage.py test  datapoints.api --settings=polio.settings_test



if __name__ == "__main__":
      test_datapoint_GET()
