from base_test_case import RhizomeApiTestCase
from rhizome.models import CacheJob, Office, Indicator, Location,\
    LocationType, DataPointComputed, CampaignType, Campaign, IndicatorTag,\
    LocationPermission, Document
from setup_helpers import TestSetupHelpers
from rhizome.etl_tasks.transform_upload import ComplexDocTransform
from rhizome.models import SourceObjectMap, SourceSubmission

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
            document_docfile='eoc_post_campaign.csv')
        dt = ComplexDocTransform(self.ts.user.id, doc.id)
        dt.main()
        get_data = {'document_id': doc.id}
        resp = self.ts.get(self, '/api/v1/source_submission/', get_data)
        self.assertHttpOK(resp)
        resp_data = self.deserialize(resp)
        self.assertEqual(len(SourceSubmission.objects.all()),
                         len(resp_data['objects']))

    def test_get_source_submission_by_id(self):
        doc = self.ts.create_arbitrary_document(
            document_docfile='eoc_post_campaign.csv')
        dt = ComplexDocTransform(self.ts.user.id, doc.id)
        dt.main()
        ss_id = SourceSubmission.objects.all()[0].id
        get_data = {'id': ss_id}
        resp = self.ts.get(self, '/api/v1/source_submission/', get_data)
        self.assertHttpOK(resp)
        resp_data = self.deserialize(resp)
        self.assertEqual(resp_data['objects'][0]['id'], ss_id)
