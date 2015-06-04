#!/bin/python

import sys

def main():

    try:
        sys.path.append("/Users/johndingee_seed/Desktop/")
        import odk_settings as odk_settings
    except ImportError:
        sys.path.append("/home/ubuntu/ODK/")
        import odk_settings

    print 'HELLO'

    print odk_settings.EXPORT_DIRECTORY

    # source "/Users/johndingee_seed/Desktop/odk_settings.sh" || source "/home/ubuntu/ODK/odk_settings.sh"
    #
    # # declare -a FORMS=("vcm_register" "VCM_Sett_Coordinates_1" "New_VCM_Summary")
    # declare -a FORMS=("VCM_Sett_Coordinates_1.2")
    # UUID=$(uuidgen)
    #
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
