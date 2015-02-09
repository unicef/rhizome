import unittest
from datapoints.tests.test_models import *


def run_all():
    '''
    this method runs all of the tests int he application.

    To run tests:
        python manage.py test test_suite.run_all --settings=polio.settings_test
    '''
    result = unittest.TestResult()
    suite = build_suite() #
    suite.run(result)

    return suite

def build_suite():
    """
    Gather all the tests from this module in a test suite.
    """
    test_suite = unittest.TestSuite()

    #######################
    ## Source Data Layer ##
    #######################

    ## Test Models ##
    ## Test CSV Upload ##


    ###########################
    ## Standardization Layer ##
    ###########################

    ## DataPoint Models ##
    test_suite.addTest(unittest.makeSuite(IndicatorTest))
    # test_suite.addTest(unittest.makeSuite(RegionTest))
    # test_suite.addTest(unittest.makeSuite(DataPointTest))

    # , RegionTest, DataPointTest

    ## Refresh Master ##


    #################
    ## Cache Layer ##
    #################

    ## Geographic Aggregation ##
    ## Computed Indicators ##
        # pct
        # sum
        # difference


    ###################
    ## Request Layer ##
    ###################

    ## Check Required Params ##
    ## Test Pagination ##
    ## Test CSV output ##


    return test_suite



if __name__ == "__main__":
    run_all()
