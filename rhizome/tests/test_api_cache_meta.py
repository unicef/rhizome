from base_test_case import RhizomeApiTestCase
from rhizome.models import DocDetailType, LocationTree
from rhizome.tests.setup_helpers import TestSetupHelpers

class CacheMetaResourceTest(RhizomeApiTestCase):

    def setUp(self):
        super(CacheMetaResourceTest, self).setUp()

        self.ts = TestSetupHelpers()
        self.lt = self.ts.create_arbitrary_location_type()
        self.o = self.ts.create_arbitrary_office()
        self.top_lvl_location = self.ts.create_arbitrary_location(
            self.lt.id,
            self.o.id,
            location_code='The Solar System',
            location_name='The Solar System'
        )
        self.leaf_location = self.ts.create_arbitrary_location(
            self.lt.id,
            self.o.id,
            location_code='Mars',
            location_name='Mars',
            parent_location_id = self.top_lvl_location.id
        )


    def test_get(self):
        '''
        This url should re-build the location_tree, so if i truncate that
        table, truncate the location table, and add two locations, they
        should show up in the locatin tree table after the url is hit.
        '''

        LocationTree.objects.all().delete()

        resp = self.ts.get(self, '/api/v1/cache_meta/')
        response_data = self.deserialize(resp)
        self.assertHttpOK(resp)

        leaf_location_tree_data = LocationTree.objects\
            .filter(location_id = self.leaf_location).values()

        ## there shoul be one record where the leaf has a parent of itself
        ## with lvl = 0, and one where the parent is the top_lvl_location
        ## and the lvl = 1
        self.assertEqual(len(leaf_location_tree_data), 2)
