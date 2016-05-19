from tastypie.test import ResourceTestCase
from rhizome.models import Document, DocumentDetail, SourceSubmission, DocDetailType
from setup_helpers import TestSetupHelpers


class UserGroupResourceTest(ResourceTestCase):
	'''
	this still needs to be implemented.
	TO DO: how to access User and Group tables through Django
	'''
	# def setUp(self):
	#     super(UserGroupResourceTest, self).setUp()

	#     self.ts = TestSetupHelpers()
	#     self.lt = self.ts.create_arbitrary_location_type()
	#     self.o = self.ts.create_arbitrary_office()
	#     self.top_lvl_location = self.ts.create_arbitrary_location(
	#         self.lt.id,
	#         self.o.id,
	#         location_code ='Nigeria',
	#         location_name='Nigeria')

	# def test_get(self):
	# 	data ={
	# 		'user_id':self.ts.user.id
	# 	}
	# 	resp = self.ts.get(self, '/api/v1/user_group/', data)
	# 	response_data = self.deserialize(resp)
	# 	print response_data
