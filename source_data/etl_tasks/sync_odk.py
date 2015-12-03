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
# import requests

from django.conf import settings


class OdkSync(object):

    def __init__(self,odk_form_name=None, *args, **kwargs):

        self.odk_form_name = odk_form_name
        self.odk_settings = settings.ODK_SETTINGS


    def main(self):
        '''
        '''

        forms_to_process = self.get_forms_to_process()
        for form_name,document_id in forms_to_process.iteritems():

            subprocess.call(['java','-jar',self.odk_settings['JAR_FILE'],\
                '--form_id', form_name, \
                '--export_filename',form_name +'.csv', \
                '--aggregate_url',self.odk_settings['AGGREGATE_URL'], \
                '--storage_directory',self.odk_settings['STORAGE_DIRECTORY'], \
                '--export_directory',self.odk_settings['EXPORT_DIRECTORY'], \
                '--odk_username',self.odk_settings['ODK_USER'], \
                '--odk_password',self.odk_settings['ODK_PASS'], \
                '--overwrite_csv_export' ,\
                '--exclude_media_export' \
              ])

            csv_file = self.odk_settings['EXPORT_DIRECTORY'] + str(form_name) + '.csv'
            with open(csv_file, 'rb') as full_file:
                 csv_base_64 = base64.b64encode(full_file.read())
                #  post_file_data(document_id, csv_base_64, str(form_name))
                 output_data = refresh_file_data(document_id)

    # def post_file_data(document_id, base_64_data, doc_title):
    #
    #     data =  json.dumps({\
    #         'id':document_id,
    #         'docfile':base_64_data,
    #         'doc_title':doc_title
    #     })
    #
    #     headers = {'content-type': 'application/json'}
    #
    #     url = odk_settings.API_ROOT + 'source_doc/?username=%s&api_key=%s' % \
    #         (odk_settings.RHIZOME_USERNAME, odk_settings.RHIZOME_KEY)
    #
    #     r = requests.post(url,data=data,headers=headers)
    #     r.close()

    def refresh_file_data(document_id):

        filters = {
            'document_id': document_id,
            'username': self.odk_settings['RHIZOME_USERNAME'],
            'api_key': self.odk_settings['RHIZOME_KEY'],
        }

        query_string = odk_settings.API_ROOT + 'transform_upload/?' + urlencode(filters)
        data = self.query_api(query_string)

        return data

    def get_forms_to_process(self):
        '''
        '''

        if self.odk_form_name:
            return {self.odk_form_name : None}
            # {u'vcm_birth_tracking': 66, u'vcm_register': 10}

        forms_to_process = {}

        filters = {
            'doc_detail_type': 'odk_form_name',
            'username': self.odk_settings['RHIZOME_USERNAME'],
            'api_key': self.odk_settings['RHIZOME_KEY'],
        }

        query_string = self.odk_settings['API_ROOT'] + 'doc_detail/?' + urlencode(filters)
        data = self.query_api(query_string)

        for result in data:
            forms_to_process[result[u'doc_detail_value']] = result[u'document_id']

        print '=='
        print forms_to_process
        print '=='

        return forms_to_process

    def query_api(self, query_string):

        response = urlopen(query_string)
        objects = json.loads(response.read())['objects']

        return objects
