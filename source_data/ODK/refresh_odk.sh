declare -a FORMS=("vcm_register" "VCM_Sett_Coordinates_1" "New_VCM_Summary")
POLIO_USERNAME=evan
POLIO_KEY=67bd6ab9a494e744a213de2641def88163652dad
UUID=$(uuidgen)
API_ROOT="http://localhost:8000/api/v1/etl/"


 wget -O/dev/null "${API_ROOT}?task=start_odk_jar&username=${POLIO_USERNAME}&api_key=${POLIO_KEY}&cron_guid=${UUID}"

for FORM in "${FORMS[@]}";
 do
   echo $FORM
    java -jar odk_briefcase.jar \
     --form_id $FORM \
     --export_filename $FORM \
     --aggregate_url https://vcm-ng.appspot.com/ \
     --storage_directory ~/ODK/odk_source \
     --export_directory ~/ODK/odk_source/csv_exports \
     --odk_username admin \
     --odk_password P@ssword \
     --exclude_media_export;
done

sleep 2
# DONE WITH ODK JAR FILE #
wget -O/dev/null "${API_ROOT}?task=finish_odk_jar&username=${POLIO_USERNAME}&api_key=${POLIO_KEY}&cron_guid=${UUID}"

# DONE WITH ODK JAR FILE #
wget -O/dev/null "${API_ROOT}?task=ingest_odk_regions&username=${POLIO_USERNAME}&api_key=${POLIO_KEY}&cron_guid=${UUID}"
