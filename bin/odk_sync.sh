#!/bin/bash

# find settings... script wont fail if file doesnt exists so try dev than prod
source /Users/johndingee_seed/code/UF04/polio/source_data/dev_odk_settings.py

JAR_FILE="/Users/johndingee_seed/code/UF04/polio/source_data/Briefcase_v1.4.4.jar"
AGGREGATE_URL="https://vcm-ng.appspot.com/"
STORAGE_DIRECTORY="/Users/johndingee_seed/code/UF04/polio/static/odk_source/"
EXPORT_DIRECTORY="/Users/johndingee_seed/code/UF04/polio/static/odk_source/csv_exports/"
USERNAME="admin"
PASSWORD="P@ssword"



# create an id that we can use to identify one cron execution
UUID=$(uuidgen)


API_ROOT='http://localhost:8000'

# ## STARTING JAR FILE PROCESS ##
wget -O/dev/null $API_ROOT/api/v1/etl/?task=start_odk_jar\&username=$POLIO_USERNAME\&password=$POLIO_KEY\&cron_guid=$UUID
wget -O/dev/null $API_ROOT/api/v1/etl/?task=start_odk_jar\&cron_guid=$UUID


java -jar $JAR_FILE \
--form_id $FORM_ID \
--export_filename $FORM_ID + '.csv' \
--aggregate_url $AGGREGATE_URL \
--storage_directory $STORAGE_DIRECTORY \
--export_directory $EXPORT_DIRECTORY \
--odk_username $USERNAME \
--odk_password $PASSWORD \
--overwrite_csv_export \
--exclude_media_export \

# JAR_PID=$!

echo DONE WITH THE JAR FILE PROCESS ##
wget -O/dev/null $API_ROOT/api/v1/etl/?task=finish_odk_jar\&username=$POLIO_USERNAME\&password=$POLIO_KEY\&cron_guid=$UUID

sleep 2
# wget -O/dev/null $API_ROOT/api/v1/etl/?task=odk_refresh_vcm_summary_work_table\&username=$POLIO_USERNAME\&password=$POLIO_KEY\&cron_guid=$UUID
# echo done w transform the ODK csv into work table records ##

# sleep 2
# wget -O/dev/null $API_ROOT/api/v1/etl/?task=odk_vcm_summary_to_source_datapoints\&username=$POLIO_USERNAME\&password=$POLIO_KEY\&cron_guid=$UUID
# echo transform work table records into source datapoints ##

#
wait

echo complete!
