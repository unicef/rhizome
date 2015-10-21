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
import requests

import odk_settings

def main():
    '''
    '''

    forms_to_process = get_forms_to_process()
    for form_name,document_id in forms_to_process.iteritems():

        subprocess.call(['java','-jar',odk_settings.JAR_FILE,\
            '--form_id', form_name, \
            '--export_filename',form_name +'.csv', \
            '--aggregate_url',odk_settings.AGGREGATE_URL, \
            '--storage_directory',odk_settings.STORAGE_DIRECTORY, \
            '--export_directory',odk_settings.EXPORT_DIRECTORY, \
            '--odk_username',odk_settings.ODK_USER, \
            '--odk_password',odk_settings.ODK_PASS, \
            '--overwrite_csv_export' ,\
            '--exclude_media_export' \
          ])

        csv_file = odk_settings.EXPORT_DIRECTORY + str(form_name) + '.csv'
        with open(csv_file, 'rb') as full_file:
             csv_base_64 = base64.b64encode(full_file.read())
             post_file_data(document_id, csv_base_64, str(form_name))
             output_data = refresh_file_data(document_id)

def post_file_data(document_id, base_64_data, doc_title):

    data =  json.dumps({\
        'id':document_id,
        'docfile':base_64_data,
        'doc_title':doc_title
    })

    headers = {'content-type': 'application/json'}

    url = odk_settings.API_ROOT + 'source_doc/?username=%s&api_key=%s' % \
        (odk_settings.RHIZOME_USERNAME, odk_settings.RHIZOME_KEY)

    r = requests.post(url,data=data,headers=headers)
    r.close()

def refresh_file_data(document_id):

    filters = {
        'document_id': document_id,
        'username': odk_settings.RHIZOME_USERNAME,
        'api_key': odk_settings.RHIZOME_KEY,
    }

    query_string = odk_settings.API_ROOT + 'transform_upload/?' + urlencode(filters)
    data = query_api(query_string)

    return data

def get_forms_to_process():
    '''
    '''

    forms_to_process = {}

    filters = {
        'doc_detail_type': 'odk_form_name',
        'username': odk_settings.RHIZOME_USERNAME,
        'api_key': odk_settings.RHIZOME_KEY,
    }

    query_string = odk_settings.API_ROOT + 'doc_detail/?' + urlencode(filters)
    data = query_api(query_string)

    for result in data:
        forms_to_process[result[u'doc_detail_value']] = result[u'document_id']

    return forms_to_process

def query_api(query_string):

    response = urlopen(query_string)
    objects = json.loads(response.read())['objects']

    return objects

if __name__ == "__main__":
    main()
