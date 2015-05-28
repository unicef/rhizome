FORM=vcm_register

java -jar odk_briefcase.jar \
--form_id $FORM \
--export_filename $FORM + '.csv' \
--aggregate_url https://vcm-ng.appspot.com/ \
--storage_directory ~/ODK/odk_source \
--export_directory ~/ODK/odk_source/csv_exports \
--odk_username admin \
--odk_password P@ssword \
--exclude_media_export \
