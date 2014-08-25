#!/bin/sh

## DEFINE VARIABLES ##
JAR_FILE="/Users/johndingee_seed/ODK_local/Briefcase_v1.4.4.jar"
FORM_ID="VCM_Summary"
AGGREGATE_URL="https://vcm-ng.appspot.com/"
STORAGE_DIRECTORY="/Users/johndingee_seed/Desktop/"
EXPORT_DIRECTORY="/Users/johndingee_seed/Desktop/csv_exports"
EXPORT_FILENAME=$FORM_ID".csv"
USERNAME="admin"
PASSWORD="P@ssword"
START_DATE="2014/08/23"
END_DATE="2014/08/24"

## PULL FROM AGGREGATE AND EXPORT TO CSV ##
java -jar $JAR_FILE \
--form_id $FORM_ID \
--storage_directory $STORAGE_DIRECTORY \
 --aggregate_url $AGGREGATE_URL \
 --odk_username $USERNAME \
 --odk_password $PASSWORD \
 --export_directory $EXPORT_DIRECTORY \
 --export_filename $EXPORT_FILENAME \
 -start $START_DATE \
 -end $END_DATE;

## PARAMS FOR JAR FILE ##

# -ed,--export_directory </path/to/dir>
# -em,--exclude_media_export
# -end,--export_end_date <yyyy/MM/dd>
# -f,--export_filename <name.csv>
# -h,--help
# -id,--form_id <form_id>
# -oc,--overwrite_csv_export
# -od,--odk_directory </path/to/dir>
# -p,--odk_password <password>
# -pf,--pem_file </path/to/file.pem>
# -sd,--storage_directory </path/to/dir>
# -start,--export_start_date <yyyy/MM/dd>
# -u,--odk_username <username>
# -url,--aggregate_url <url>
# -v,--version




## NOTES ##
# Our problem is that we need to figure out how to pull data from ODK
# aggregate with a particular time filter.

## -> the command line tools pull ALL data then filter on the start / end date
## -> this doesnt work for us because we still need to pull all of the data from ODK

## Solution ->
  ## Create a database / file system that holds all of the submissions from ODK call this 'Archve'
  ## Pull the data from ODK
  ## Save this data to the archive
  ## Process data and save it to the Polio Back end (our app)
  ## Truncate the data in ODK Aggregate for that form
    ## -> Next time you pull this data, you will have only the data inserted since truncation

## Semi Solution ->
  ## Hit ODK Aggregate for one thread per form.
