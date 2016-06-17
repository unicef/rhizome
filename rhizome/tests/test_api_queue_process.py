from base_test_case import RhizomeApiTestCase
from rhizome.models import Document, SourceSubmission
from rhizome.tests.setup_helpers import TestSetupHelpers


class QueueProcessResourceTest(RhizomeApiTestCase):

    def setUp(self):
        super(QueueProcessResourceTest, self).setUp()

        self.ts = TestSetupHelpers()
        self.lt = self.ts.create_arbitrary_location_type()
        self.o = self.ts.create_arbitrary_office()
        self.top_lvl_location = self.ts.create_arbitrary_location(
            self.lt.id,
            self.o.id,
            location_code='Nigeria',
            location_name='Nigeria')

        # create a document, and one record for the soruce_submission #
        self.doc = Document.objects.create(doc_title='new doc')
        self.ss_obj = SourceSubmission.objects.create(
            document_id = self.doc.id,
            process_status = 'PROCESSED',
            row_number = 0
        )

    def test_get(self):
        '''
        This method is meant to update the soruce_submission table so that
        it is queued up for re-processing.

        So to test that.. we create one source_submission, that says it is
        processed, then we hit the api, and query again ensuring that the
        processed_status = 'TO_PROCESS', that is.. that the API call did what
        it was supposed to.
        '''

        data = { 'document_id': self.doc.id }

        resp = self.ts.get(self, '/api/v1/queue_process/', data=data)
        response_data = self.deserialize(resp)
        self.assertHttpOK(resp)

        new_ss_obj = SourceSubmission.objects.get(id = self.ss_obj.id)
        self.assertEqual(new_ss_obj.process_status, 'TO_PROCESS')


    def test_get_no_param(self):
        '''
        We should get an error if we do not pass a document_id
        '''
        resp = self.ts.get(self, '/api/v1/queue_process/')
        response_data = self.deserialize(resp)
        self.assertHttpApplicationError(resp)
        self.assertEqual(str(response_data['error'])\
            ,'Missing required parameter document_id')
