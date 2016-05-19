# from tastypie.test import ResourceTestCase
# from setup_helpers import TestSetupHelpers

# class RefreshMasterAPIResourceTest(ResourceTestCase):
# 	def setUp(self):
# 	    super(RefreshMasterAPIResourceTest, self).setUp()

# 	    self.ts = TestSetupHelpers()
# 	    self.lt = self.ts.create_arbitrary_location_type()
# 	    self.o = self.ts.create_arbitrary_office()
# 	    self.top_lvl_location = self.ts.create_arbitrary_location(
# 	        self.lt.id,
# 	        self.o.id,
# 	        location_code ='Nigeria',
# 	        location_name='Nigeria')

#     def test_refresh(self):