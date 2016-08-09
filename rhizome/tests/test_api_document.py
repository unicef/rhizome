import base64
import os

from pandas import read_csv, notnull, to_datetime
from django.contrib.auth.models import User

from rhizome.models.office_models import Office
from rhizome.models.campaign_models import Campaign, CampaignType, \
    DataPointComputed
from rhizome.models.location_models import Location, LocationType, LocationPermission
from rhizome.models.indicator_models import Indicator, IndicatorTag
from rhizome.models.document_models import Document, SourceObjectMap, DataPoint

from rhizome.tests.setup_helpers import TestSetupHelpers
from rhizome.tests.base_test_case import RhizomeApiTestCase

from rhizome.cache_meta import LocationTreeCache

class DocumentResourceTest(RhizomeApiTestCase):

    def setUp(self):
        super(DocumentResourceTest, self).setUp()
        self.ts = TestSetupHelpers()
        self.create_metadata()

    def test_obj_create(self):
        path = os.path.join(os.path.dirname(__file__),
                            '_data/eoc_post_campaign.csv')
        file = open(path).read()
        encoded_data = base64.b64encode(file)
        post_data = {'docfile': encoded_data,
                     'file_type': 'campaign',
                     'doc_title': 'eoc_post_campaign.csv'}
        resp = self.ts.post(self, '/api/v1/source_doc/', post_data)
        self.deserialize(resp)
        self.assertHttpCreated(resp)

    def test_xlsx_transform(self):
        path = os.path.join(os.path.dirname(__file__),
                            '_data/eoc_post_campaign.xlsx')
        f = open(path).read()
        encoded_data = base64.b64encode(f)
        post_data = {'docfile': encoded_data,
                     'file_type': 'campaign',
                     'doc_title': 'eoc_post_campaign.xlsx'}
        resp = self.ts.post(self, '/api/v1/source_doc/', post_data)
        self.assertHttpCreated(resp)
        resp_data = self.deserialize(resp)

        get_data = {'document_id':resp_data['id']}
        ## this right here emulates what happens when the user clicks the
        ## `refresh master` button
        resp = self.ts.get(self, '/api/v1/transform_upload/', get_data)

        the_value_from_the_database = DataPointComputed.objects.get(
            campaign_id=self.mapped_campaign_id,
            indicator_id=self.mapped_indicator_with_data,
            location_id=self.mapped_location_id
        ).value

        some_cell_value_from_the_file = 0.082670906
        # FIXME find this from the data frame by selecting the cell where we
        # have mapped the data..

        self.assertEqual(some_cell_value_from_the_file, \
            the_value_from_the_database)

    def test_upload_empty_csv(self):
        file_name = '_data/empty_csv.csv'
        path = os.path.join(os.path.dirname(__file__), file_name)
        file = open(path).read()
        encoded_data = base64.b64encode(file)
        post_data = {'docfile': encoded_data, 'file_type': 'campaign', \
            'doc_title': 'empty_csv.csv'}
        resp = self.ts.post(self, '/api/v1/source_doc/', post_data)
        self.assertHttpApplicationError(resp)

    def test_upload_empty_excel(self):
        file_name = '_data/empty_xlsx.xlsx'
        path = os.path.join(os.path.dirname(__file__), file_name)
        file = open(path).read()
        encoded_data = base64.b64encode(file)
        post_data = {'docfile': encoded_data,'file_type': 'campaign',\
            'doc_title': 'empty_xlsx.xlsx'}
        resp = self.ts.post(self, '/api/v1/source_doc/', post_data)
        self.assertHttpApplicationError(resp)

    def test_post_no_doc_title(self):
        path = os.path.join(os.path.dirname(__file__),
                            '_data/eoc_post_campaign.csv')
        file = open(path).read()
        encoded_data = base64.b64encode(file)
        post_data = {'docfile': encoded_data,'file_type': 'campaign'}
        resp = self.ts.post(self, '/api/v1/source_doc/', post_data)
        self.assertHttpApplicationError(resp)

    def create_metadata(self):
        '''
        Creating the Indicator, location, Campaign, meta data needed for the
        system to aggregate / caclulate.
        '''

        top_lvl_tag = IndicatorTag.objects.create(id=1, tag_name='Polio')

        campaign_df = read_csv('rhizome/tests/_data/campaigns.csv')
        campaign_df['top_lvl_indicator_tag_id'] = top_lvl_tag.id

        campaign_df['start_date'] = to_datetime(campaign_df['start_date'])
        campaign_df['end_date'] = to_datetime(campaign_df['end_date'])

        location_df = read_csv('rhizome/tests/_data/locations.csv')
        indicator_df = read_csv('rhizome/tests/_data/indicators.csv')

        office_id = Office.objects.create(id=1, name='test').id

        campaign_type = CampaignType.objects.create(id=1, name="test")

        locations = self.model_df_to_data(location_df, Location)
        campaigns = self.model_df_to_data(campaign_df, Campaign)
        indicators = self.model_df_to_data(indicator_df, Indicator)
        self.user_id = User.objects.create_user(
            'test', 'test@test.com', 'test').id
        self.mapped_location_id = locations[0].id
        loc_map = SourceObjectMap.objects.create(
            source_object_code='AF001039003000000000',
            content_type='location',
            mapped_by_id=self.user_id,
            master_object_id=self.mapped_location_id
        )

        source_campaign_string = '2016 March NID OPV'
        self.mapped_campaign_id = campaigns[0].id
        campaign_map = SourceObjectMap.objects.create(
            source_object_code=source_campaign_string,
            content_type='campaign',
            mapped_by_id=self.user_id,
            master_object_id=self.mapped_campaign_id
        )
        self.mapped_indicator_id_0 = indicators[0].id
        indicator_map = SourceObjectMap.objects.create(
            source_object_code='Percent missed children_PCA',
            content_type='indicator',
            mapped_by_id=self.user_id,
            master_object_id=self.mapped_indicator_id_0
        )

        self.mapped_indicator_with_data = locations[2].id
        indicator_map = SourceObjectMap.objects.create(
            source_object_code='Percent missed due to other reasons',
            content_type='indicator',
            mapped_by_id=self.user_id,
            master_object_id=self.mapped_indicator_with_data
        )
        ltc = LocationTreeCache()
        ltc.main()

    def model_df_to_data(self, model_df, model):

        meta_ids = []

        non_null_df = model_df.where((notnull(model_df)), None)
        list_of_dicts = non_null_df.transpose().to_dict()

        for row_ix, row_dict in list_of_dicts.iteritems():

            row_id = model.objects.create(**row_dict)
            meta_ids.append(row_id)

        return meta_ids
