import json
from subprocess import call
from pprint import pprint

from django.db import transaction
from django.test import TransactionTestCase, TestCase
from django.contrib.auth.models import User
from tastypie.test import ResourceTestCase
from django.test import Client
# from django.conf.test_settings import PROJECT_ROOT
from pandas import read_csv, notnull

from datapoints.models import *
from source_data.models import *
from datapoints.cache_tasks import CacheRefresh


# class CacheRefreshTestCase(TransactionTestCase):
class CacheRefreshTestCase(TestCase):

    '''
        from datapoints.cache_tasks import CacheRefresh
        mr = CacheRefresh()

        ## or ##

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

        self.create_metadata()

    def create_metadata(self):
        '''
        Creating the Indicator, Region, Campaign, meta data needed for the
        system to aggregate / caclulate.
        '''
        campaign_df = read_csv('datapoints/tests/_data/campaigns.csv')
        region_df= read_csv('datapoints/tests/_data/regions.csv')
        indicator_df = read_csv('datapoints/tests/_data/indicators.csv')
        calc_indicator_df = read_csv\
            ('datapoints/tests/_data/calculated_indicator_component.csv')

        user_id = User.objects.create_user('test','john@john.com', 'test').id

        office_id = Office.objects.create(id=1,name='test').id

        source_id1 = Source.objects.create(id=1,source_name='test1',source_description='test1').id
        source_id2 = Source.objects.create(id=2,source_name='test2',source_description='test2').id

        cache_job_id = CacheJob.objects.create(id = -2,date_attempted = '2015-01-01', is_error = False)

        status_id = ProcessStatus.objects.create(
                status_text = 'test',
                status_description = 'test').id

        document_id = Document.objects.create(
            doc_text = 'test',
            created_by_id = user_id,
            source_id = source_id1,
            guid = 'test').id

        sdp_id = SourceDataPoint.objects.create(
            id = -1,
            document_id = document_id,
            row_number = 0,
            source_id = source_id1,
            status_id = status_id).id


        region_type1 = RegionType.objects.create(id=1,name="country")
        region_type2 = RegionType.objects.create(id=2,name="settlement")
        region_type3 = RegionType.objects.create(id=3,name="province")
        region_type4 = RegionType.objects.create(id=4,name="district")
        region_type5 = RegionType.objects.create(id=5,name="sub-district")

        campaign_type = CampaignType.objects.create(id=1,name="test")

        region_ids = self.model_df_to_data(region_df,Region)
        campaign_ids = self.model_df_to_data(campaign_df,Campaign)
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
        '''
        Using the calc_data.csv, create a test_df and target_df.  Ensure that
        the aggregation and calcuation are working properly, but ingesting the
        stored data, running the cache, and checking that the calculated data
        for the aggregate region (parent region, in this case Nigeria) is as
        expected.
        '''

        self.set_up()
        self.create_raw_datapoints()

        cr = CacheRefresh()

        for ix, row in self.target_df.iterrows():

            region_id, campaign_id, indicator_id = int(row.region_id),\
               int(row.campaign_id),int(row.indicator_id)

            actual_value = self.get_dwc_value(region_id, campaign_id,\
                indicator_id)

            self.assertEqual(row.value,actual_value)

    def test_agg(self):
        '''
        First refresh the new datapoints and then only refresh the cache for
        one datapoint_id and make sure agg uses all child data below even when
        that data is from a different job

        To Do - After the first cache_refresh, update the value and make sure
        that the aggregated total works.  Note - will need to use either
        ``transaction.atomic`` or ``TrasactionTestCase`` in order to persist
        multiple DB changes within one test
        '''
        raw_indicator_id, campaign_id, raw_region_id, agg_region_id = 22, 111,\
            12939, 12907

        self.set_up()
        self.create_raw_datapoints()

        agg_value_target = self.test_df = self.test_df[self.test_df['indicator_id'] ==\
             raw_indicator_id]['value'].sum()

        dp_id_to_refresh = DataPoint.objects.filter(
            region_id = raw_region_id,
            campaign_id = campaign_id ,
            indicator_id = raw_indicator_id
        ).values_list('id',flat=True)

        cr = CacheRefresh()

        ## now just try for one id (see POLIO-491 )
        cr = CacheRefresh(datapoint_id_list=list(dp_id_to_refresh))

        actual_value = self.get_dwc_value(agg_region_id,campaign_id,\
            raw_indicator_id)

        self.assertEqual(actual_value,agg_value_target)

    def get_dwc_value(self,region_id,campaign_id,indicator_id):
        '''
        This testings the API for a row in the target dataframe and returns
        the corresponding value

        Testing the Value agains the API test_client currenlty is not working.
        Instead I will query the datapoint_with_computed table and ensure
        later that the dataopint_abstracted transformation is working properly
        '''

        actual_value = DataPointComputed.objects.get(
            region_id = region_id,
            indicator_id = indicator_id,
            campaign_id = campaign_id
        ).value

        return actual_value
