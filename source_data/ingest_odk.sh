#!/bin/bash

# find settings... script wont fail if file doesnt exists so try dev than prod
source /Users/johndingee_seed/code/UF04/polio/source_data/dev_odk_settings.py
source /var/www/clients.seedscientific.com/uf/UF04/polio/source_data/prod_odk_settings.py

wget -O/dev/null http://localhost:8000/api/v1/etl?task=start_odk_jar&username=$POLIO_USERNAME&password=$POLIO_PASSWORD

pid[0]=$!
trap INT " kill ${pid[0]}; exit 1"
wait


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


wget -O/dev/null http://localhost:8000/api/v1/etl?task=finish_odk_jar&username=$POLIO_USERNAME&password=$POLIO_PASSWORD

## this peice of code kills the wget process we just ran ( same as cntr-c )
pid[0]=$!
trap INT " kill ${pid[0]}; exit 1"
wait
