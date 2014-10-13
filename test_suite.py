import unittest
from unittest import TestResult

from datapoints.tests.test_api_filters import CampaignDateFilterTestCase
from source_data.tests.all_tests import NewDPTestCase

# python manage.py test test_suite.run_all --settings=polio.settings_test


def build_suite():
    """
        Gather all the tests from this module in a test suite.
    """
    test_suite = unittest.TestSuite()


    ## ODK ##
    ## CSV UPLOAD ##
    ## POST REQUESTS ##
    ## META DATA ##
    ## REFRESH MASTER METHOD ##
    test_suite.addTest(unittest.makeSuite(NewDPTestCase))
    ## BASIC API ##
    ## CUSTOM FILTERS ##
    test_suite.addTest(unittest.makeSuite(CampaignDateFilterTestCase))
    ## AGGREGATE QUERIES ##

    return test_suite

def run_all():
    test_results = TestResult()
    my_suite = build_suite()
    my_suite.run(test_results)

    return my_suite
