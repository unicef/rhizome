#!/bin/bash
SQL_DIR=$(pwd)'/datapoints/sql/'

## VIEWS ##
# psql  -f $SQL_DIR'views/vw_missing_mappings.sql'

## FUNCTIONS ##


psql test_polio -f $SQL_DIR'functions/fn_agg_datapoint.sql'
psql test_polio -f $SQL_DIR'functions/fn_test_data_accuracy.sql'
psql test_polio -f $SQL_DIR'functions/fn_find_bad_data.sql'

psql test_polio -f $SQL_DIR'functions/fn_calc_prep.sql'
psql test_polio -f $SQL_DIR'functions/fn_calc_sum_of_parts.sql'
psql test_polio -f $SQL_DIR'functions/fn_calc_part_over_whole.sql'
psql test_polio -f $SQL_DIR'functions/fn_calc_part_of_difference.sql'
psql test_polio -f $SQL_DIR'functions/fn_calc_upsert_computed.sql'

psql test_polio -f $SQL_DIR'functions/fn_calc_datapoint.sql'
