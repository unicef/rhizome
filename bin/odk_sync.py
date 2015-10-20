#!/usr/bin/env python
import csv
import json
import urllib2, urllib
import httplib
import subprocess
import base64

from datetime import datetime
from urllib2 import Request, urlopen
from urllib import urlencode
from pprint import pprint
import requests


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
            #  post_file_data(document_id, csv_base_64, str(form_name))
             refresh_file_data(document_id)

def post_file_data(document_id, base_64_data, doc_title):

    print 'POSTING FILE DATA'
    data =  json.dumps({\
        'id':document_id,
        'docfile':base_64_data,
        'doc_title':doc_title
    })

    headers = {'content-type': 'application/json'}

    url = 'http://localhost:8000/api/v1/source_doc/?username=%s&api_key=%s' % \
        (RHIZOME_USERNAME, RHIZOME_KEY)

    r = requests.post(url,data=data,headers=headers)

    print 'THIS IS WHERE I AM NOW'

    r.close()

def refresh_file_data(document_id):

    filters = {
        'document_id': document_id,
        'username': RHIZOME_USERNAME,
        'api_key': RHIZOME_KEY,
    }

    query_string = 'transform_upload/?' + urlencode(filters)
    data = query_api(query_string)

    print data[0]

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
