from base_test_case import RhizomeApiTestCase
from rhizome.models import DocDetailType, LocationTree
from rhizome.tests.setup_helpers import TestSetupHelpers

class SyncODKResourceTest(RhizomeApiTestCase):

    def setUp(self):
        super(SyncODKResourceTest, self).setUp()
        self.ts = TestSetupHelpers()
        self.lt = self.ts.create_arbitrary_location_type()
        self.o = self.ts.create_arbitrary_office()

        self.top_lvl_location = self.ts.create_arbitrary_location(
            self.lt.id,
            self.o.id,
            location_code='Mars',
            location_name='Mars')

    def test_get(self):
        '''
        This test only covers exceptions as this needs a .jar file on the
        server to execute.

        The ODK process that this tests is based on an interface between
        our app and ODK aggregate on ODK app engine.  At the time we were
        writing this, the ODK backend that we had access to was run on
        google cloud, but there was no REST api to access that information
        like there is for other ODK providers like ONA.

        So, this api call is here as a skeleton for other ODK integration
        in which you would replace the jar file process n the `sync_odk`
        module, with a GET request for instance to the ONA server holding
        the ODK form data that you need.
        '''

        ## without a form_id, we can't do anything ##
        resp = self.ts.get(self, '/api/v1/sync_odk/')
        response_data = self.deserialize(resp)
        self.assertHttpApplicationError(resp)
        expected_error_message = 'Missing required parameter odk_form_id'
        self.assertEqual(expected_error_message, str(response_data['error']))

        ## without a document_id, we can still proceed, but we need to ensure
        ## that after we run this method, that we can find the document
        ## id for what we created

        filters = {'odk_form_id': 'an_odk_form_from_a_server'}
        resp = self.ts.get(self, '/api/v1/sync_odk/', data = filters)
        response_data = self.deserialize(resp)
        self.assertHttpOK(resp)
        # self.assertEqual(expected_error_message, str(response_data['error']))
