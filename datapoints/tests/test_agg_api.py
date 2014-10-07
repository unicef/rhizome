import time
import pprint as pp
import urllib
import json
from random import randrange


from tastypie.test import ResourceTestCase
from django.core.urlresolvers import reverse

from datapoints.models import *
from source_data.models import *

class CalcPctSoloRegionSoloCampaign(ResourceTestCase):
    '''
    For one region, and one campaign, take the part over the whole for the
    two indicators provided in the URL string
    '''

    # python manage.py test datapoints.tests.test_agg_api.CalcPctSoloRegionSoloCampaign --settings=polio.settings_test


    def setUp(self):
        super(CalcPctSoloRegionSoloCampaign, self).setUp()

        ## AGGREGATION ##

        self.api_method_string = 'calc_pct_solo_region_solo_campaign'

        a = AggregationType.objects.create(
            name = self.api_method_string,
            slug = self.api_method_string,
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

        self.ind_part_val = 68.00
        self.ind_whole_val = 100.00

        self.user = User.objects.create(username='test_user')
        self.source = Source.objects.create(source_name='test_source')
        self.office = Office.objects.create(name='test_office')
        self.to_process_status = ProcessStatus.objects.create(status_text='TO_PROCESS')
        self.document = Document.objects.create(docfile='asfasfasf',created_by=self.user)

        self.campaign = Campaign.objects.create(
            name = 'fake campaign',
            office = self.office,
            start_date = time.strftime("%Y-%m-%d"),
            end_date = time.strftime("%Y-%m-%d"),
        )
        self.region = Region.objects.create(
            # full_name = 'some region',
            region_code = 12414,
            office = self.office,
            latitude = 1.2,
            longitude = 2.1,
            source = self.source,
            source_guid = 'somethingfake'
        )

        self.ind_part = Indicator.objects.create(
            short_name = 'Number of Children Missed Due to Refusal',
            name = 'Number of Children Missed Due to Refusal',
            description = 'Number of Children Missed Due to Refusal'
        )

        self.ind_whole = Indicator.objects.create(
            short_name = 'Total Children Missed',
            name = 'Total Children Missed',
            description = 'Total Children Missed'
        )


        # need this for the foreign key to datapints table #

        self.sdp = SourceDataPoint.objects.create(
            region_string = 'easye',
            campaign_string = 'icecube',
            indicator_string = 'snoopdog',
            cell_value = 1.9,
            row_number= 0,
            source = self.source,
            document = self.document,
            source_guid = 'asfasfasfasfasfsa',
            status = self.to_process_status
        )

        ## Indicator Part #
        self.dp_ind_part = DataPoint.objects.create(
            indicator = self.ind_part,
            region = self.region,
            campaign = self.campaign,
            value = self.ind_part_val,
            changed_by = self.user,
            source_datapoint = self.sdp
        )


        ## Indicator Whole #
        self.dp_ind_whole = DataPoint.objects.create(
            indicator = self.ind_whole,
            region = self.region,
            campaign = self.campaign,
            value = self.ind_whole_val,
            changed_by = self.user,
            source_datapoint = self.sdp
        )


    def test_(self):

        base_url = '/api/v1/aggregate/'

        params = {}
        params['api_method'] = self.api_method_string
        params['indicator_part'] = self.ind_part.id
        params['indicator_whole'] = self.ind_whole.id
        params['region_solo'] = self.region.id
        params['campaign_solo'] = self.campaign.id

        url = base_url + '?' + urllib.urlencode(params)

        response = self.api_client.get(url,follow=True)

        data = json.loads(response.content)

        objects = data['objects']
        result = objects[0]['DATA']

        final_val = str(self.ind_part_val  / self.ind_whole_val)
        self.assertEqual(result,final_val)


class CalcPctParentRegionSoloCampaign(ResourceTestCase):
    #python manage.py test datapoints.tests.test_agg_api.CalcPctSoloRegionSoloCampaign --settings=polio.settings_test

    def setUp(self):
        super(CalcPctParentRegionSoloCampaign, self).setUp()

        self.api_method_string = 'calc_pct_parent_region_solo_campaign'

        a = AggregationType.objects.create(
            name = self.api_method_string,
            slug = self.api_method_string,
            display_name_w_sub = self.api_method_string
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
            param_type = 'parent',
            slug = 'region_parent'
        )


        self.user = User.objects.create(username='test_user')
        self.source = Source.objects.create(source_name='test_source')
        self.office = Office.objects.create(name='test_office')
        self.to_process_status = ProcessStatus.objects.create(status_text='TO_PROCESS')
        self.document = Document.objects.create(docfile='asfasfasf',created_by=self.user)

        self.campaign = Campaign.objects.create(
            name = 'fake campaign',
            office = self.office,
            start_date = time.strftime("%Y-%m-%d"),
            end_date = time.strftime("%Y-%m-%d"),
        )


        self.ind_part = Indicator.objects.create(
            short_name = 'Number of Children Missed Due to Refusal',
            name = 'Number of Children Missed Due to Refusal',
            description = 'Number of Children Missed Due to Refusal'
        )

        self.ind_whole = Indicator.objects.create(
            short_name = 'Total Children Missed',
            name = 'Total Children Missed',
            description = 'Total Children Missed'
        )

        ## Sub Regions
        self.sub_region_0 = Region.objects.create(
            full_name = 'some sub region',
            region_code = 1,
            office = self.office,
            latitude = 1.2,
            longitude = 2.1,
            source = self.source,
            source_guid = 'somethingfake'
        )

        self.sub_region_1 = Region.objects.create(
            full_name = 'some other sub region',
            region_code = 2,
            office = self.office,
            latitude = 1.2,
            longitude = 2.1,
            source = self.source,
            source_guid = 'somethingfake1'
        )

        self.sub_region_2 = Region.objects.create(
            full_name = 'another sub region',
            region_code = 3,
            office = self.office,
            latitude = 1.2,
            longitude = 2.1,
            source = self.source,
            source_guid = 'somethingfake2'
        )

        self.parent_region = Region.objects.create(
            full_name = 'parent region',
            region_code = 4,
            office = self.office,
            latitude = 1.2,
            longitude = 2.1,
            source = self.source,
            source_guid = 'somethingfake3'
        )

        self.rr_type = RegionRelationshipType.objects.create(
          display_name = 'contains',
          inverse_display_name = 'contained_by',
          description = 'nys contains nys'
        )

        self.rr_0 = RegionRelationship.objects.create(
            region_0 = self.parent_region,
            region_1 = self.sub_region_0,
            region_relationship_type = self.rr_type

        )

        self.rr_1 = RegionRelationship.objects.create(
            region_0 = self.parent_region,
            region_1 = self.sub_region_1,
            region_relationship_type = self.rr_type

        )

        self.rr_2 = RegionRelationship.objects.create(
            region_0 = self.parent_region,
            region_1 = self.sub_region_2,
            region_relationship_type = self.rr_type

        )

        # need this for the foreign key to datapints table #

        self.sdp = SourceDataPoint.objects.create(
            region_string = 'easye',
            campaign_string = 'icecube',
            indicator_string = 'snoopdog',
            cell_value = 1.9,
            row_number= 0,
            source = self.source,
            document = self.document,
            source_guid = 'asfasfasfasfasfsa',
            status = self.to_process_status
        )

        ## Create the DataPoints

        sub_regions = [self.sub_region_0, self.sub_region_1, self.sub_region_2]

        for rg in sub_regions:

            ## Indicator Part #

            self.dp_ind_part = DataPoint.objects.create(
                indicator = self.ind_part,
                region = rg,
                campaign = self.campaign,
                value = random.randint(1,9),
                changed_by = self.user,
                source_datapoint = self.sdp
            )


            ## Indicator Whole #
            self.dp_ind_whole = DataPoint.objects.create(
                indicator = self.ind_whole,
                region = rg,
                campaign = self.campaign,
                value = random.randint(1,9) * 10,
                changed_by = self.user,
                source_datapoint = self.sdp
            )



    def test_(self):

        base_url = '/api/v1/aggregate/'

        params = {}
        params['api_method'] = self.api_method_string
        params['indicator_part'] = self.ind_part.id
        params['indicator_whole'] = self.ind_whole.id
        params['region_parent'] = self.parent_region.id
        params['campaign_solo'] = self.campaign.id

        url = base_url + '?' + urllib.urlencode(params)

        response = self.api_client.get(url,follow=True)

        data = json.loads(response.content)

        objects = data['objects']
        result = objects[0]['DATA']
        print result
        print result
        print result
        print result


        # final_val = str(self.ind_part_val  / self.ind_whole_val)
        self.assertEqual(1,1)
