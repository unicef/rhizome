#!/usr/cat /hom bin/python

import sys
import json
import urllib2
import subprocess
from time import sleep
from urllib import urlencode


try:
    sys.path.append("/Users/johndingee_seed/Desktop/")
    import odk_settings
except ImportError:
    sys.path.append("/home/ubuntu/ODK/")
    import odk_settings


class ODKRefreshTask(object):

    def __init__(self):

        self.base_url_string = odk_settings.API_ROOT

    def main(self):

        # pull_regions(base_url_string)
        # refresh_regions(base_url_string)

        forms_to_process = self.get_forms_to_process()

        for form in forms_to_process:
            print 'processing_forms: %s' % form
            # form_results = self.process_odk_form(form)


    def api_wrapper(self,kwargs=None):

        url_string = self.base_url_string + '?' + urlencode(dict(**kwargs))
        response = urllib2.urlopen(url_string)#
        etl_api_response = json.loads(response.read())['objects'][0]

        return etl_api_response

    def pull_regions(self):

        REGION_FORM="VCM_Sett_Coordinates_1.2"

        # START ODK JAR FILE #
        start_odk_jar_url_string = self.base_url_string +\
            '&task=start_odk_jar&form_name=' + REGION_FORM
        start_odk_response = urllib2.urlopen(start_odk_jar_url_string, data=None)


        # PULL ODK DATA #
        sleep(2)
        pull_odk_form_data(base_url_string,REGION_FORM)
        sleep(2)

        # DONE WITH ODK JAR FILE #
        finish_odk_jar_url_string = base_url_string + \
            '&task=finish_odk_jar&form_name=' + REGION_FORM
        finish_odk_response = urllib2.urlopen(start_odk_jar_url_string, data=None)

    def pull_odk_form_data(base_url_string,form):

        subprocess.call(['java','-jar',odk_settings.JAR_FILE,\
            '--form_id', form, \
            '--export_filename',form +'.csv', \
            '--aggregate_url',odk_settings.AGGREGATE_URL, \
            '--storage_directory',odk_settings.STORAGE_DIRECTORY, \
            '--export_directory',odk_settings.EXPORT_DIRECTORY, \
            '--odk_username',odk_settings.ODK_USER, \
            '--odk_password',odk_settings.ODK_PASS, \
            '--overwrite_csv_export' ,\
            '--exclude_media_export' \
          ])


    def refresh_regions(base_url_string):

        # START ODK JAR FILE #
        ingest_odk_url_string = base_url_string + '&task=ingest_odk_regions'
        ingest_odk_response = urllib2.urlopen(ingest_odk_url_string, data=None)

    def get_forms_to_process(self):

        url_params = {'task':'get_odk_forms_to_process'}
        etl_api_response = self.api_wrapper(url_params)
        form_list_response = etl_api_response['success_msg']

        cleaned_response_string = form_list_response.replace("['","")
        cleaned_response_string = cleaned_response_string.replace("', '",",")
        cleaned_response_string = cleaned_response_string.replace("']","")

        list_of_forms = [str(y) for y in cleaned_response_string.split(',')]

        return list_of_forms


    def process_odk_form(self,form):
        '''
        First Download the data from ODK, then ingest into source_dps and finally
        Merge what is mapped into datapoints.
        '''

        form_string = form.replace("u'","").replace("'","")

        ## DOWNLOAD DATA FROM ODK ##

        self.pull_odk_form_data(form_string)

        form_transform_kwargs = {'task':'odk_transform','form_name':form_string}
        form_ingest_response = self.api_wrapper(form_transform_kwargs)
        form_ingest_result = form_ingest_response['success_msg']



        return form_ingest_result


if __name__ == "__main__":
  # main()
  ort = ODKRefreshTask()
  ort.main()
