#!/bin/sh

dir="$(dirname "$0")"
source "$dir/odk_settings.sh"

# declare -a FORMS=("vcm_register" "VCM_Sett_Coordinates_1" "New_VCM_Summary")
declare -a FORMS=("VCM_Sett_Coordinates_1.2")
UUID=$(uuidgen)

wget -O/dev/null "${API_ROOT}?task=start_odk_jar&username=${POLIO_USERNAME}&api_key=${POLIO_KEY}&cron_guid=${UUID}"

for FORM in "${FORMS[@]}";
 do
   echo $FORM
    java -jar $JAR_FILE \
     --form_id $FORM \
     --export_filename $FORM \
     --aggregate_url $AGGREGATE_URL \
     --storage_directory $STORAGE_DIRECTORY \
     --export_directory $EXPORT_DIRECTORY \
     --odk_username $ODK_USER admin \
     --odk_password $ODK_PASS P@ssword \
     --exclude_media_export;
done

sleep 2
# DONE WITH ODK JAR FILE #
wget -O/dev/null "${API_ROOT}?task=finish_odk_jar&username=${POLIO_USERNAME}&api_key=${POLIO_KEY}&cron_guid=${UUID}"

sleep 2

# DONE WITH ODK JAR FILE #
wget -O/dev/null "${API_ROOT}?task=ingest_odk_regions&username=${POLIO_USERNAME}&api_key=${POLIO_KEY}&cron_guid=${UUID}"
