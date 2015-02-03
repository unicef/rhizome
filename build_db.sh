#!/bin/bash
SQL_DIR=$(pwd)'/datapoints/sql/'

psql polio -f $SQL_DIR'scripts/computed_ref.sql'
psql polio -f $SQL_DIR'views/vw_missing_mappings.sql'
psql polio -f $SQL_DIR'views/vw_region_simple.sql'
psql polio -f $SQL_DIR'cache_tables/datapoint_plus_computed.sql'
