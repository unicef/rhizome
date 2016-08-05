from base_test_case import RhizomeApiTestCase
from rhizome.tests.setup_helpers import TestSetupHelpers
from rhizome.simple_models import DataPoint, IndicatorTag, User, Office, CacheJob, LocationType, Document, DocDetailType, CampaignType, CalculatedIndicatorComponent, IndicatorToTag, DocumentDetail, SourceObjectMap, Location, Campaign, Indicator, DataPointComputed
from pandas import read_csv, notnull, to_datetime
from rhizome.etl_tasks.transform_upload import CampaignDocTransform


class RefreshMasterAPIResourceTest(RhizomeApiTestCase):

    def setUp(self):
        super(RefreshMasterAPIResourceTest, self).setUp()
        self.create_metadata()
        self.ts = TestSetupHelpers()

    def test_refresh(self):
        doc_id = self.ingest_file('eoc_post_campaign.csv')
        dt = CampaignDocTransform(self.user_id, doc_id)
        dt.main()
        self.assertEqual(DataPoint.objects.count(), 0)
        self.assertEqual(DataPointComputed.objects.count(), 0)
        get_data = {
            'document_id': doc_id
        }
        resp = self.ts.get(self, '/api/v1/refresh_master/', get_data)
        self.assertHttpOK(resp)
        response_data = self.deserialize(resp)
        self.assertEqual(DataPoint.objects.count(), 1)
        self.assertEqual(response_data['objects'][0]['id'], doc_id)

    def test_refresh_no_params(self):
        doc_id = self.ingest_file('eoc_post_campaign.csv')
        dt = CampaignDocTransform(self.user_id, doc_id)
        dt.main()
        self.assertEqual(DataPoint.objects.count(), 0)
        self.assertEqual(DataPointComputed.objects.count(), 0)
        resp = self.ts.get(self, '/api/v1/refresh_master/')
        self.assertHttpApplicationError(resp)

# HELPER FUNCTIONS:::

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
        calc_indicator_df = read_csv\
            ('rhizome/tests/_data/calculated_indicator_component.csv')

        user_id = User.objects.create_user('test', 'test@test.com', 'test').id
        self.user_id = user_id
        office_id = Office.objects.create(id=1, name='test').id

        cache_job_id = CacheJob.objects.create(id=-2,
                                               date_attempted='2015-01-01', is_error=False)

        self.location_type1 = LocationType.objects.create(admin_level=0,
                                                          name="country", id=1)
        self.location_type2 = LocationType.objects.create(admin_level=1,
                                                          name="province", id=2)

        document_id = Document.objects.create(
            doc_title='test',
            file_header='Campaign,Wardcode,uq_id,HHsampled,HHvisitedTEAMS,Marked0to59,UnImmun0to59,NOimmReas1,NOimmReas2,NOimmReas3,NOimmReas4,NOimmReas5,NOimmReas6,NOimmReas7,NOimmReas8,NOimmReas9,NOimmReas10,NOimmReas11,NOimmReas12,NOimmReas13,NOimmReas14,NOimmReas15,NOimmReas16,NOimmReas17,NOimmReas18,NOimmReas19,NOimmReas20,ZeroDose,TotalYoungest,YoungstRI,RAssessMrk,RCorctCAT,RIncorect,RXAssessMrk,RXCorctCAT,RXIncorect,STannounc,SRadio,STradlead,SReiliglead,SMosque,SNewspaper,SPoster,Sbanner,SRelative,SHworker,Scommmob,SNOTAWARE,Influence1,Influence2,Influence3,Influence4,Influence5,Influence6,Influence7,Influence8',
            created_by_id=user_id,
            guid='test').id

        for ddt in ['uq_id_column', 'username_column', 'image_col',
                    'date_column', 'location_column', 'location_display_name']:

            DocDetailType.objects.create(name=ddt)

        for rt in ["country", "settlement", "province", "district", "sub-district"]:
            DocDetailType.objects.create(name=rt)

        campaign_type = CampaignType.objects.create(id=1, name="test")

        self.locations = self.model_df_to_data(location_df, Location)
        self.campaigns = self.model_df_to_data(campaign_df, Campaign)
        self.indicators = self.model_df_to_data(indicator_df, Indicator)
        calc_indicator_ids = self.model_df_to_data(calc_indicator_df,
                                                   CalculatedIndicatorComponent)

        ## associate indicators with tag ##
        indicator_to_tag_ids = [IndicatorToTag(**{
            'indicator_id': ind.id,
            'indicator_tag_id': top_lvl_tag.id}) for ind in self.indicators]

        IndicatorToTag.objects.bulk_create(indicator_to_tag_ids)

        ## create the uq_id_column configuration ##

        uq_id_config = DocumentDetail.objects.create(
            document_id=document_id,
            doc_detail_type_id=DocDetailType
            .objects.get(name='uq_id_column').id,
            doc_detail_value='uq_id'
        )

        location_column_config = DocumentDetail.objects.create(
            document_id=document_id,
            doc_detail_type_id=DocDetailType
            .objects.get(name='location_column').id,
            doc_detail_value='Wardcode'
        )

        date_column_config = DocumentDetail.objects.create(
            document_id=document_id,
            doc_detail_type_id=DocDetailType
            .objects.get(name='date_column').id,
            doc_detail_value='submission_date'
        )

        self.mapped_location_id = self.locations[0].id
        loc_map = SourceObjectMap.objects.create(
            source_object_code='AF001039003000000000',
            content_type='location',
            mapped_by_id=user_id,
            master_object_id=self.mapped_location_id
        )

        source_campaign_string = '2016 March NID OPV'
        self.mapped_campaign_id = self.campaigns[0].id
        campaign_map = SourceObjectMap.objects.create(
            source_object_code=source_campaign_string,
            content_type='campaign',
            mapped_by_id=user_id,
            master_object_id=self.mapped_campaign_id
        )
        self.mapped_indicator_id_0 = self.indicators[0].id
        indicator_map = SourceObjectMap.objects.create(
            source_object_code='Percent missed children_PCA',
            content_type='indicator',
            mapped_by_id=user_id,
            master_object_id=self.mapped_indicator_id_0
        )

        self.mapped_indicator_with_data = self.locations[2].id
        indicator_map = SourceObjectMap.objects.create(
            source_object_code='Percent missed due to other reasons',
            content_type='indicator',
            mapped_by_id=user_id,
            master_object_id=self.mapped_indicator_with_data
        )

    def ingest_file(self, file_name):
        ## create one doc ##
        document = Document.objects.create(
            doc_title=file_name,
            created_by_id=self.user_id,
            guid='test')
        document.docfile = file_name
        document.save()
        return document.id

    def model_df_to_data(self, model_df, model):

        meta_ids = []

        non_null_df = model_df.where((notnull(model_df)), None)
        list_of_dicts = non_null_df.transpose().to_dict()

        for row_ix, row_dict in list_of_dicts.iteritems():

            row_id = model.objects.create(**row_dict)
            meta_ids.append(row_id)

        return meta_ids
