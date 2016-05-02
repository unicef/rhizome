import json

from tastypie.test import ResourceTestCase
from django.contrib.auth.models import User
from setup_helpers import TestSetupHelpers
from pandas import read_csv, notnull, to_datetime
from rhizome.models import *

class ComputedDatapointResourceTest(ResourceTestCase):
    def setUp(self):
        super(ComputedDatapointResourceTest, self).setUp()

        self.ts = TestSetupHelpers()
        self.create_metadata()
        self.doc_id = self.ts.ingest_file('eoc_post_campaign.csv')

    def test_get_computed_datapoint(self):
        get_data = {'document_id':self.doc_id}
    	resp = self.ts.get(self, '/api/v1/computed_datapoint/', get_data)
    	self.assertHttpOK(resp)
    	resp_data = self.deserialize(resp)
        db_data = DataPointComputed.objects.filter(document_id = self.doc_id).values()
    	self.assertEqual(len(resp_data['objects']), len(db_data))

    def test_get_computed_datapoint_no_data(self):
        resp = self.ts.get(self, '/api/v1/computed_datapoint/')
        self.assertHttpOK(resp)
        response_data = self.deserialize(resp)
        self.assertEqual(len(response_data['objects']), 0)

    def test_post_computed_datapoint(self):
        doc_id = Document.objects.create(doc_title='Data Entry').id
        indicator_id = Indicator.objects.all()[0].id
        campaign_id = Campaign.objects.all()[0].id
        location_id = Location.objects.all()[0].id
        # value indicator campaign location document_i
        data = {'document_id':doc_id,
            'indicator_id':indicator_id,
            'campaign_id':campaign_id,
            'location_id':location_id,
            'value':10
        }
        resp = self.ts.post(self, '/api/v1/computed_datapoint/', data)
        response_data = self.deserialize(resp)
        self.assertEqual(response_data['value'], 10.0)

    # def test_delete_computed_datapoint(self):
    #     # create a random cdp
    #     indicator_id = Indicator.objects.all()[0].id
    #     campaign_id = Campaign.objects.all()[0].id
    #     location_id = Location.objects.all()[0].id
    #     document_id = Document.objects.all()[0].id

    #     dpc = DataPointComputed.objects.create(
    #         indicator_id = indicator_id,
    #         campaign_id = campaign_id,
    #         location_id = location_id,
    #         document_id = document_id,
    #         value = 21)

    #     dpc_query = DataPointComputed.objects.filter(id = dpc.id)
    #     self.assertEqual(len(dpc_query), 1)

    #     delete_url = '/api/v1/computed_datapoint/%d/' %dpc.id

    #     resp = self.ts.delete(self, delete_url)

    #     print self.deserialize(resp)


    def create_metadata(self):
        '''
        Creating the Indicator, location, Campaign, meta data needed for the
        system to aggregate / caclulate.
        '''

        top_lvl_tag = IndicatorTag.objects.create(id = 1, tag_name='Polio')

        campaign_df = read_csv('rhizome/tests/_data/campaigns.csv')
        campaign_df['top_lvl_indicator_tag_id'] = top_lvl_tag.id

        campaign_df['start_date'] = to_datetime(campaign_df['start_date'])
        campaign_df['end_date'] = to_datetime(campaign_df['end_date'])

        location_df= read_csv('rhizome/tests/_data/locations.csv')
        indicator_df = read_csv('rhizome/tests/_data/indicators.csv')

        office_id = Office.objects.create(id=1,name='test').id

        cache_job_id = CacheJob.objects.create(id = -2, \
            date_attempted = '2015-01-01',is_error = False)

        campaign_type = CampaignType.objects.create(id=1,name="test")

        locations = self.model_df_to_data(location_df,Location)
        campaigns = self.model_df_to_data(campaign_df,Campaign)
        indicators = self.model_df_to_data(indicator_df,Indicator)
        self.user_id = User.objects.create_user('test','test@test.com', 'test').id
        self.mapped_location_id = locations[0].id
        loc_map = SourceObjectMap.objects.create(
            source_object_code = 'AF001039003000000000',
            content_type = 'location',
            mapped_by_id = self.user_id,
            master_object_id = self.mapped_location_id
        )

        source_campaign_string = '2016 March NID OPV'
        self.mapped_campaign_id = campaigns[0].id
        campaign_map = SourceObjectMap.objects.create(
            source_object_code = source_campaign_string,
            content_type = 'campaign',
            mapped_by_id = self.user_id,
            master_object_id = self.mapped_campaign_id
        )

        self.mapped_indicator_with_data = locations[2].id
        indicator_map = SourceObjectMap.objects.create(
            source_object_code = 'Percent missed due to other reasons',
            content_type = 'indicator',
            mapped_by_id = self.user_id,
            master_object_id = self.mapped_indicator_with_data
        )



    def model_df_to_data(self,model_df,model):

        meta_ids = []

        non_null_df = model_df.where((notnull(model_df)), None)
        list_of_dicts = non_null_df.transpose().to_dict()

        for row_ix, row_dict in list_of_dicts.iteritems():

            row_id = model.objects.create(**row_dict)
            meta_ids.append(row_id)

        return meta_ids
