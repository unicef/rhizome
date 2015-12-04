#!/usr/bin/env python
import csv
import json
import urllib2, urllib
import httplib
from subprocess import Popen, PIPE
import base64
from datetime import datetime
from urllib2 import Request, urlopen
from urllib import urlencode

from django.core.files.base import ContentFile
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings

from source_data.models import Document

class OdkJarFileException(Exception):
    # defaultMessage = "Sorry, this request could not be processed."
    # defaultCode = -1

    def __init__(self, message, *args, **kwargs):


        print '===\n' * 3
        print message
        print '===\n' * 3

        java_message = message[message.index("SEVERE:"):]
        self.errorMessage = java_message + '...... ' + kwargs['odk_form_name']

        ## for more infomration see here:
        # <my aggregate url > Aggregate.html#management/forms///

class OdkSync(object):

    def __init__(self,odk_form_name=None, *args, **kwargs):

        self.odk_form_name = odk_form_name
        self.odk_settings = settings.ODK_SETTINGS
        self.user_id = kwargs['user_id']
        self.sync_result_data = {}

    def main(self):
        '''
        '''

        forms_to_process = self.get_forms_to_process()
        for form_name,document_id in forms_to_process.iteritems():

            procedure = Popen(['java','-jar',self.odk_settings['JAR_FILE'],\
                    '--form_id', form_name, \
                    '--export_filename',form_name +'.csv', \
                    '--aggregate_url',self.odk_settings['AGGREGATE_URL'], \
                    '--storage_directory',self.odk_settings['STORAGE_DIRECTORY'], \
                    '--export_directory',self.odk_settings['EXPORT_DIRECTORY'], \
                    '--odk_username',self.odk_settings['ODK_USER'], \
                    '--odk_password',self.odk_settings['ODK_PASS'], \
                    '--overwrite_csv_export' ,\
                    '--exclude_media_export' \
                  ], stdout=PIPE, stderr=PIPE)

            out, err = procedure.communicate()
            exitcode = procedure.returncode

            # if exitcode == 0:
            if 'SEVERE:' in err:
                error_details = {'odk_form_name':form_name}
                raise OdkJarFileException(err, **error_details)

            csv_file = self.odk_settings['EXPORT_DIRECTORY'] + form_name.replace('-','_') + '.csv'
            with open(csv_file, 'rb') as full_file:
                 csv_base_64 = base64.b64encode(full_file.read())
                 self.post_file_data(document_id, csv_base_64, str(form_name))
                 # output_data = self.refresh_file_data(document_id)

        return document_id, self.sync_result_data

    def post_file_data(self, document_id, base_64_data, doc_title):

        file_content = ContentFile(base64.b64decode(base_64_data))
        sd, created = Document.objects.update_or_create(
            id=document_id,
            defaults={'doc_title': doc_title, 'created_by_id': self.user_id}
        )

        sd.docfile.save(sd.guid, file_content)


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

            try:
                doc_id = Document.objects.get(doc_title=self.odk_form_name).id
            except ObjectDoesNotExist:
                doc_id = None

            return {self.odk_form_name : doc_id}
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

        return forms_to_process

    def query_api(self, query_string):

        response = urlopen(query_string)
        objects = json.loads(response.read())['objects']

        return objects
