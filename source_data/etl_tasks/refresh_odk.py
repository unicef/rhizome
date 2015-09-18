#!/usr/cat /hom bin/python

import sys
import json
import urllib2
import subprocess
from time import sleep
from urllib import urlencode
from uuid import uuid4


try:
    sys.path.append("/Users/johndingee_seed/Desktop/")
    import odk_settings
except ImportError:
    sys.path.append("/home/ubuntu/ODK/")
    import odk_settings


class ODKRefreshTask(object):

    def __init__(self):

        self.base_url_string = odk_settings.API_ROOT
        self.cron_guid = uuid4()


    def main(self):

        ## NOT INTEGRATING locationS FOR A WHILE - NEED VALIDATION ON CURRENT
          ## STRUCTURE AS WELL AS WAY TO MOVE FORWARD WITH MAPPING ##

        # pull_locations(base_url_string)
        # refresh_locations(base_url_string)

        forms_to_process = self.get_forms_to_process()

        for form in forms_to_process:
            print 'processing_forms: %s' % form
            form_results = self.process_odk_form(form)


    def api_wrapper(self,kwargs=None):

        kwargs['job_id'] = self.cron_guid
        url_string = self.base_url_string + '?' + urlencode(dict(**kwargs))
        response = urllib2.urlopen(url_string)#
        etl_api_response = json.loads(response.read())['objects'][0]

        return etl_api_response

    def pull_locations(self):

        location_FORM="VCM_Sett_Coordinates_1.2"

        # START ODK JAR FILE #
        self.api_wrapper({'task':'start_odk_jar','form_name':location_FORM})

        # PULL ODK DATA #
        sleep(2)
        self.pull_odk_form_data(location_FORM)
        sleep(2)

        # DONE WITH ODK JAR FILE #
        self.api_wrapper({'task':'finish_odk_jar','form_name':location_FORM})


    def pull_odk_form_data(self, form):

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


    def refresh_locations(base_url_string):

        etl_api_response = self.api_wrapper({'task':'ingest_odk_locations'})

    def get_forms_to_process(self):

        etl_api_response = self.api_wrapper({'task':'get_odk_forms_to_process'})
        form_list_response = etl_api_response['success_msg']

        ## having trouble deserializing json here.. hack alert ##
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

        ######################################################
        ## FIRST PULL THE ODK DATA FROM THE AGGREGAT SERVER ##
        ######################################################

        ## BEGIN DATA DOWNLOAD FROM ODK ##
        form_ingest_response = self.api_wrapper\
            ({'task':'start_odk_jar','form':form})

        self.pull_odk_form_data(form)

        ## END DATA DOWNLOAD FROM ODK ##
        form_ingest_response = self.api_wrapper\
            ({'task':'finish_odk_jar','form':form})

        #####################################################
        ## NOW TRANSFORM THE ODK DATA TO OUR NATIVE SCHEMA ##
        #####################################################

        form_ingest_response = self.api_wrapper\
            ({'task':'odk_transform','form_name':form})
        form_ingest_result = form_ingest_response['success_msg']

        return form_ingest_result


if __name__ == "__main__":
  ort = ODKRefreshTask()
  ort.main()
