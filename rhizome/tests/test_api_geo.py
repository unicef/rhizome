import json

from tastypie.test import ResourceTestCase
from django.contrib.auth.models import User
from setup_helpers import TestSetupHelpers
from pandas import read_csv, notnull, to_datetime
from rhizome.models import *
from pandas import read_csv, notnull, to_datetime, DataFrame, Series
from rhizome.cache_meta import minify_geo_json, LocationTreeCache


class GeoResourceTest(ResourceTestCase):
    def setUp(self):
      #   super(GeoResourceTest, self).setUp()


        self.ts = TestSetupHelpers()
        self.lt = LocationType.objects.create(name='Province',admin_level=2)
        self.o = self.ts.create_arbitrary_office()
        location_df_from_csv= read_csv('rhizome/tests/_data/locations_nimroz.csv')
        locations = self.ts.model_df_to_data(location_df_from_csv,Location)

        ## override location type attribute from file so that these locations ##
        ## are provinces ##
        for loc in locations:
            loc.location_type_id = self.lt.id
            loc.save()

        geo_json_df = read_csv('rhizome/tests/_data/geo_json.txt',delimiter = "|")
        location_df = DataFrame(list(Location.objects.all()\
		    .values_list('id','location_code')),columns=['location_id','location_code'])
        location_tree_df = DataFrame(list(Location.objects.all()\
		    .values_list('id','parent_location_id')),columns=['location_id','parent_location_id'])
        location_tree_df['lvl'] = Series(1, index=location_tree_df.index)
        location_tree = self.ts.model_df_to_data(location_tree_df, LocationTree)
        merged_df = location_df.merge(geo_json_df)[['location_id','geo_json']]
        self.ts.model_df_to_data(merged_df, LocationPolygon)
        minify_geo_json()
        LocationPermission.objects.create(user_id = self.ts.user.id,\
            top_lvl_location_id = 1)


    def test_get_geo_tree_lvl(self):
        get_data ={'parent_location_id__in':6, 'tree_lvl':1}
        resp = self.ts.get(self, '/api/v1/geo/', get_data)
        self.assertHttpOK(resp)
        self.assertEqual(len(self.deserialize(resp)['features']), 5)

    # make sure that the api returns the parent location

    def test_check_parent_location(self):
        get_data ={'parent_location_id__in':6, 'tree_lvl':1}
        resp = self.ts.get(self, '/api/v1/geo/', get_data)
        self.assertHttpOK(resp)
        resp_data = self.deserialize(resp)
        self.assertEqual(int(resp_data['parent_location_id__in']), 6)
