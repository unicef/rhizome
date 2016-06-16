from base_test_case import RhizomeApiTestCase
from rhizome.models import DocDetailType
from rhizome.models import Document
from rhizome.models import DocumentDetail
from setup_helpers import TestSetupHelpers


class CacheMetaResourceTest(RhizomeApiTestCase):

    def setUp(self):
        super(CacheMetaResourceTest, self).setUp()

        self.ts = TestSetupHelpers()
        self.lt = self.ts.create_arbitrary_location_type()
        self.o = self.ts.create_arbitrary_office()
        self.top_lvl_location = self.ts.create_arbitrary_location(
            self.lt.id,
            self.o.id,
            location_code='Nigeria',
            location_name='Nigeria')

    def test_get(self):

        data = {  }
        resp = self.ts.get(self, '/api/v1/cache_meta/', data=data)

        response_data = self.deserialize(resp)
        self.assertHttpOK(resp)
        # self.assertEqual(len(response_data['objects']), 1)
        # self.assertEqual(response_data['objects'][0]['id'], doc_detail.id)
