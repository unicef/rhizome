import json

from pandas import notnull, DataFrame, concat

from rhizome.models.indicator_models import Indicator, IndicatorToTag, \
    IndicatorBound
from rhizome.models.location_models import Location, LocationTree, \
    LocationType, LocationPolygon, MinGeo

class IndicatorCache(object):
    '''
    from rhizome.cache_meta import IndicatorCache as ic
    ic_obj = ic(indicator_id_list=[164])
    ic_obj.main()
    '''

    def __init__(self, indicator_id_list=None):

        if not indicator_id_list:
            self.indicator_id_list = Indicator.objects.all().values_list('id',
                                                                         flat=True)
        else:
            self.indicator_id_list = indicator_id_list

    def main(self):
        '''
        Find the office id for each indicator.

        Find the Tags for Each indicator

        Find the bounds for each indicator

        '''

        indicator_batch = []
        qs,  bound_df, tag_df = self.build_related_objects()

        for ind in qs:

            # look up the bounds / tags from the data two DFs created above
            filtered_tag_df = tag_df[tag_df['indicator_id'] == ind.id]
            filtered_bound_df = bound_df[bound_df['indicator_id'] == ind.id]

            ind.bound_json = [row.to_dict()
                              for ix, row in filtered_bound_df.iterrows()]
            ind.tag_json = list(filtered_tag_df['indicator_tag_id'].unique())

            ind.save()

    def build_related_objects(self):
        tag_cols = ['indicator_id', 'indicator_tag_id']
        bound_cols = ['indicator_id', 'bound_name', 'mn_val', 'mx_val']

        tag_df = DataFrame(list(IndicatorToTag.objects.filter(
            indicator_id__in=self.indicator_id_list).values_list(*tag_cols)), columns=tag_cols)

        bound_df = DataFrame(list(
            IndicatorBound.objects.filter(
                indicator_id__in=self.indicator_id_list).values_list(*bound_cols)
        ), columns=bound_cols)

        qs = Indicator.objects.filter(id__in=self.indicator_id_list)

        bound_df = bound_df.where((notnull(bound_df)), None)
        tag_df = tag_df.where((notnull(tag_df)), None)
        # office_df = office_df.where((notnull(office_df)), None)

        return qs, bound_df, tag_df


class LocationTreeCache(object):
    """
    """

    def __init__(self):

        self.location_tree_columns = ['location_id','parent_location_id','lvl']
        self.location_tree_df = DataFrame(columns=self.location_tree_columns)

    def main(self):
        '''
        The loop is initiated by taking the lowest level ( village for
        instance ) and moving up throughout the tree. district > province >
        region > country etc.

        The process creates a dataframe caled location_tree_df that we continue
        to append to finally bulk inserting that information into the db.
        '''

        ## iterate from bottom to bottom to top ##
        for lt_id, name, admin_level in LocationType.objects.all()\
            .values_list('id', 'name', 'admin_level')\
            .order_by('-admin_level'):

            self.process_location_tree_lvl(lt_id)

        self.add_lvl_zero_to_df()
        self.upsert_location_tree()

    def process_location_tree_lvl(self, location_type_id):
        '''
        Get and process data for a particular location type ( admin level ).
        '''

        lt_batch = []
        df_columns = ['location_id', 'parent_location_id']
        location_df = DataFrame(list(Location.objects
                             .filter(location_type_id=location_type_id)
                             .values_list('id', 'parent_location_id')),\
                              columns= df_columns)
        location_df['lvl'] = 1 # since this is a direct parent child relation

        merged_df = location_df.merge(self.location_tree_df\
                        ,left_on='location_id'\
                        ,right_on='parent_location_id')

        cleaned_merge_df = merged_df[['location_id_y', 'parent_location_id_x'\
            ,'lvl_y']]

        cleaned_merge_df['lvl_y'] = cleaned_merge_df['lvl_y'] + 1
        cleaned_merge_df.columns = self.location_tree_columns

        self.location_tree_df = concat([self.location_tree_df, location_df,
                                        cleaned_merge_df])
        self.location_tree_df.drop_duplicates()

    def add_lvl_zero_to_df(self):
        '''
        Every location should have a row for itself in this table such that
        my any location is equal to it's parent when lvl = 0.
        '''

        unique_location_id_list = \
            list(self.location_tree_df['location_id'].unique())

        zero_level_df = DataFrame([[l, l, 0] for l in unique_location_id_list],\
            columns = self.location_tree_columns)

        self.location_tree_df = self.location_tree_df.append(zero_level_df)


    def upsert_location_tree(self):
        """
        """

        lt_batch = []

        ## Drop Duplicates; NaN --> None
        self.location_tree_df.dropna(inplace=True)

        ## iterate through the location tree df created above ##
        for ix, loc in self.location_tree_df.iterrows():
            lt_batch.append(LocationTree(**{
                'location_id': loc.location_id,
                'parent_location_id': loc.parent_location_id,
                'lvl': loc.lvl,
            }))

        LocationTree.objects.all().delete()
        LocationTree.objects.bulk_create(lt_batch)

        ## add the ultimate parent as it will not have a record in the df yet
        ultimate_parent_id = Location.objects\
            .filter(parent_location_id__isnull = True)[0].id

        ult_parent, created = LocationTree.objects.get_or_create(
            location_id = ultimate_parent_id,
            parent_location_id = ultimate_parent_id,
            defaults = {'lvl': 0},
        )

def minify_geo_json():
    '''
    Make a square a triangle.. an octagon a hexagon.  Shrink the Number of
    vertices for each polygon.

    This is a kind of "dumb" algorithm because the adjacent shaps dont line up
    Like they do with the source, but the reduced size of the data returned
    to the API makes having the lower fidelity shapes worth the performance
    boost.

    This ensures that every shape in the system has no more than 100 vertices.
    If the original shape has 99, we do not shrink.  I do my best here not to
    blindly shrink the shape, but instead to remove points that are super close
    together.

    from rhizome.cache_meta import minify_geo_json as m
    m()
    '''

    min_geo_batch = []

    for shp in LocationPolygon.objects.all():

        new_polygon_list = []
        geo_json = json.loads(shp.geo_json)
        polygon = geo_json['geometry']['coordinates']

        if geo_json['geometry']['type'] == 'Polygon':  # MultiPolygons trip me up ##

            min_polygon = minify_polygon(polygon)
            new_polygon_list.append(min_polygon)

            geo_json['geometry']['coordinates'] = new_polygon_list

        shp_obj = \
            MinGeo(**{'location_id': shp.location_id, 'geo_json': geo_json})
        min_geo_batch.append(shp_obj)

    MinGeo.objects.all().delete()
    MinGeo.objects.bulk_create(min_geo_batch)


def minify_polygon(polygon):
    '''
    This should be a more sophisticated algorithm that ensures adjacent shapes
    line up.  However for now, we just take one out of ever 5 points... meaning
    That the geo_json we return to the browser ( while there may be a little
    overlap for adjacent shapes ) is theoretically 1/5th the size.
    '''

    shape_df = DataFrame(polygon[0], columns=['lat', 'lon'])

    shape_df['index_col'] = shape_df.index
    shape_df['to_take'] = 0  # shape_df['index_col'].map(lambda x: x % 5)
    filtered_df = shape_df[shape_df['to_take'] == 0][['lat', 'lon']]

    return filtered_df.values.tolist()


def cache_all_meta():

    location_tree_cache_data = LocationTreeCache()
    location_tree_cache_data.main()

    indicator_cache_data = IndicatorCache()
    indicator_cache_data.main()

    # minify_geo_json()
