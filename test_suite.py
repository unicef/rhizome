import unittest
from unittest import TestResult

from datapoints.tests.test_api_filters import CampaignDateFilterTestCase
from datapoints.tests.test_agg_api import CalcPctSoloRegionSoloCampaign
from datapoints.tests.test_agg_api import CalcPctParentRegionSoloCampaign
# from source_data.tests.test_odk import OdkTestCase
from source_data.tests.test_master_refresh import NewDPTestCase

# python manage.py test test_suite.run_all --settings=polio.settings_test



def run_all():
    '''
    this method runs all of the tests int he application.  to run tests:
    python manage.py test test_suite.run_all --settings=polio.settings_test

    '''
    result = TestResult()
    my_suite = build_suite()
    my_suite.run(result)

    print 'WHAT FAILED\n' * 10

    print result.failures
    return my_suite



def build_suite():
    """
    Gather all the tests from this module in a test suite.
    """
    test_suite = unittest.TestSuite()

    ###############
    ## BASIC API ##
    ###############

    ####################
    ## CUSTOM FILTERS ##
    ####################
    # test_suite.addTest(unittest.makeSuite(CampaignDateFilterTestCase))


    #######################
    ## AGGREGATE QUERIES ##
    #######################
    # test_suite.addTest(unittest.makeSuite(CalcPctSoloRegionSoloCampaign))
    # test_suite.addTest(unittest.makeSuite(CalcPctParentRegionSoloCampaign))

    #########
    ## ODK ##
    #########
    # OdkTestCase

    ###########################
    ## REFRESH MASTER METHOD ##
    ###########################
    # test_suite.addTest(unittest.makeSuite(NewDPTestCase))


    print '=\n' * 100

    return test_suite
