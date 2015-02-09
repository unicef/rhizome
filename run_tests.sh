python manage.py test --settings=polio.settings_test

## For now the coverage will omit the urls and migrations.
# the urls specifically should be tested once the application has better coverate

coverage html --omit="venv/*,*migrations/*,*admin*,*manage*,*wsgi*,*__init__*,*test*,*settings*,*url*" -i

## shows any unused imports or PEP8 style violations ##
flake8 datapoints/ polio/ source_data/ --exclude=*migrations*

#######################
## Source Data Layer ##
#######################

## Test Models ##
## Test CSV Upload ##

#######################
## Master Data Layer ##
#######################

## DataPoint Models ##

###########################
## Standardization Layer ##
###########################

## Refresh Master ##

#################
## Cache Layer ##
#################

## Geographic Aggregation ##
## Computed Indicators ##

###################
## Request Layer ##
###################

## Check Required Params ##
## Test Pagination ##
## Test CSV output ##
