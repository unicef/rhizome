#!/bin/bash
SQL_DIR=$(pwd)'/datapoints/sql/'

## VIEWS ##
psql polio -f $SQL_DIR'views/vw_missing_mappings.sql'
psql polio -f $SQL_DIR'views/vw_region_simple.sql'
psql polio -f $SQL_DIR'views/vw_campaign_simple.sql'

## FUNCTIONS ##
psql polio -f $SQL_DIR'functions/fn_agg_datapoint.sql'
psql polio -f $SQL_DIR'functions/fn_calc_datapoint.sql'
psql polio -f $SQL_DIR'functions/fn_test_data_accuracy.sql'
