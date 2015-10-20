#!/usr/bin/env python
import csv
import json
import urllib2
import subprocess
import base64

from datetime import datetime
from urllib2 import Request, urlopen
from urllib import urlencode
from pprint import pprint


def main():
    '''
    Pull 2015 for Top Level Regions and Save as a CSV...
    '''

    forms_to_process = get_forms_to_process()
    for form_name,document_id in forms_to_process.iteritems():

        # subprocess.call(['java','-jar',JAR_FILE,\
        #     '--form_id', form_name, \
        #     '--export_filename',form_name +'.csv', \
        #     '--aggregate_url',AGGREGATE_URL, \
        #     '--storage_directory',STORAGE_DIRECTORY, \
        #     '--export_directory',EXPORT_DIRECTORY, \
        #     '--odk_username',ODK_USER, \
        #     '--odk_password',ODK_PASS, \
        #     '--overwrite_csv_export' ,\
        #     '--exclude_media_export' \
        #   ])

        csv_file = EXPORT_DIRECTORY + str(form_name) + '.csv'
        with open(csv_file, 'rb') as full_file:
             csv_base_64 = base64.b64encode(full_file.read())
             post_file_data(document_id, csv_base_64)

def post_file_data(document_id, base_64_data):


    url = 'http://localhost:8000/api/source_doc/'

    method = 'POST'
    post_data = json.dumps({'document_id':document_id,'docfile':base_64_data})
    handler = urllib2.HTTPHandler()
    opener = urllib2.build_opener(handler)
    request = urllib2.Request(url, data=post_data)


    print 'request\n' * 5
    print request

    request.add_header("Content-Type",'application/json')
    request.get_method = lambda: method

    try:
        connection = opener.open(request)
    except urllib2.HTTPError,e:
        connection = e


    if connection.code == 200:
        data = connection.read()

def get_forms_to_process():
    '''
    '''

    forms_to_process = {}

    filters = {
        'doc_detail_type': 'odk_form_name',
        'username': RHIZOME_USERNAME,
        'api_key': RHIZOME_KEY,
        # 'cron_guid':UUID,
    }

    query_string = 'doc_detail/?' + urlencode(filters)
    data = query_api(query_string)

    for result in data:
        forms_to_process[result[u'doc_detail_value']] = result[u'document_id']

    return forms_to_process

def query_api(query_string):

    HOST = 'http://localhost:8000/api/v1/'

    url = HOST + query_string

    print '=== HITTING API %s === '% url
    response = urlopen(url)
    objects = json.loads(response.read())['objects']

    return objects

if __name__ == "__main__":
    main()
