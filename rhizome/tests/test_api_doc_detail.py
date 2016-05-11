from tastypie.test import ResourceTestCase
from setup_helpers import TestSetupHelpers
from rhizome.models import Document, DocDetailType, DocumentDetail

class DocDetailResourceTest(ResourceTestCase):

    def setUp(self):
        super(DocDetailResourceTest, self).setUp()
        self.ts = TestSetupHelpers();
        self.lt = self.ts.create_arbitrary_location_type()
        self.o = self.ts.create_arbitrary_office()
        self.top_lvl_location = self.ts.create_arbitrary_location(
            self.lt.id,
            self.o.id,
            location_code ='Nigeria',
            location_name='Nigeria')


    def test_post_doc_detail(self):
    	doc = Document.objects.create(doc_title='test')
    	doc_detail_type = DocDetailType.objects.create(name='test type')
    	url = '/api/v1/doc_detail/'
    	data = {
    		'document_id':doc.id, 
    		'doc_detail_type_id':doc_detail_type.id,
    		'doc_detail_value':1
		}
    	resp = self.ts.post(self, url, data=data)
    	self.assertHttpCreated(resp)

# WHY WON"T THIS TEST RUN???
	def test_get_doc_detail_by_type(self):
		doc = Document.objects.create(doc_title='test')
		doc_detail_type = DocDetailType.objects.create(name='test type')
		doc_detail = DocumentDetail.objects.create(document_id = doc.id,\
			doc_detail_type_id = doc_detail_type.id,\
			doc_detail_value = 1
		)
		url = '/api/v1/doc_detail/'
		data ={'doc_detail_type':doc_detail_type.id}
		resp = self.ts.get(self, url, data=data)
		self.assertHttpOk(resp)
		response_data = self.deserialize(resp)
		print response_data
    	# self.assertEqual(response_data[])
