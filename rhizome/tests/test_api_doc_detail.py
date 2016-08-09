from rhizome.tests.base_test_case import RhizomeApiTestCase
from rhizome.tests.setup_helpers import TestSetupHelpers
from rhizome.models.document_models import Document, DocDetailType,\
    DocumentDetail

class DocDetailResourceTest(RhizomeApiTestCase):

    def setUp(self):
        super(DocDetailResourceTest, self).setUp()
        self.ts = TestSetupHelpers()
        self.lt = self.ts.create_arbitrary_location_type()
        self.top_lvl_location = self.ts.create_arbitrary_location(
            self.lt.id,
            location_code='Nigeria',
            location_name='Nigeria')

    def test_post_doc_detail(self):
        doc = Document.objects.create(doc_title='test')
        doc_detail_type = DocDetailType.objects.create(name='test type')
        url = '/api/v1/doc_detail/'
        value = 1232
        data = {
            'document_id': doc.id,
            'doc_detail_type_id': doc_detail_type.id,
            'doc_detail_value': value
        }
        resp = self.ts.post(self, url, data=data)
        self.assertHttpCreated(resp)
        response_data = self.deserialize(resp)
        self.assertEqual(response_data['doc_detail_value'], value)

    def test_get_doc_detail_by_type(self):
        doc = Document.objects.create(doc_title='test')
        doc_detail_type = DocDetailType.objects.create(name='test type')
        doc_detail = DocumentDetail.objects.create(document_id=doc.id,
                                                   doc_detail_type_id=doc_detail_type.id,
                                                   doc_detail_value=1
                                                   )
        url = '/api/v1/doc_detail/'
        data = {'doc_detail_type': doc_detail_type.name}
        resp = self.ts.get(self, url, data=data)
        self.assertHttpOK(resp)
        response_data = self.deserialize(resp)
        self.assertEqual(len(response_data['objects']), 1)
        self.assertEqual(response_data['objects'][0]['id'], doc_detail.id)

    def test_get_doc_detail_by_id(self):
        doc = Document.objects.create(doc_title='test')
        doc_detail_type = DocDetailType.objects.create(name='test type')
        doc_detail = DocumentDetail.objects.create(document_id=doc.id,
                                                   doc_detail_type_id=doc_detail_type.id,
                                                   doc_detail_value=1
                                                   )
        url = '/api/v1/doc_detail/'
        data = {'document_id': doc.id}
        resp = self.ts.get(self, url, data=data)
        self.assertHttpOK(resp)
        response_data = self.deserialize(resp)
        self.assertEqual(len(response_data['objects']), 1)
        self.assertEqual(response_data['objects'][0]['id'], doc_detail.id)

    def test_get_all_doc_detail(self):
        doc = Document.objects.create(doc_title='test')
        doc_2 = Document.objects.create(doc_title='test2')
        doc_detail_type = DocDetailType.objects.create(name='test type')
        doc_detail_1 = DocumentDetail.objects.create(document_id=doc.id,
                                                     doc_detail_type_id=doc_detail_type.id,
                                                     doc_detail_value=1
                                                     )
        doc_detail_2 = DocumentDetail.objects.create(document_id=doc_2.id,
                                                     doc_detail_type_id=doc_detail_type.id,
                                                     doc_detail_value=1
                                                     )
        url = '/api/v1/doc_detail/'
        resp = self.ts.get(self, url)
        self.assertHttpOK(resp)
        response_data = self.deserialize(resp)
        self.assertEqual(len(response_data['objects']), 2)
