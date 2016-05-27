from tastypie.test import ResourceTestCase

class RhizomeAPITestCase(ResourceTestCase):

	def assertHttpOK(self, resp):
		self.assertHttp(resp, 200)
	
	def assertHttpCreated(self, resp):
		self.assertHttp(resp, 201)

	def assertHttpApplicationError(self, resp):
		self.assertHttp(resp, 500)


	def assertHttp(self, resp, status_code):
		if resp.status_code != status_code:
			print self.deserialize(resp)
		self.assertEqual(resp.status_code, status_code)
