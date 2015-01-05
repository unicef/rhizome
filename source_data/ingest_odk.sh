#!/bin/bash

# find settings... script wont fail if file doesnt exists so try dev than prod
source /Users/johndingee_seed/code/UF04/polio/source_data/dev_odk_settings.py
source /var/www/clients.seedscientific.com/uf/UF04/polio/source_data/prod_odk_settings.py

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
