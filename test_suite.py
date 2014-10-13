import unittest
from unittest import TestResult

from datapoints.tests.test_api_filters import CampaignDateFilterTestCase


def suite():
    """
        Gather all the tests from this module in a test suite.
    """
    test_suite = unittest.TestSuite()
    test_suite.addTest(unittest.makeSuite(CampaignDateFilterTestCase))
    return test_suite

def run_all():

    test_results = TestResult()
    my_suite = suite()
    my_suite.run(test_results)

    return my_suite



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
# python manage.py test datapoints.tests.test_api_filters.CampaignDateFilterTestCase --settings=$SETTINGS



## AGGREGATE QUERIES ##
# Aggregate API Methods
# solo region solo campaign indicator percentage
# parent region solo campaign indicator percentage
