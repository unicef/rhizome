from rhizome.tests.base_test_case import RhizomeApiTestCase
from rhizome.tests.setup_helpers import TestSetupHelpers

from rhizome.models.indicator_models import IndicatorTag, Indicator
from rhizome.models.location_models import Location, LocationType, \
    LocationPermission
from rhizome.models.datapoint_models import CacheJob, DataPointComputed
from rhizome.models.document_models import Document, SourceObjectMap, SourceSubmission

from rhizome.etl_tasks.transform_upload import CampaignDocTransform
from rhizome.cache_meta import LocationTreeCache


class SourceSubmissionResourceTest(RhizomeApiTestCase):

    def setUp(self):
        super(SourceSubmissionResourceTest, self).setUp()
        self.ts = TestSetupHelpers()
        self.ts.load_some_metadata()
        ltr = LocationTreeCache()
        ltr.main()
        self.mapped_location_id = self.ts.locations[0].id
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

    def test_get_source_submission_by_doc(self):
        doc = self.ts.create_arbitrary_document(
            file_type = 'campaign',
            document_docfile='eoc_post_campaign.csv')
        doc.transform_upload()
        get_data = {'document_id': doc.id}
        resp = self.ts.get(self, '/api/v1/source_submission/', get_data)
        self.assertHttpOK(resp)
        resp_data = self.deserialize(resp)
        self.assertEqual(len(SourceSubmission.objects.all()),
                         len(resp_data['objects']))

    def test_get_source_submission_by_id(self):
        doc = self.ts.create_arbitrary_document(
            document_docfile='eoc_post_campaign.csv', file_type='campaign')
        doc.transform_upload()
        ss_id = SourceSubmission.objects.all()[0].id
        resp = self.ts.get(self, '/api/v1/source_submission/%s/' % ss_id)
        self.assertHttpOK(resp)
        resp_data = self.deserialize(resp)
        self.assertEqual(resp_data['id'], ss_id)
