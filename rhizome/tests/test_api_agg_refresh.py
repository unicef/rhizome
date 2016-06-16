from rhizome.tests.setup_helpers import TestSetupHelpers
from pandas import read_csv
from rhizome.models import User, Office, CacheJob, LocationType, CampaignType,\
    Campaign, Document, SourceSubmission, IndicatorTag, DataPoint, Location,\
    Indicator, DataPointComputed
from base_test_case import RhizomeApiTestCase


class AggRefreshAPITestCase(RhizomeApiTestCase):
    # ./manage.py test rhizome.tests.test_api_agg_refresh.AggRefreshAPITestCase --settings=rhizome.settings.test

    def setUp(self):
        super(AggRefreshAPITestCase, self).setUp()
        self.ts = TestSetupHelpers()

        # create some metadata
        user_id = User.objects.create_user('test', 'john@john.com', 'test').id
        self.office_id = Office.objects.create(id=1, name='test').id
        cache_job_id = CacheJob.objects.create(
            id=-1, date_completed='2015-01-01', date_attempted='2015-01-01', is_error=False)
        self.location_type1 = LocationType.objects.create(admin_level=0,
                                                          name="country", id=1)
        self.location_type2 = LocationType.objects.create(admin_level=1,
                                                          name="province", id=2)

        location_df = read_csv('rhizome/tests/_data/locations.csv')
        indicator_df = read_csv('rhizome/tests/_data/indicators.csv')

        self.locations = self.ts.model_df_to_data(location_df, Location)
        self.indicators = self.ts.model_df_to_data(indicator_df, Indicator)

        campaign_type1 = CampaignType.objects.create(name='test')
        ind_tag = IndicatorTag.objects.create(tag_name='Polio')

        self.campaign_id = Campaign.objects.create(
            start_date='2016-01-01',
            end_date='2016-01-02',
            campaign_type_id=campaign_type1.id,
            top_lvl_location_id=12907,
            top_lvl_indicator_tag_id=ind_tag.id,
            office_id=self.office_id,
        ).id

        document = Document.objects.create(
            doc_title='test',
            created_by_id=user_id,
            guid='test')

        self.ss_1 = SourceSubmission.objects.create(
            document_id=document.id,
            submission_json='',
            row_number=0,
            data_date='2016-01-01'
        ).id

        # create a couple datapoints

        dp_1 = DataPoint.objects.create(
            location_id=self.locations[21].id,
            indicator_id=self.indicators[0].id,
            campaign_id=self.campaign_id,
            value=1,
            data_date='2016-01-01',
            cache_job_id=-1,
            source_submission_id=self.ss_1,
            unique_index=1

        )

        dp_2 = DataPoint.objects.create(
            location_id=self.locations[22].id,
            indicator_id=self.indicators[0].id,
            campaign_id=self.campaign_id,
            value=1,
            data_date='2016-01-01',
            cache_job_id=-1,
            source_submission_id=self.ss_1,
            unique_index=2

        )

    def test_agg_refresh(self):
        '''
        When i pass a campaign the agg refresh should happen for that campaign,
        and i should get a queryset that has the top 10 datapoints with the
        given campaign
        '''
        url = '/api/v1/agg_refresh/'
        data = {'campaign_id': self.campaign_id}
        resp = self.ts.get(self, url, data=data)

        self.assertHttpOK(resp)

        response_data = self.deserialize(resp)
        response_objects = response_data['objects']
        db_objects = DataPointComputed.objects.all()

        self.assertEqual(len(response_objects), len(db_objects))

    def test_agg_refresh_no_campaign(self):
        url = '/api/v1/agg_refresh/'
        resp = self.ts.get(self, url)
        response_data = self.deserialize(resp)
        self.assertHttpOK(resp)

        response_data = self.deserialize(resp)
        response_objects = response_data['objects']
        db_objects = DataPointComputed.objects.all()

        all_campaigns = Campaign.objects.all().values()
        self.assertEqual(len(response_objects), len(db_objects))

    def test_invalid_campaign_id(self):
        url = '/api/v1/agg_refresh/'
        data = {'campaign_id': 12345}
        resp = self.ts.get(self, url, data=data)
        self.assertHttpApplicationError(resp)
