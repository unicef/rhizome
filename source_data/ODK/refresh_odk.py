#!/bin/python

import sys
import urllib2

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

    start_odk_jar_url_string = base_url_string + '&task=start_odk_jar'

    response = urllib2.urlopen(start_odk_jar_url_string, data=None)
    print response.read()#data

    # "${API_ROOT}?task=start_odk_jar&username=${POLIO_USERNAME}&api_key=${POLIO_KEY}&cron_guid=${UUID}"


    # wget -O/dev/null "${API_ROOT}?task=start_odk_jar&username=${POLIO_USERNAME}&api_key=${POLIO_KEY}&cron_guid=${UUID}"
    #
    # for FORM in "${FORMS[@]}";
    #  do
    #    echo $FORM
    #     java -jar $JAR_FILE \
    #      --form_id $FORM \
    #      --export_filename $FORM \
    #      --aggregate_url $AGGREGATE_URL \
    #      --storage_directory $STORAGE_DIRECTORY \
    #      --export_directory $EXPORT_DIRECTORY \
    #      --odk_username $ODK_USER admin \
    #      --odk_password $ODK_PASS P@ssword \
    #      --exclude_media_export;
    # done
    #
    # sleep 2
    # # DONE WITH ODK JAR FILE #
    # wget -O/dev/null "${API_ROOT}?task=finish_odk_jar&username=${POLIO_USERNAME}&api_key=${POLIO_KEY}&cron_guid=${UUID}"
    #
    # sleep 2
    #
    # # DONE WITH ODK JAR FILE #
    # wget -O/dev/null "${API_ROOT}?task=ingest_odk_regions&username=${POLIO_USERNAME}&api_key=${POLIO_KEY}&cron_guid=${UUID}"


if __name__ == "__main__":
  main()
