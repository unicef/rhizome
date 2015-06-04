#!/bin/python

import sys
import urllib2
import subprocess

def main():

    try:
        sys.path.append("/Users/johndingee_seed/Desktop/")
        import odk_settings as odk_settings
    except ImportError:
        sys.path.append("/home/ubuntu/ODK/")
        import odk_settings

    base_url_string = '%s?username=%s&api_key=%s' % (odk_settings.API_ROOT, \
        odk_settings.POLIO_USERNAME, odk_settings.POLIO_KEY)

    # pull_regions(base_url_string)
    refresh_regions(base_url_string)


def pull_regions(base_url_string):

    REGION_FORM="VCM_Sett_Coordinates_1.2"

    # START ODK JAR FILE #
    start_odk_jar_url_string = base_url_string +\
        '&task=start_odk_jar&form_name=' + REGION_FORM
    start_odk_response = urllib2.urlopen(start_odk_jar_url_string, data=None)

    subprocess.call(['java','-jar',odk_settings.JAR_FILE,\
        '--form_id', REGION_FORM, \
        '--export_filename',REGION_FORM +'.csv', \
        '--aggregate_url',odk_settings.AGGREGATE_URL, \
        '--storage_directory',odk_settings.STORAGE_DIRECTORY, \
        '--export_directory',odk_settings.EXPORT_DIRECTORY, \
        '--odk_username',odk_settings.ODK_USER, \
        '--odk_password',odk_settings.ODK_PASS, \
        '--overwrite_csv_export' ,\
        '--exclude_media_export' \
      ])

    # DONE WITH ODK JAR FILE #
    sleep(5)
    finish_odk_jar_url_string = base_url_string + \
        '&task=finish_odk_jar&form_name=' + REGION_FORM
    finish_odk_response = urllib2.urlopen(start_odk_jar_url_string, data=None)

def refresh_regions(base_url_string):

    # START ODK JAR FILE #
    ingest_odk_url_string = base_url_string + '&task=ingest_odk_regions'
    ingest_odk_response = urllib2.urlopen(ingest_odk_url_string, data=None)

def process_odk_datapoints(base_url_string):







if __name__ == "__main__":
  main()
