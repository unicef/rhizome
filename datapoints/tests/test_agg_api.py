import time

from tastypie.test import ResourceTestCase
from django.core.urlresolvers import reverse
from django.test.client import Client

from datapoints.models import *
from source_data.models import *

class AggApiTestCase(ResourceTestCase):
    ''' bla bla  '''
    # python manage.py test datapoints.tests.test_agg_api.AggApiTestCase --settings=polio.settings_test


    def setUp(self):
        super(AggApiTestCase, self).setUp()

        ## AGGREGATION ##
        a = AggregationType.objects.create(
            name = 'calc_pct_single_reg_single_campaign',
            slug = 'calc_pct_single_reg_single_campaign',
            display_name_w_sub = 'doesntmatter'
        )

        AggregationExpectedData.objects.create(
            aggregation_type = a,
            content_type = 'indicator',
            param_type = 'part',
            slug='indicator_part'
        )

        AggregationExpectedData.objects.create(
            aggregation_type = a,
            content_type = 'indicator',
            param_type = 'whole',
            slug='indicator_whole'
        )

        AggregationExpectedData.objects.create(
            aggregation_type = a,
            content_type = 'campaign',
            param_type = 'solo',
            slug = 'campaign_solo'
        )

        AggregationExpectedData.objects.create(
            aggregation_type = a,
            content_type = 'region',
            param_type = 'solo',
            slug = 'region_solo'
        )

        ## REF DATA ##

        ind_part_val = 68
        ind_whole_val = 100

        user = User.objects.create(username='test_user')
        source = Source.objects.create(source_name='test_source')
        office = Office.objects.create(name='test_office')
        to_process_status = ProcessStatus.objects.create(status_text='TO_PROCESS')
        document = Document.objects.create(docfile='asfasfasf',created_by=user)

        campaign = Campaign.objects.create(
            name = 'fake campaign',
            office = office,
            start_date = time.strftime("%Y-%m-%d"),
            end_date = time.strftime("%Y-%m-%d"),
        )
        region = Region.objects.create(
            full_name = 'some region',
            region_code = 12414,
            office = office,
            latitude = 1.2,
            longitude = 2.1,
            source = source,
            source_guid = 'somethingfake'
        )

        ind_part = Indicator.objects.create(
            short_name = 'Number of Children Missed Due to Refusal',
            name = 'Number of Children Missed Due to Refusal',
            description = 'Number of Children Missed Due to Refusal'
        )

        ind_whole = Indicator.objects.create(
            short_name = 'Total Children Missed',
            name = 'Total Children Missed',
            description = 'Total Children Missed'
        )


        # need this for the foreign key to datapints table #

        sdp = SourceDataPoint.objects.create(
            region_string = 'easye',
            campaign_string = 'icecube',
            indicator_string = 'snoopdog',
            cell_value = 1.9,
            row_number= 0,
            source = source,
            document = document,
            source_guid = 'asfasfasfasfasfsa',
            status = to_process_status
        )

        ## Indicator Part #
        dp_ind_part = DataPoint.objects.create(
            indicator = ind_part,
            region = region,
            campaign = campaign,
            value = ind_part_val,
            changed_by = user,
            source_datapoint = sdp
        )


        ## Indicator Whole #
        ind_whole = DataPoint.objects.create(
            indicator = ind_whole,
            region = region,
            campaign = campaign,
            value = ind_whole_val,
            changed_by = user,
            source_datapoint = sdp
        )


    def test_something_fake(self):

        # a = AggregationType.objects.all()
        # ed = AggregationExpectedData.objects.filter(aggregation_type=a)

        # dps = DataPoint.objects.all()
        #
        # for d in dps:
        #     print d.value
        #

        response = self.api_client.get('/api/v1/aggregate',format='json')
        print response.status_code

        print 'PRINTING CONTEnt'
        print response.content


        self.assertEqual(1,1)
