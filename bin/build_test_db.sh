#!/bin/bash
SQL_DIR=$(pwd)'/datapoints/sql/'

## VIEWS ##
# psql  -f $SQL_DIR'views/vw_missing_mappings.sql'

## FUNCTIONS ##
psql test_polio -f $SQL_DIR'functions/fn_agg_datapoint.sql'
psql test_polio -f $SQL_DIR'functions/fn_calc_datapoint.sql'
psql test_polio -f $SQL_DIR'functions/fn_test_data_accuracy.sql'
