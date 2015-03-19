import json
from subprocess import call
from pprint import pprint

from django.test import TestCase
from tastypie.test import ResourceTestCase
from django.test import Client
# from django.conf.test_settings import PROJECT_ROOT
from pandas import read_csv, notnull

from datapoints.models import *
from datapoints.cache_tasks import CacheRefresh


class CacheRefreshTestCase(TestCase):

    '''
    from datapoints.cache_tasks import CacheRefresh
    from datapoints.models import DataPoint, Region
    r_ids = Region.objects.filter(parent_region_id = 12907).values_list('id',flat=True)
    dp_ids = DataPoint.objects.filter(region_id__in=r_ids,campaign_id=111,indicator_id__in=[55]).values_list('id',flat=True)
    mr = CacheRefresh(list(dp_ids))
    '''

    def __init__(self, *args, **kwargs):

        super(CacheRefreshTestCase, self).__init__(*args, **kwargs)

    def set_up(self):

        data_df = read_csv('datapoints/tests/_data/calc_data.csv')

        self.changed_by_id = 1

        self.test_df = data_df[data_df['is_raw'] == 1]
        self.target_df = data_df[data_df['is_raw'] == 0]

        self.build_db() # builds sprocs and views needed to test cache refresh
        self.create_metadata()


    def build_db(self):
        '''
        please fix me
        '''

        ## remove the build_test_db script and pass a $DB param to build_db.sh
        call(["bash" ,"/Users/johndingee_seed/code/UF04/polio/bin/build_test_db.sh"])

    def create_metadata(self):
        '''
        Creating the Indicator, Region, Campaign, meta data needed for the
        system to aggregate / caclulate.
        '''

        region_df = read_csv('datapoints/tests/_data/regions.csv')
        indicator_df = read_csv('datapoints/tests/_data/indicators.csv')
        calc_indicator_df = read_csv\
            ('datapoints/tests/_data/calculated_indicator_component.csv')

        region_ids = self.model_df_to_data(region_df,Region)
        indicator_ids = self.model_df_to_data(indicator_df,Indicator)
        calc_indicator_ids = self.model_df_to_data(calc_indicator_df,\
            CalculatedIndicatorComponent)


    def model_df_to_data(self,model_df,model):

        meta_ids = []

        non_null_df = model_df.where((notnull(model_df)), None)
        list_of_dicts = non_null_df.transpose().to_dict()

        for row_ix, row_dict in list_of_dicts.iteritems():

            row_id = model.objects.create(**row_dict)
            meta_ids.append(row_id)

        return meta_ids


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

        cr = CacheRefresh()

        for ix, row in self.target_df.iterrows():

            # actual_value = self.get_dwc_value(row)
            # actual_value = response_data[0]['value']

            actual_value = self.get_dwc_value(row)
            self.assertEqual(row.value,actual_value)


    def get_dwc_value(self,row):
        '''
        This testings the API for a row in the target dataframe and returns
        the corresponding value

        Testing the Value agains the API test_client currenlty is not working.
        Instead I will query the datapoint_with_computed table and ensure
        later that the dataopint_abstracted transformation is working properly
        '''

        dwc_curs = DataPointComputed.objects.raw('''
            SELECT id, value FROM datapoint_with_computed
                WHERE region_id = %s
                AND campaign_id = %s
                AND indicator_id = %s;
        ''' ,[int(row.region_id),int(row.campaign_id),int(row.indicator_id)])


        dwc_list = [dwc.value for dwc in dwc_curs]
        actual_value = dwc_list[0]

        # target_url = \
        # '/api/v1/datapoint/?region__in=%s&campaign__in=%s&indicator__in=%s'\
        # % (int(row.region_id),int(row.campaign_id),int(row.indicator_id))

        # c = Client()
        # resp = c.get(target_url,format='json',follow=True)
        # response_data = json.loads(resp.content)['objects']

        # print response_data

        # actual_value = float(response_data[0]['value'])

        return actual_value
