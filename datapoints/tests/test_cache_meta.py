import json

from pandas import read_csv, notnull, DataFrame
from numpy import nan,isnan
from django.test import TestCase

from datapoints.models import LocationType, Location, LocationTree, Office,\
    Indicator, IndicatorBound, IndicatorToTag, IndicatorAbstracted, IndicatorTag
from datapoints.cache_meta import LocationTreeCache
from datapoints.cache_meta import cache_indicator_abstracted

class CacheMetaTestCase(TestCase):
    '''
    '''

    def __init__(self, *args, **kwargs):

        self.set_up()
        super(CacheMetaTestCase, self).__init__(*args, **kwargs)

    def set_up(self):
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
        location_type_country = LocationType.objects.create(name='Country',\
            admin_level=0,id=1)
        location_type_state = LocationType.objects.create(name='State',\
            admin_level=1,id=2)
        location_type_city = LocationType.objects.create(name='City',\
            admin_level=2,id=3)
        location_type_city = LocationType.objects.create(name='Neighborhood',\
            admin_level=3,id=4)

        location_data = {
                'id':[1,2,3,4,5,6,7,8],
                'location_type_id':[1,2,3,2,2,2,3,4],
                'name': ['U.S.A.','New York State','New York City','Texas',\
                    'California','Maine','Portland, ME','Brooklyn'],
                'parent_location_id': [None,1,2,1,1,1,6,3]
            }

        df = DataFrame.from_dict(location_data)
        df.set_index('id', inplace=True, drop=False, append=False)
        no_nan_df = df.where((notnull(df)), None)

        for ix, loc in no_nan_df.iterrows():
            location_batch.append(Location(**{
                'id':loc.id,
                'name':loc.name,
                'location_code': unicode(loc.name).replace(' ',''),
                'office_id':office.id,
                'location_type_id':loc.location_type_id,
                'parent_location_id':loc.parent_location_id
            }))

        Location.objects.bulk_create(location_batch)

        ## now use the following function to transform the location_tree ##
        ltc = LocationTreeCache()
        ltc.main()

        location_tree_in_db = LocationTree.objects.all()\
            .values_list('location_id','parent_location_id')

        ## the ultimate parent, should have a with itself is parent ##
        self.assertTrue((1,1) in location_tree_in_db)

        ## Brooklyn However should not be the parent of itself ##
        self.assertFalse((8,8) in location_tree_in_db)

        ## new york city has a parent of NY State AND U.S.A ##
        self.assertTrue((3,1) in location_tree_in_db)
        self.assertTrue((3,2) in location_tree_in_db)

        ## Portland ME has a parent of Maine AND U.S.A ##
        self.assertTrue((7,1) in location_tree_in_db)
        self.assertTrue((7,6) in location_tree_in_db)

        # ## new york state and maine are children of USA #
        self.assertTrue((2,1) in location_tree_in_db)
        self.assertTrue((6,1) in location_tree_in_db)

        ## Brooklkyn has, NYC, NYState and USA as parents ##
        self.assertTrue((8,3) in location_tree_in_db)
        self.assertTrue((8,2) in location_tree_in_db)
        self.assertTrue((8,1) in location_tree_in_db)

    def test_cache_indicator_abstracted(self):
        '''
        '''
        ind = Indicator.objects.create(**{
            'name':'test name',
            'short_name':'test short name',
            'description':'test description',
        })

        ## tags ##
        ind_tag_1 = IndicatorTag.objects.create(tag_name='tag1')
        ind_tag_2 = IndicatorTag.objects.create(tag_name='tag2')

        indicator_to_tag_1 = IndicatorToTag.objects.create(
            indicator = ind,indicator_tag = ind_tag_1
        )
        indicator_to_tag_2 = IndicatorToTag.objects.create(
            indicator = ind,indicator_tag = ind_tag_2
        )

        ## bounds ##
        bound_dict_1 = {u'indicator_id': ind.id, u'mn_val':10, u'mx_val':20,\
            u'bound_name':u'Good'}
        bound_dict_2 = {'indicator_id': ind.id, u'mn_val':20, u'mx_val':30,\
            u'bound_name':u'Bad'}

        ind_bound_1 = IndicatorBound.objects.create(**bound_dict_1)
        ind_bound_2 = IndicatorBound.objects.create(**bound_dict_2)

        cache_indicator_abstracted()

        ind_abstract = IndicatorAbstracted.objects.get(id=ind.id)
        target_tag_json = [ind_tag_1.id, ind_tag_2.id]
        target_bound_json = [bound_dict_1, bound_dict_2]

        ## is the short_name the same ? ##
        self.assertEqual(ind.short_name, ind_abstract.short_name)

        # ## are the tags properly pivoted into json ? ##
        self.assertEqual(target_tag_json.sort(), ind_abstract.tag_json.sort())

        # ## do indicator bounds get properly transformed into json ? ##
        # self.assertEqual(bound_dict_1['bound_name'],\
        #     ind_abstract.bound_json[0]['bound_name'])
        # self.assertEqual(bound_dict_1['mn_val'],\
        #     ind_abstract.bound_json[0]['mn_val'])
        # self.assertEqual(bound_dict_1['mx_val'],\
        #     ind_abstract.bound_json[0]['mx_val'])
        #
        # self.assertEqual(bound_dict_2['bound_name'],\
        #     ind_abstract.bound_json[1]['bound_name'])
        # self.assertEqual(bound_dict_2['mn_val'],\
        #     ind_abstract.bound_json[1]['mn_val'])
        # self.assertEqual(bound_dict_2['mx_val'],\
        #     ind_abstract.bound_json[1]['mx_val'])
