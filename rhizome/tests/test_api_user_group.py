from base_test_case import RhizomeAPITestCase
from rhizome.models import UserGroup
from setup_helpers import TestSetupHelpers
from django.contrib.auth.models import User, Group

class UserGroupResourceTest(RhizomeAPITestCase):
	
	def setUp(self):
	    super(UserGroupResourceTest, self).setUp()

	    self.ts = TestSetupHelpers()
	    self.lt = self.ts.create_arbitrary_location_type()
	    self.o = self.ts.create_arbitrary_office()
	    self.top_lvl_location = self.ts.create_arbitrary_location(
	        self.lt.id,
	        self.o.id,
	        location_code ='Nigeria',
	        location_name='Nigeria')

	def test_get(self):
		user = User.objects.create(username='Sam')
		group = Group.objects.create(name="Sam's Group")
		user_group = UserGroup.objects.create(user=user, group=group)
		data ={
			'user_id':user.id
		}
		resp = self.ts.get(self, '/api/v1/user_group/', data)
		response_data = self.deserialize(resp)
		self.assertHttpOK(resp)
		self.assertEqual(len(response_data['objects']), 1)
		resp_obj = response_data['objects'][0]
		self.assertEqual(resp_obj['group_id'], group.id)
		self.assertEqual(resp_obj['user_id'], user.id)
		self.assertEqual(resp_obj['id'], user_group.id)

	def test_get_all(self):
		user = User.objects.create(username='Sam')
		group = Group.objects.create(name="Sam's Group")
		user_group_1 = UserGroup.objects.create(user=user, group=group)
		user_group_2 = UserGroup.objects.create(user=self.ts.user, group=group)
		resp = self.ts.get(self, '/api/v1/user_group/')
		response_data = self.deserialize(resp)
		self.assertHttpOK(resp)
		self.assertEqual(len(response_data['objects']), UserGroup.objects.count())


	def test_create(self):
		user = User.objects.create(username='Sam')
		group = Group.objects.create(name="Sam's Group")
		self.assertEqual(UserGroup.objects.count(), 0)
		data ={
			'user_id':user.id,
			'group_id':group.id
		}
		resp = self.ts.post(self, '/api/v1/user_group/', data)
		self.assertHttpCreated(resp)
		self.assertEqual(UserGroup.objects.count(), 1)
		response_data = self.deserialize(resp)
		self.assertEqual(response_data['user_id'], user.id)
		self.assertEqual(response_data['group_id'], group.id)

	def test_obj_delete(self):
		user = User.objects.create(username='Sam')
		group = Group.objects.create(name="Sam's Group")
		user_group = UserGroup.objects.create(user=user, group=group)
		self.assertEqual(UserGroup.objects.count(), 1)
		delete_url = '/api/v1/user_group/?user_id='+ str(user.id) + '&group_id=' + str(group.id)
		self.ts.delete(self, delete_url)
		self.assertEqual(UserGroup.objects.count(), 0)




