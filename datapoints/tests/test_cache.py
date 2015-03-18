from subprocess import call

from django.test import TestCase
from django.test import Client
# from django.conf.test_settings import PROJECT_ROOT
from pandas import read_csv

from datapoints.models import DataPoint
from datapoints.cache_tasks import CacheRefresh


class CacheRefreshTestCase(TestCase):

    def __init__(self, *args, **kwargs):

        super(CacheRefreshTestCase, self).__init__(*args, **kwargs)

    def set_up(self):

        data_df = read_csv('datapoints/tests/_data/calc_data.csv')

        self.changed_by_id = 1

        self.test_df = data_df[data_df['is_raw'] == 1]
        self.target_df = data_df[data_df['is_raw'] == 0]

        self.build_db() # builds sprocs and views needed to test cache refresh

    def build_db(self):
        #
        # # filename = PROJECT_ROOT + '/bin/build_db.sh'
        # # filename = '/Users/johndingee_seed/code/UF04/polio/bin/build_db.sh'
        #
        # # filename = 'bin/build_db.sh'
        # # print '========'
        # # print filename
        # # print '========'
        #
        # # call("bash Users/johndingee_seed/code/UF04/polio/bin/build_db.sh")
        # # call("./" + filename)
        # call(["bash" ,"/Users/johndingee_seed/code/UF04/polio/bin/build_db.sh"])
        call(["bash" ,"/Users/johndingee_seed/code/UF04/polio/bin/build_test_db.sh"])

    def create_raw_datapoints(self):

        for row_ix,row_data in self.test_df.iterrows():

            dp_id = self.create_datapoint(row_data.region_id, row_data\
                .campaign_id, row_data.indicator_id, row_data.value)


    def create_datapoint(self, region_id, campaign_id, indicator_id, value):
        '''
        Right now this is being performed as a database insert.  I would like to
        Test this against the data entry resource, but this will do for now
        in order to test caching.
        '''

        dp_id = DataPoint.objects.create(
            region_id = region_id,
            campaign_id = campaign_id,
            indicator_id = indicator_id,
            value = value,
            changed_by_id = self.changed_by_id,
            source_datapoint_id = -1
        ).id

        return dp_id


    def test_basic(self):

        self.set_up()
        self.create_raw_datapoints()
        # cr = CacheRefresh()


        for row in self.target_df.iterrows():

            pass

            # resp = api.call('region_id':row.region_id,'indicator_id':indicator_id)
            # self.assertEqual(row.value,resp.value)

        self.assertEqual(1,2)
