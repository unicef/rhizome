
from tastypie.test import ResourceTestCase
from setup_helpers import TestSetupHelpers
from pandas import read_csv
from rhizome.models import *
from pandas import DataFrame
from pandas import Series
from pandas import read_csv
from rhizome.cache_meta import minify_geo_json


class GeoResourceTest(ResourceTestCase):
    def setUp(self):
        super(GeoResourceTest, self).setUp()

        self.ts = TestSetupHelpers()
        self.lt = LocationType.objects.create(name='Region',admin_level=1)

        self.distr, created = \
            LocationType.objects.get_or_create(name='District',admin_level = 2)

        self.o = self.ts.create_arbitrary_office()
        location_df_from_csv= read_csv('rhizome/tests/_data/locations_nimroz.csv')
        self.ts.model_df_to_data(location_df_from_csv,Location)

        # make sure that the proper level is set for the 
        locs = Location.objects.filter(parent_location_id=6)
        for loc in locs:
            loc.location_type_id = self.distr.id
            loc.save()

        parent = Location.objects.get(id=6)
        parent.location_type_id = self.lt.id
        parent.save()

        geo_json_df = read_csv('rhizome/tests/_data/geo_json_small.txt',delimiter = "|")
        location_df = DataFrame(list(Location.objects.all()\
		    .values_list('id','location_code')),columns=['location_id','location_code'])
        location_tree_df = DataFrame(list(Location.objects.all()\
		    .values_list('id','parent_location_id')),columns=['location_id','parent_location_id'])
        location_tree_df['lvl'] = Series(1, index=location_tree_df.index)
        self.ts.model_df_to_data(location_tree_df, LocationTree)
        merged_df = location_df.merge(geo_json_df)[['location_id','geo_json']]
        self.ts.model_df_to_data(merged_df, LocationPolygon)
        minify_geo_json()
        LocationPermission.objects.create(user_id = self.ts.user.id,
            top_lvl_location_id = 1)


    def test_get_geo(self):
        get_data ={'location_id__in':6, 'location_depth':1}
        resp = self.ts.get(self, '/api/v1/geo/', get_data)
        self.assertHttpOK(resp)
        self.deserialize(resp)
        self.assertEqual(len(self.deserialize(resp)['features']), 5)

   