from django.test import TestCase
from tastypie.test import ResourceTestCase
from tastypie.models import ApiKey
from django.contrib.auth.models import User
from rhizome.models import CacheJob, Office, Indicator, Location,\
    LocationType, DataPointComputed, CampaignType, Campaign, IndicatorTag,\
    LocationPermission, Document
from setup_helpers import TestSetupHelpers
from pandas import read_csv, notnull, to_datetime
import base64
import os
from pandas import read_excel
from rhizome.etl_tasks.simple_upload_transform import SimpleDocTransform
from rhizome.models import *

from rhizome.cache_meta import LocationTreeCache

class DocTransformResourceTest(ResourceTestCase):
    def setUp(self):
        super(DocTransformResourceTest, self).setUp()
        self.ts = TestSetupHelpers()
        self.ts.load_some_metadata()
        ltr = LocationTreeCache()
        ltr.main()

        self.mapped_location_id = self.ts.locations[0].id
        self.loc_map = SourceObjectMap.objects.create(
            source_object_code = 'AF001039003000000000',
            content_type = 'location',
            mapped_by_id = self.ts.user.id,
            master_object_id = self.mapped_location_id
        )

        source_campaign_string = '2016 March NID OPV'
        self.mapped_campaign_id = self.ts.campaigns[0].id
        self.campaign_map = SourceObjectMap.objects.create(
            source_object_code = source_campaign_string,
            content_type = 'campaign',
            mapped_by_id = self.ts.user.id,
            master_object_id = self.mapped_campaign_id
        )
        self.mapped_indicator_with_data = self.ts.locations[2].id
        self.indicator_map = SourceObjectMap.objects.create(
            source_object_code = 'Percent missed due to other reasons',
            content_type = 'indicator',
            mapped_by_id = self.ts.user.id,
            master_object_id = self.mapped_indicator_with_data
        )


    def test_doc_transform(self):
        doc = self.ts.create_arbitrary_document(document_docfile='eoc_post_campaign.csv')
        get_data = {'document_id':doc.id}
        resp = self.ts.get(self, '/api/v1/transform_upload/', get_data)

        self.assertHttpOK(resp)
        self.assertEqual(len(self.deserialize(resp)['objects']), 1)
        self.assertEqual(DataPointComputed.objects.all()[0].value, 0.082670906)
