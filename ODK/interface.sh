#!/bin/sh


## pull from aggregate

# java -jar Briefcase.jar --form_id market_prices --storage_directory
# ~/Desktop --aggregate_url https://my-server.appspot.com --odk_username
# admin --odk_password p@ssw0rd;

## export to csv

# java -jar Briefcase.jar --form_id market_prices --storage_directory
# ~/Desktop --export_directory ~/Desktop --export_filename
# market_prices.csv;

JAR_FILE="/Users/johndingee_seed/ODK_local/Briefcase_v1.4.4.jar"
FORM_ID="build_Polio-Sample_1406906455"
AGGREGATE_URL="http://10.0.1.71/"
STORAGE_DIRECTORY="/Users/johndingee_seed/Desktop"
USERNAME="aggregate"
PASSWORD="aggregate"

java -jar $JAR_FILE \
--form_id $FORM_ID \
--storage_directory $STORAGE_DIRECTORY \
 --aggregate_url $AGGREGATE_URL \
 --odk_username $USERNAME \
 --odk_password $PASSWORD;
