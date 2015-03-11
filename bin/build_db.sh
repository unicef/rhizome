#!/bin/bash
SQL_DIR=$(pwd)'/datapoints/sql/polio/'

## VIEWS ##
# psql polio -f $SQL_DIR'vw_missing_mappings.sql'
psql polio -f $SQL_DIR'vw_region_simple.sql'
