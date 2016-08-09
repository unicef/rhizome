from rhizome.tests.base_test_case import RhizomeApiTestCase

from rhizome.models.office_models import Office
from rhizome.models.campaign_models import Campaign, DataPointComputed
from rhizome.models.location_models import Location, LocationType, \
    LocationPermission
from rhizome.models.indicator_models import Indicator, IndicatorTag
from rhizome.models.document_models import Document, SourceObjectMap, \
    SourceSubmission, DataPoint

from rhizome.tests.setup_helpers import TestSetupHelpers
from datetime import datetime

from rhizome.cache_meta import LocationTreeCache


class DocTransformResourceTest(RhizomeApiTestCase):
    # ./manage.py test rhizome.tests.test_api_doc_transform.DocTransformResourceTest.test_doc_transform --settings=rhizome.settings.test

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
        # ./manage.py test rhizome.tests.test_api_doc_transform.DocTransformResourceTest.test_doc_transform --settings=rhizome.settings.test
        doc = self.ts.create_arbitrary_document(
            document_docfile='eoc_post_campaign.csv', file_type='campaign')
        get_data = {'document_id': doc.id}
        resp = self.ts.get(self, '/api/v1/transform_upload/', get_data)

        ss_list = SourceSubmission.objects.filter(document_id = doc.id)\
            .values_list('id', flat=True)

        self.assertHttpOK(resp)
        self.assertEqual(len(self.deserialize(resp)['objects']), 1)
        self.assertEqual(DataPointComputed.objects.all()[0].value, 0.082670906)

    def test_data_date_transform(self):
        DataPoint.objects.all().delete()
        loc_map = SourceObjectMap.objects.create(
            source_object_code='AF001054001000000000',
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
        doc = self.ts.create_arbitrary_document('AfgPolioCases.csv', \
            file_type='date')
        get_data = {'document_id': doc.id, 'file_type':'date_file'}
        resp = self.ts.get(self, '/api/v1/transform_upload/', get_data)
        self.assertHttpOK(resp)
        self.assertEqual(len(self.deserialize(resp)['objects']), 1)
        ## check out the date format in the test data -- `17-7-2015`
        data_date = datetime(2015, 07, 17, 0, 0)
        single_dp = DataPoint.objects.filter(location_id=self.mapped_location_id,
                                      indicator=self.mapped_indicator_with_data,
                                      data_date=data_date)
        self.assertEqual(len(single_dp), 1)
        self.assertEqual(1, single_dp[0].value)

        all_achin_dps = DataPoint.objects\
            .filter(location_id=self.mapped_location_id,
                    indicator=self.mapped_indicator_with_data,
                    data_date__gt='2000-01-01', data_date__lt='2020-01-01')

        self.assertEqual(len(all_achin_dps), 6)

    def test_doc_transform_with_zeros(self):
        doc = self.ts.create_arbitrary_document(
            document_docfile='zero_val_test.csv', file_type='campaign')
        get_data = {'document_id': doc.id}
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
            document_docfile='eoc_post_campaign.csv', file_type='campaign')
        get_data = {'document_id': doc.id}
        resp = self.ts.get(self, '/api/v1/transform_upload/', get_data)
        self.assertHttpOK(resp)
        self.assertEqual(DataPointComputed.objects.all()[0].value, 0.082670906)

        # upload and transform again:
        doc_2 = self.ts.create_arbitrary_document(
            document_docfile='eoc_post_campaign_2.csv',
            doc_title='eoc_post_campaign_2.csv',file_type='campaign')
        get_data_2 = {'document_id': doc_2.id}
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
            source_object_code='AF001054001000000000',
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
            document_docfile='AfgPolioCases.csv',
            doc_title='AfgPolioCases.csv',
            file_type='date'
        )
        get_data = {'document_id': doc.id}
        resp = self.ts.get(self, '/api/v1/transform_upload/', get_data)
        self.assertHttpOK(resp)

        cases = DataPoint.objects.filter(location_id=self.mapped_location_id,
                                      indicator=self.mapped_indicator_with_data)

        self.assertEqual(len(cases), 6)

            # do it again, the case count should be 6 not 12
        doc = self.ts.create_arbitrary_document(
            document_docfile='AfgPolioCases_2.csv',
            doc_title='AfgPolioCases_2.csv',
            file_type = 'date'
        )
        get_data = {'document_id': doc.id}
        resp = self.ts.get(self, '/api/v1/transform_upload/', get_data)

        cases_2 = DataPoint.objects.filter(location_id=self.mapped_location_id,
                                      indicator=self.mapped_indicator_with_data)
        self.assertEqual(len(cases_2), 6)
        sum_of_cases = sum([dp.value for dp in cases_2])

        self.assertEqual(6, sum_of_cases)

    def _class_indicator(self):
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

        # IndicatorClassMap.objects.create(
        #     indicator_id=self.mapped_indicator_with_data,
        #     string_value='pass',
        #     is_display=True
        # )

        doc = self.ts.create_arbitrary_document(
            file_type = 'campaign',
            document_docfile='lqas_test.csv',
            doc_title='lqas_test.csv'
        )
        get_data = {'document_id': doc.id}
        resp = self.ts.get(self, '/api/v1/transform_upload/', get_data)
        self.deserialize(resp)

        dp_count = DataPoint.objects.count()

        self.assertEqual(dp_count, 1)
