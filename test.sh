#!/bin/bash
STR="Hello World!"
# echo $STR

SETTINGS="polio.settings_test"

python manage.py test --keepdb source_data --settings=$SETTINGS
