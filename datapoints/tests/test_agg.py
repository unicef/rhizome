import json
from subprocess import call
from pprint import pprint
from os import path

from django.db import transaction
from django.test import TransactionTestCase, TestCase
from django.contrib.auth.models import User
from tastypie.test import ResourceTestCase
from django.test import Client
from django.core.management import call_command
from django.db import migrations

# from django.conf.test_settings import PROJECT_ROOT
from pandas import read_csv, notnull

from datapoints.models import *
from source_data.models import *
from datapoints.agg_tasks import CacheRefresh


class CacheRefreshTestCase(TestCase):

    '''
    from datapoints.agg_tasks import CacheRefresh
    mr = CacheRefresh()

    ## or ##

    from datapoints.agg_tasks import CacheRefresh
    from datapoints.models import DataPoint, location
    r_ids = location.objects.filter(parent_location_id = 12907).values_list('id',flat=True)
    dp_ids = DataPoint.objects.filter(location_id__in=r_ids,campaign_id=111,indicator_id__in=[55]).values_list('id',flat=True)
    mr = CacheRefresh(list(dp_ids))
    '''

    def __init__(self, *args, **kwargs):

        super(CacheRefreshTestCase, self).__init__(*args, **kwargs)

    def set_up(self):

        data_df = read_csv('datapoints/tests/_data/calc_data.csv')
        self.create_metadata()
        self.user = User.objects.get(username="test")

        self.test_df = data_df[data_df['is_raw'] == 1]
        self.target_df = data_df[data_df['is_raw'] == 0]

        # ./manage.py migrate --fake myapp 0004_previous_migration
        # ./manage.py migrate myapp 0005_migration_to_run

    def readSQLFromFile(self,filename):
        SQL_DIR = path.join(path.dirname(path.dirname(path.\
            abspath(__file__))), 'sql')
        return open(path.join(SQL_DIR, filename), 'r').read()

    def create_metadata(self):
        '''
        Creating the Indicator, location, Campaign, meta data needed for the
        system to aggregate / caclulate.
        '''

        campaign_df = read_csv('datapoints/tests/_data/campaigns.csv')
        location_df= read_csv('datapoints/tests/_data/locations.csv')
        indicator_df = read_csv('datapoints/tests/_data/indicators.csv')
        calc_indicator_df = read_csv\
            ('datapoints/tests/_data/calculated_indicator_component.csv')

        user_id = User.objects.create_user('test','john@john.com', 'test').id

        office_id = Office.objects.create(id=1,name='test').id

        cache_job_id = CacheJob.objects.create(id = -2,date_completed=\
            '2015-01-01',date_attempted = '2015-01-01', is_error = False)

        status_id = ProcessStatus.objects.create(
                status_text = 'test',
                status_description = 'test').id

        location_type1 = LocationType.objects.create(admin_level=0,name="country")
        location_type2 = LocationType.objects.create(admin_level=1,name="province")
        # location_type3 = LocationType.objects.create(admin_level=2,name="district")

        campaign_type1 = CampaignType.objects.create(name='test')

        location_ids = self.model_df_to_data(location_df,Location)
        campaign_ids = self.model_df_to_data(campaign_df,Campaign)
        indicator_ids = self.model_df_to_data(indicator_df,Indicator)
        calc_indicator_ids = self.model_df_to_data(calc_indicator_df,\
            CalculatedIndicatorComponent)

        document = Document.objects.create(
            doc_title = 'test',
            created_by_id = user_id,
            guid = 'test')

        ss = SourceSubmission.objects.create(
            document_id = document.id,
            submission_json = '',
            row_number = 0
        ).id


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

            dp_id = self.create_datapoint(row_data.location_id, row_data\
                .campaign_id, row_data.indicator_id, row_data.value)


    def create_datapoint(self, location_id, campaign_id, indicator_id, value):
        '''
        Right now this is being performed as a database insert.  I would like to
        Test this against the data entry resource, but this will do for now
        in order to test caching.
        '''

        document_id = Document.objects.get(doc_title='test').id
        ss_id = SourceSubmission.objects.get(document_id = document_id).id

        dp_id = DataPoint.objects.create(
            location_id = location_id,
            campaign_id = campaign_id,
            indicator_id = indicator_id,
            value = value,
            changed_by_id = self.user.id,
            source_submission_id = ss_id
        ).id

        return dp_id

    def test_location_aggregation(self):
        '''
        Using the calc_data.csv, create a test_df and target_df.  Ensure that
        the aggregation and calcuation are working properly, but ingesting the
        stored data, running the cache, and checking that the calculated data
        for the aggregate location (parent location, in this case Nigeria) is as
        expected.
        '''

        self.set_up()
        self.create_raw_datapoints()
        indicator_id, campaign_id, raw_location_id,\
            agg_location_id = 22,111,12910,12907

        location_ids = Location.objects.filter(parent_location_id =\
            agg_location_id).values_list('id',flat=True)

        dps = DataPoint.objects.filter(\
            indicator_id = indicator_id,
            campaign_id = campaign_id,
            location_id__in = location_ids
            ).values_list('id','value')

        sum_dp_value = sum([y for x,y in dps])
        dp_ids = [x for x,y in dps]

        cr = CacheRefresh(datapoint_id_list=dp_ids)

        #################################################
        ## ensure that raw data gets into AggDataPoint ##
        #################################################

        raw_value = DataPoint.objects.get(campaign_id = campaign_id,
            indicator_id = indicator_id,
            location_id = raw_location_id)\
            .value

        raw_value_in_agg = AggDataPoint.objects.get(campaign_id = campaign_id,
            indicator_id = indicator_id,
            location_id = raw_location_id)\
            .value

        self.assertEqual(raw_value, raw_value_in_agg)

        #############################################
        ## ensure that the aggregated data gets in ##
        #############################################

        agg_value = AggDataPoint.objects.get(
            indicator_id = indicator_id,
            campaign_id = campaign_id,
            location_id = agg_location_id
        ).value

        self.assertEqual(agg_value, sum_dp_value)

    def test_raw_data_to_computed(self):
        '''
        This just makes sure that any data in the datapoint table, gets into the
        Calculated DataPoint table.  That is, i insert a value for missed
        children in Borno, the same exact data should be in the
        datapoint_with_computed table no matter what.
        '''

        self.set_up()
        self.create_raw_datapoints()
        indicator_id, campaign_id, raw_location_id,\
            agg_location_id = 22,111,12910,12907

        location_ids = Location.objects.filter(parent_location_id =\
            agg_location_id).values_list('id',flat=True)

        dps = DataPoint.objects.filter(\
            indicator_id = indicator_id,
            campaign_id = campaign_id,
            location_id__in = location_ids
            ).values_list('id','value')

        sum_dp_value = sum([y for x,y in dps])
        dp_ids = [x for x,y in dps]

        cr = CacheRefresh(datapoint_id_list=dp_ids)

        #################################################
        ## ensure that raw data gets into datapoint_with_computed ##
        #################################################

        raw_value = DataPoint.objects.get(campaign_id = campaign_id,
            indicator_id = indicator_id,
            location_id = raw_location_id)\
            .value

        raw_value_in_agg = DataPointComputed.objects.get(campaign_id = campaign_id,
            indicator_id = indicator_id,
            location_id = raw_location_id)\
            .value

        self.assertEqual(raw_value, raw_value_in_agg)

        #############################################
        ## ensure that the aggregated data gets in ##
        #############################################

        agg_value = AggDataPoint.objects.get(
            indicator_id = indicator_id,
            campaign_id = campaign_id,
            location_id = agg_location_id
        ).value

        self.assertEqual(agg_value, sum_dp_value)
