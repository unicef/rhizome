from pandas import read_csv
from django.test import TestCase


class CacheRefreshTestCase(TestCase):

    def __init__(self, *args, **kwargs):

        super(CacheRefreshTestCase, self).__init__(*args, **kwargs)

    def set_up(self):

        print 'TESTING\n' * 2

        test_df = read_csv('datapoints/tests/_data/calc_data.csv')

        print test_df

    def create_raw_datapoints(self,raw_df):

        pass

    def test_basic(self):

        self.set_up()

        self.assertEqual(1,1)
