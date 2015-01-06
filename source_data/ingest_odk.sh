#!/bin/bash

# find settings... script wont fail if file doesnt exists so try dev than prod
source /Users/johndingee_seed/code/UF04/polio/source_data/dev_odk_settings.py
source /var/www/clients.seedscientific.com/uf/UF04/polio/source_data/prod_odk_settings.py

## STARTING JAR FILE PROCESS ##
wget -O/dev/null http://localhost:8000/api/v1/etl?task=start_odk_jar&username=$POLIO_USERNAME&password=$POLIO_PASSWORD
pid[0]=$!


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

## DONE WITH THE JAR FILE PROCESS ##
wget -O/dev/null http://localhost:8000/api/v1/etl?task=finish_odk_jar&username=$POLIO_USERNAME&password=$POLIO_PASSWORD
pid[1]=$!


# ## populate data into vcm summary table ##
# wget -O/dev/null http://localhost:8000/api/v1/etl?task=odk_refresh_vcm_summary_work_table&username=$POLIO_USERNAME&password=$POLIO_PASSWORD
# pid[2]=$!
#
# ## move data from vcm summary table into source datapoints ##
# wget -O/dev/null http://localhost:8000/api/v1/etl?task=odk_vcm_summary_to_source_datapoints&username=$POLIO_USERNAME&password=$POLIO_PASSWORD
# pid[3]=$!

## kill all the wget spids
# trap INT " kill ${pid[0]} ${pid[1]} ${pid[2]} ${pid[3]}; exit 1"
trap INT " kill ${pid[0]} ${pid[1]}; exit 1"

wait
