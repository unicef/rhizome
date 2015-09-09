# flake8 datapoints/ polio/ source_data/ --exclude=*migrations*
python manage.py test --settings=polio.settings.test
coverage html --omit="venv/*,*migrations/*,*admin*,*manage*,*wsgi*,*__init__*,*test*,*settings*,*url*" -i


#######################
## Source Data Layer ##
#######################

## Test Models ##
## Test CSV Upload ##

#######################
## Master Data Layer ##
#######################

## DataPoint Models ##
## Test Refresh Master (source submission -> datapoint ) ##
## Geographic Aggregation ##
## Computed Indicators ##
## transforming computed_datapoint -. abstracted datapoint

###################
## Request Layer ##
###################

## required PARAMS
## serialization
## authentication
