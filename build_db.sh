#!/bin/bash
SQL_DIR=$(pwd)'/datapoints/sql/views/'

psql polio -f $SQL_DIR'vw_datapoint.sql'
psql polio -f $SQL_DIR'vw_missing_mappings.sql'
psql polio -f $SQL_DIR'vw_region_simple.sql'
