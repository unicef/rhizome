#!/bin/bash

PROTOCOL="http://"
HOST="polio.localhost"
API="/api/v1/datapoint"
PARAMS="username=evan&api_key=67bd6ab9a494e744a213de2641def88163652dad&campaign_start=2012-03-01&campaign_end=2014-03-01&region__in=12907"

URL="$PROTOCOL$HOST$API?$PARAMS"

# wget -b --user=unicef --password=stoppolio -O "168.json" -- "$URL&indicator__in=168"
# wget -b --user=unicef --password=stoppolio -O "165-166-167-188.json" -- "$URL&indicator__in=166,188,167,165"
# wget -b --user=unicef --password=stoppolio -O "187-180.json" -- "$URL&indicator__in=187,189"

wget -b -O "168.json" -- "$URL&indicator__in=168"
wget -b -O "165-166-167-188.json" -- "$URL&indicator__in=166,188,167,165"
wget -b -O "187-180.json" -- "$URL&indicator__in=187,189"
