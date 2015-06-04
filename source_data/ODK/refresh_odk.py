#!/bin/python

import sys
import json
import urllib2
import subprocess

try:
    sys.path.append("/Users/johndingee_seed/Desktop/")
    import odk_settings
except ImportError:
    sys.path.append("/home/ubuntu/ODK/")
    import odk_settings


def main():

    base_url_string = '%s?username=%s&api_key=%s' % (odk_settings.API_ROOT, \
        odk_settings.POLIO_USERNAME, odk_settings.POLIO_KEY)

    pull_regions(base_url_string)
    # refresh_regions(base_url_string)

    forms_to_process = get_forms_to_process(base_url_string)

    for form in forms_to_process:
        print 'processing_forms: %s' % form
        form_results = process_odk_form(base_url_string, form)


def pull_regions(base_url_string):

    REGION_FORM="VCM_Sett_Coordinates_1.2"

    # START ODK JAR FILE #
    start_odk_jar_url_string = base_url_string +\
        '&task=start_odk_jar&form_name=' + REGION_FORM
    start_odk_response = urllib2.urlopen(start_odk_jar_url_string, data=None)

    # PULL ODK DATA #
    pull_odk_form_data(base_url_string,REGION_FORM)

    # DONE WITH ODK JAR FILE #
    sleep(5)
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

def get_forms_to_process(base_url_string):

    get_odk_form_url_string = base_url_string + '&task=get_odk_forms_to_process'
    get_odk_form_response = urllib2.urlopen(get_odk_form_url_string, data=None)

    response_data =  json.loads(get_odk_form_response.read())

    form_list_response = response_data['objects'][0]['success_msg']

    cleaned_response = form_list_response.replace('[','').replace(']','')
    form_list = cleaned_response.split(',')

    return form_list


def process_odk_form(base_url_string,form):

    form_string = form.replace("u'","").replace("'","")

    odk_form_url_string = base_url_string + '&task=odk_transform&form_name=' + \
        form_string
    odk_form_response = urllib2.urlopen(odk_form_url_string, data=None)

    response_data =  json.loads(odk_form_response.read())

    form_ingest_result = response_data['objects'][0]['success_msg']

    return form_ingest_result


if __name__ == "__main__":
  main()
