from django.utils import timezone

from pandas import concat
from pandas import DataFrame
from pandas import notnull

from rhizome.cache_meta import IndicatorCache

import numpy as np

class AggRefresh(object):
    '''

    '''

    def __init__(self, campaign_id=None):
        '''
        If there is a job running, return to with a status code of
        "cache_running".

        If passed an explicit list of datapoints ids, then we process those
        other wise the datapoint IDs to process are handled in the set_up()
        method.
        '''
        pass
