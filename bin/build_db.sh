#!/bin/bash
SQL_DIR=$(pwd)'/datapoints/sql/polio/'

## VIEWS ##
# psql polio -f $SQL_DIR'vw_missing_mappings.sql'
psql polio -f $SQL_DIR'vw_region_simple.sql'

# Create the table needed for the datapoint modification tracking
# used by simple_history
psql polio -f './datapoints/sql/scripts/datapoints_entry_history.sql'
