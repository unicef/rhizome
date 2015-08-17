#!/bin/bash
SQL_DIR=$(pwd)'/datapoints/sql/'
DB=rhizome

## FUNCTIONS ##

psql $DB -f $SQL_DIR'functions/fn_agg_datapoint.sql'
psql $DB -f $SQL_DIR'functions/fn_test_data_accuracy.sql'

psql $DB -f $SQL_DIR'functions/fn_calc_prep.sql'
psql $DB -f $SQL_DIR'functions/fn_calc_sum_of_parts.sql'
psql $DB -f $SQL_DIR'functions/fn_calc_part_over_whole.sql'
psql $DB -f $SQL_DIR'functions/fn_calc_part_of_difference.sql'
psql $DB -f $SQL_DIR'functions/fn_calc_upsert_computed.sql'
psql $DB -f $SQL_DIR'functions/fn_calc_datapoint.sql'
psql $DB -f $SQL_DIR'functions/fn_get_authorized_regions_by_user.sql'

SRC_SQL_DIR=$(pwd)'/source_data/sql/'

psql $DB -f $SRC_SQL_DIR'functions/fn_populate_doc_meta.sql'
psql $DB -f $SRC_SQL_DIR'functions/fn_upsert_source_dps.sql'
psql $DB -f $SRC_SQL_DIR'functions/fn_sync_odk_regions.sql'
