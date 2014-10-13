#!/usr/bash


SETTINGS="polio.settings_test"

# python manage.py test source_data --settings=$SETTINGS


    # INSERTING DATA

## ODK ##
# Testing jar file process
# Testing work table
# Testing work table to source datapoints

## CSV ##
# File saves properly
# Pivoted Data can be re-built to reflect the source data exactly

## POST ##
# Data gets into source datpoints


    ## INSERTING METADATA ##

## BASIC ##
# Creating Source Regions, Indicators, Campaigns from Source Data
# Create Mappings for Source Regions, Source Indicators, Source Campaigns

## REFRESH MASTER METHOD ##
# Datapoints with mapped metadata get in
# Datapoints without mapped meta data do not get in
# Duplicative Datapoints -> New takes precedence over Old
# Datapoints with Deleted Mappings get deleted
# Datapoints with Updated Mappings get Updated

    ## RETRIEVING DATA ##

## BASIC API ##
# Basic API Methods
# Test Filters
# CSV Export

## CUSTOM FILTERS ##
# Test Campaign Filters
python manage.py test datapoints.tests.test_api_filters.CampaignDateFilterTestCase --settings=$SETTINGS



## AGGREGATE QUERIES ##
# Aggregate API Methods
# solo region solo campaign indicator percentage
# parent region solo campaign indicator percentage
