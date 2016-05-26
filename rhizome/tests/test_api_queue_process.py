from tastypie.test import ResourceTestCase
from rhizome.models import DocDetailType
from rhizome.models import Document
from rhizome.models import DocumentDetail
from setup_helpers import TestSetupHelpers


class QueueProcessResourceTest(ResourceTestCase):
	def setUp(self):
	    super(QueueProcessResourceTest, self).setUp()

	    self.ts = TestSetupHelpers()
	    self.lt = self.ts.create_arbitrary_location_type()
	    self.o = self.ts.create_arbitrary_office()
	    self.top_lvl_location = self.ts.create_arbitrary_location(
	        self.lt.id,
	        self.o.id,
	        location_code ='Nigeria',
	        location_name='Nigeria')

	def test_get(self):
		# create a document, document_detail, source_submission
		doc = Document.objects.create(doc_title='new doc, bro!')
		doc_detail_type = DocDetailType.objects.create(name='some detail type')
		doc_detail = DocumentDetail.objects.create(document_id=doc.id,\
		 doc_detail_type_id = doc_detail_type.id,\
		 doc_detail_value ='something!' )

		data ={
			'document_id':doc.id
		}

		resp = self.ts.get(self, '/api/v1/queue_process/', data=data)

		response_data = self.deserialize(resp)
		self.assertHttpOK(resp)
		self.assertEqual(len(response_data['objects']), 1)
		self.assertEqual(response_data['objects'][0]['id'], doc_detail.id)

	def test_get_no_param(self):
		resp = self.ts.get(self, '/api/v1/queue_process/')
		self.assertHttpApplicationError(resp)
