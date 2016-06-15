from pandas import DataFrame, notnull
from django.test import TestCase

from rhizome.models import LocationTree, Office, LocationType, Location

from rhizome.cache_meta import LocationTreeCache

class LocationTreeCacheTest(TestCase):
    '''
    The point of this test is to ensure that the

    `LocationTreeCache`

    Takes input from the location table and transforms the location tree
    appropriately.

    The idea with this cache is that we have three columns, location_id,
    parent_location_id and lvl.  Lvl cooresponds to what level of depth that
    child is of it's parent.

    Conside the following input ( `location` table )

    |      location      |     parent_location   |
    ----------------------------------------------
    | USA               | NULL                  |
    | New York State    | USA                   |
    | New York City     | New York State        |
    | The Bronx         | New York City         |
    | California        | USA                   |

    We want the output ( `location_tree` table )

    |   location    |   parent_location  | lvl |
    ----------------------------------------------
    | USA            |   USA             | 0 |
    | New York State |   USA             | 1 |
    | California     |   USA             | 1 |
    | New York City  |   USA             | 2 |
    | The Bronx      |   USA             | 3 |
    | New York State |   New York State  | 0 |
    | New York City  |   New York State  | 1 |
    | Brooklyn       |   New York State  | 1 |

    ... and so on.
    '''

    def __init__(self, *args, **kwargs):

        super(LocationTreeCacheTest, self).__init__(*args, **kwargs)

    def setUp(self):

        pass

    def test_cache_location_tree(self):
        '''
        The point of this test is that it the cache_location_tree function
        creates database rows that represents each parent / child relationship
        between all locations, from the stored information.

        That is, if we say that NYC is a sub-location of NYState, and NYState
        is a sub-location of U.S.A. , then that means that we should have a row
        in the LocationTree table rebresenting the fact that both Nystate AND
        U.S.A. are parent_location's on New York City.
        '''

        location_batch = []

        office = Office.objects.create(name='not important')
        location_type_country = LocationType.objects\
            .create(name='Country', admin_level=0, id=1)
        location_type_state = LocationType.objects\
            .create(name='State', admin_level=1, id=2)
        location_type_city = LocationType.objects\
            .create(name='City', admin_level=2, id=3)
        location_type_city = LocationType.objects\
            .create(name='Neighborhood', admin_level=3, id=4)

        location_data = {
            'id': [1, 2, 3, 4, 5, 6, 7, 8],
            'location_type_id': [1, 2, 3, 2, 2, 2, 3, 4],
            'name': ['U.S.A.', 'New York State', 'New York City', 'Texas',
                     'California', 'Maine', 'Portland, ME', 'Brooklyn'],
            'parent_location_id': [None, 1, 2, 1, 1, 1, 6, 3]
        }

        df = DataFrame.from_dict(location_data)
        df.set_index('id', inplace=True, drop=False, append=False)
        no_nan_df = df.where((notnull(df)), None)

        for ix, loc in no_nan_df.iterrows():
            location_batch.append(Location(**{
                'id': loc.id,
                'name': loc.name,
                'location_code': unicode(loc.name).replace(' ', ''),
                'office_id': office.id,
                'location_type_id': loc.location_type_id,
                'parent_location_id': loc.parent_location_id
            }))

        Location.objects.bulk_create(location_batch)

        ## now use the following function to transform the location_tree ##
        ltc = LocationTreeCache()
        ltc.main()

        location_tree_in_db = LocationTree.objects.all()\
            .values_list('location_id', 'parent_location_id','lvl')

        ## every location should have a row in this table with
        ## lvl = 0 and itself as the parent_location_id
        for loc in location_data['id']:
            self.assertTrue((loc, loc, 0) in location_tree_in_db)

        ## new york city (3) has a parent of NY State (2) AND U.S.A (1)##
        self.assertTrue((3, 1, 2) in location_tree_in_db)
        self.assertTrue((3, 2, 1) in location_tree_in_db)

        ## Portland ME (7) has a parent of Maine (6) AND U.S.A (1) ##
        self.assertTrue((7, 1, 2) in location_tree_in_db)
        self.assertTrue((7, 6, 1) in location_tree_in_db)

        ## new york state and maine are direct children of USA ##
        self.assertTrue((2, 1, 1) in location_tree_in_db)
        self.assertTrue((6, 1, 1) in location_tree_in_db)

        ## Brooklkyn has, NYC, NYState and USA as parents ##
        self.assertTrue((8, 3, 1) in location_tree_in_db)
        self.assertTrue((8, 2, 2) in location_tree_in_db)
        self.assertTrue((8, 1, 3) in location_tree_in_db)
