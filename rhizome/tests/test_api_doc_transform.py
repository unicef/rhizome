from base_test_case import RhizomeApiTestCase
from rhizome.models import CacheJob, Office, Indicator, Location,\
    LocationType, DataPointComputed, CampaignType, Campaign, IndicatorTag,\
    LocationPermission, Document, SourceObjectMap, IndicatorClassMap, DataPoint
from rhizome.tests.setup_helpers import TestSetupHelpers
from datetime import datetime

from rhizome.cache_meta import LocationTreeCache


class DocTransformResourceTest(RhizomeApiTestCase):

    def setUp(self):
        super(DocTransformResourceTest, self).setUp()
        self.ts = TestSetupHelpers()
        self.ts.load_some_metadata()

        ltr = LocationTreeCache()
        ltr.main()

        self.mapped_location_id = self.ts.locations[0].id
        self.mapped_location_id_2 = self.ts.locations[1].id

        self.loc_map = SourceObjectMap.objects.create(
            source_object_code='AF001039003000000000',
            content_type='location',
            mapped_by_id=self.ts.user.id,
            master_object_id=self.mapped_location_id
        )

        source_campaign_string = '2016 March NID OPV'
        self.mapped_campaign_id = self.ts.campaigns[0].id
        self.campaign_map = SourceObjectMap.objects.create(
            source_object_code=source_campaign_string,
            content_type='campaign',
            mapped_by_id=self.ts.user.id,
            master_object_id=self.mapped_campaign_id
        )
        self.mapped_indicator_with_data = self.ts.locations[2].id
        self.indicator_map = SourceObjectMap.objects.create(
            source_object_code='Percent missed due to other reasons',
            content_type='indicator',
            mapped_by_id=self.ts.user.id,
            master_object_id=self.mapped_indicator_with_data
        )

    def test_doc_transform(self):
        doc = self.ts.create_arbitrary_document(
            document_docfile='eoc_post_campaign.csv')
        get_data = {'document_id': doc.id, 'file_type':'multi_campaign'}
        resp = self.ts.get(self, '/api/v1/transform_upload/', get_data)

        self.assertHttpOK(resp)
        self.assertEqual(len(self.deserialize(resp)['objects']), 1)
        self.assertEqual(DataPointComputed.objects.all()[0].value, 0.082670906)

    def test_data_date_transform(self):
        DataPoint.objects.all().delete()
        loc_map = SourceObjectMap.objects.create(
            source_object_code='AF001047005000000000',
            content_type='location',
            mapped_by_id=self.ts.user.id,
            master_object_id=self.mapped_location_id
        )

        self.mapped_indicator_with_data = self.ts.indicators[2].id

        self.indicator_map = SourceObjectMap.objects.create(
            source_object_code='polio_case',
            content_type='indicator',
            mapped_by_id=self.ts.user.id,
            master_object_id=self.mapped_indicator_with_data
        )
        doc = self.ts.create_arbitrary_document('AfgPolioCases.csv')
        get_data = {'document_id': doc.id, 'file_type':'date_file'}
        resp = self.ts.get(self, '/api/v1/transform_upload/', get_data)
        self.assertHttpOK(resp)
        self.assertEqual(len(self.deserialize(resp)['objects']), 1)
        data_date = datetime(2014, 9, 1, 0, 0)
        dp = DataPoint.objects.filter(location_id=self.mapped_location_id,
                                      indicator=self.mapped_indicator_with_data,
                                      data_date=data_date)
        self.assertEqual(len(dp), 1)
        self.assertEqual(1, dp[0].value)

    def test_doc_transform_with_zeros(self):
        doc = self.ts.create_arbitrary_document(
            document_docfile='zero_val_test.csv')
        get_data = {'document_id': doc.id, 'file_type':'multi_campaign'}
        resp = self.ts.get(self, '/api/v1/transform_upload/', get_data)
        self.assertHttpOK(resp)
        self.assertEqual(len(self.deserialize(resp)['objects']), 1)
        self.assertEqual(DataPointComputed.objects.all()[0].value, 0.0)

    def test_doc_transform_no_document_id(self):
        resp = self.ts.get(self, '/api/v1/transform_upload/')
        self.assertHttpApplicationError(resp)

    # datapoint should be overwritten for unique location/campaign/indicator
    def test_duplicate_datapoint_campaign(self):
        # upload document and run transform
        doc = self.ts.create_arbitrary_document(
            document_docfile='eoc_post_campaign.csv')
        get_data = {'document_id': doc.id, 'file_type':'multi_campaign'}
        resp = self.ts.get(self, '/api/v1/transform_upload/', get_data)
        self.assertHttpOK(resp)
        self.assertEqual(DataPointComputed.objects.all()[0].value, 0.082670906)

        # upload and transform again:
        doc_2 = self.ts.create_arbitrary_document(
            document_docfile='eoc_post_campaign_2.csv', doc_title='eoc_post_campaign_2.csv')
        get_data_2 = {'document_id': doc_2.id, 'file_type':'multi_campaign'}
        resp_2 = self.ts.get(self, '/api/v1/transform_upload/', get_data_2)
        self.assertHttpOK(resp_2)

        # the datapoint should be overwritten
        self.assertEqual(DataPoint.objects.count(), 1)
        # make sure we have the new value
        self.assertEqual(DataPointComputed.objects.all()[0].value, 0.9)

    # datapoint should be overwritten for unique location/data_date/indicator
    def test_duplicate_datapoint_data_date(self):
        # create required metadata
        loc_map = SourceObjectMap.objects.create(
            source_object_code='AF001047005000000000',
            content_type='location',
            mapped_by_id=self.ts.user.id,
            master_object_id=self.mapped_location_id
        )

        self.mapped_indicator_with_data = self.ts.indicators[2].id

        self.indicator_map = SourceObjectMap.objects.create(
            source_object_code='polio_case',
            content_type='indicator',
            mapped_by_id=self.ts.user.id,
            master_object_id=self.mapped_indicator_with_data
        )
        doc = self.ts.create_arbitrary_document(
            document_docfile='AfgPolioCases.csv', doc_title='AfgPolioCases.csv')
        get_data = {'document_id': doc.id, 'file_type': 'date_file'}
        resp = self.ts.get(self, '/api/v1/transform_upload/', get_data)
        self.assertHttpOK(resp)
        data_date = datetime(2014, 9, 1, 0, 0)
        dp = DataPoint.objects.filter(location_id=self.mapped_location_id,
                                      indicator=self.mapped_indicator_with_data,
                                      data_date=data_date)
        self.assertEqual(len(dp), 1)
        self.assertEqual(1, dp[0].value)

        # do it again
        doc = self.ts.create_arbitrary_document(
            document_docfile='AfgPolioCases_2.csv', doc_title='AfgPolioCases_2.csv')
        get_data = {'document_id': doc.id, 'file_type': 'date_file'}
        resp = self.ts.get(self, '/api/v1/transform_upload/', get_data)
        data_date = datetime(2014, 9, 1, 0, 0)
        dp = DataPoint.objects.filter(location_id=self.mapped_location_id,
                                      indicator=self.mapped_indicator_with_data,
                                      data_date=data_date)
        self.assertEqual(len(dp), 1)
        self.assertEqual(2, dp[0].value)

    def test_class_indicator(self):
        # create required metadata

        self.mapped_indicator_with_data = self.ts.indicators[2].id

        loc_map = SourceObjectMap.objects.create(
            source_object_code='AF001039006000000000',
            content_type='location',
            mapped_by_id=self.ts.user.id,
            master_object_id=self.mapped_location_id_2
        )

        self.indicator_map = SourceObjectMap.objects.create(
            source_object_code='LQAS',
            content_type='indicator',
            mapped_by_id=self.ts.user.id,
            master_object_id=self.mapped_indicator_with_data
        )

        IndicatorClassMap.objects.create(
            indicator_id=self.mapped_indicator_with_data,
            string_value='pass',
            enum_value=1,
            is_display=True
        )

        doc = self.ts.create_arbitrary_document(
            document_docfile='lqas_test.csv', doc_title='lqas_test.csv')
        get_data = {'document_id': doc.id, 'file_type': 'multi_campaign'}
        resp = self.ts.get(self, '/api/v1/transform_upload/', get_data)
        self.deserialize(resp)

        dp_count = DataPoint.objects.count()

        self.assertEqual(dp_count, 1)
