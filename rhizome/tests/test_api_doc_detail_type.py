from tastypie.test import ResourceTestCase
from setup_helpers import TestSetupHelpers
from rhizome.models import DocDetailType

class DocDetailTypeResourceTest(ResourceTestCase):
    def setUp(self):

        ## instantiate the test client and all other methods ##
        super(DocDetailTypeResourceTest, self).setUp()

        self.ts = TestSetupHelpers()
        self.lt = self.ts.create_arbitrary_location_type()
        self.o = self.ts.create_arbitrary_office()
        self.top_lvl_location = self.ts.create_arbitrary_location(
            self.lt.id,
            self.o.id,
            location_code ='Nigeria',
            location_name='Nigeria')

    def test_doc_detail_type(self):
        ddt = DocDetailType.objects.create(name="ddt")
        ddt_2 = DocDetailType.objects.create(name="ddt2")
        url = '/api/v1/doc_detail_type/'
        resp = self.ts.get(self, url)
        response_data = self.deserialize(resp)
        self.assertHttpOK(resp)
        self.assertEqual(len(response_data['objects']), 2)