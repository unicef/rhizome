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

    REGION_FORM="VCM_Sett_Coordinates_1.2"
    # UUID=$(uuidgen)

    base_url_string = '%s?username=%s&api_key=%s' % (odk_settings.API_ROOT, \
        odk_settings.POLIO_USERNAME, odk_settings.POLIO_KEY)

    start_odk_jar_url_string = base_url_string + '&task=start_odk_jar&form_name=' + REGION_FORM

    response = urllib2.urlopen(start_odk_jar_url_string, data=None)

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

    sleep(5)
    start_odk_jar_url_string = base_url_string + '&task=finish_odk_jar&form_name=' + REGION_FORM

    # # DONE WITH ODK JAR FILE #
    # wget -O/dev/null "${API_ROOT}?task=finish_odk_jar&username=${POLIO_USERNAME}&api_key=${POLIO_KEY}&cron_guid=${UUID}"
    #
    # sleep 2
    #
    # # DONE WITH ODK JAR FILE #
    # wget -O/dev/null "${API_ROOT}?task=ingest_odk_regions&username=${POLIO_USERNAME}&api_key=${POLIO_KEY}&cron_guid=${UUID}"


if __name__ == "__main__":
  main()
