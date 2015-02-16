#!/bin/bash
SQL_DIR=$(pwd)'/datapoints/sql/polio/'

## SCRIPTS ##
psql polio -f $SQL_DIR'computed_ref.sql'
psql polio -f $SQL_DIR'datapoint_agg_and_compute.sql'

## VIEWS ##
psql polio -f $SQL_DIR'vw_missing_mappings.sql'
psql polio -f $SQL_DIR'vw_region_simple.sql'
