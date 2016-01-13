from pandas import read_csv, notnull, DataFrame, concat
from numpy import sqrt, log

from datapoints.models import *
from source_data.models import SourceObjectMap



class IndicatorCache(object):
    '''
    from datapoints.cache_meta import IndicatorCache as ic
    ic_obj = ic(indicator_id_list=[164])
    ic_obj.main()
    '''
    def __init__(self, indicator_id_list = None):

        if not indicator_id_list:
            self.indicator_id_list = Indicator.objects.all().values_list('id',\
                flat =True)
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

            ind.bound_json = [row.to_dict() for ix, row in filtered_bound_df.iterrows()]
            ind.tag_json = list(filtered_tag_df['indicator_tag_id'].unique())

            ind.save()

    def build_related_objects(self):
        tag_cols = ['indicator_id', 'indicator_tag_id']
        bound_cols = ['indicator_id', 'bound_name', 'mn_val', 'mx_val']
        ind_to_office_cols = ['indicator_id', 'office_id']

        tag_df = DataFrame(list(IndicatorToTag.objects.filter(
            indicator_id__in=self.indicator_id_list).values_list(*tag_cols)), columns=tag_cols)

        bound_df = DataFrame(list(
            IndicatorBound.objects.filter(indicator_id__in=self.indicator_id_list).values_list(*bound_cols)
        ), columns=bound_cols)

        qs = Indicator.objects.filter(id__in=self.indicator_id_list)

        bound_df = bound_df.where((notnull(bound_df)), None)
        tag_df = tag_df.where((notnull(tag_df)), None)
        # office_df = office_df.where((notnull(office_df)), None)

        return qs, bound_df, tag_df


class LocationTreeCache(object):

    def __init__(self):

        self.location_tree_columns = ['location_id','parent_location_id']
        self.location_tree_df = DataFrame(columns=self.location_tree_columns)

    def main(self):
        '''
        Any and all parents attributed any and all children.  See the test
        case for an abstracted example.
        '''

        ## now iterate from bottom to bottom to top ##
        location_type_loop_order = LocationType.objects.all()\
            .values_list('id',flat=True).order_by('-admin_level')

        for lt_id in location_type_loop_order:
            self.process_location_tree_lvl(lt_id)

        self.upsert_location_tree()

    def process_location_tree_lvl(self, location_type_id):

        lt_batch = []

        location_df = DataFrame(list(Location.objects\
            .filter(location_type_id = location_type_id)\
            .values_list('id','parent_location_id')),columns=self.location_tree_columns)

        merged_df = location_df.merge(self.location_tree_df
            ,left_on='location_id',right_on='parent_location_id')

        cleaned_merge_df = merged_df[['location_id_y','parent_location_id_x']]
        cleaned_merge_df.columns = self.location_tree_columns

        self.location_tree_df = concat([self.location_tree_df,location_df,\
            cleaned_merge_df])

        self.location_tree_df.drop_duplicates()

    def upsert_location_tree(self):

        lt_batch = []

        ## only the ultimate parent should have itself as a parent ##
        ## drop all NA values, then create the ultimate parents ##
        self.location_tree_df.dropna(inplace=True)
        for loc in Location.objects.filter(parent_location_id__isnull=True):
            lt_batch.append(LocationTree(**{
                'location_id':loc.id,
                'parent_location_id':loc.id,
                'lvl':0,
            }))

        ## iterate through the location tree df created above ##
        for ix,loc in self.location_tree_df.iterrows():
            lt_batch.append(LocationTree(**{
                'location_id':loc.location_id,
                'parent_location_id':loc.parent_location_id,
                'lvl':0,
            }))

        LocationTree.objects.all().delete()
        LocationTree.objects.bulk_create(lt_batch)


def update_source_object_names():

    som_raw = SourceObjectMap.objects.raw(
    '''
        DROP TABLE IF EXISTS _tmp_object_names;
        CREATE TEMP TABLE _tmp_object_names
        AS

        SELECT som.master_object_id, i.short_name as master_object_name, som.content_type
        FROM source_object_map som
        INNER JOIN indicator i
            ON som.master_object_id = i.id
            AND som.content_type = 'indicator'

        UNION ALL

        SELECT som.master_object_id, r.name, som.content_type
        FROM source_object_map som
        INNER JOIN location r
            ON som.master_object_id = r.id
            AND som.content_type = 'location';

        UPDATE source_object_map som
        set master_object_name = t.master_object_name
        FROM _tmp_object_names t
        WHERE t.master_object_id = som.master_object_id
        AND t.content_type = som.content_type;

        SELECT * FROM source_object_map limit 1;

    ''')

    for row in som_raw:
        print row.id

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

    from datapoints.cache_meta import minify_geo_json as m
    m()
    '''

    min_geo_batch = []

    for shp in LocationPolygon.objects.all():

        new_polygon_list = []
        polygon = shp.geo_json['geometry']['coordinates']

        if shp.geo_json['geometry']['type'] == 'Polygon': # MultiPolygons trip me up ##

            min_polygon = minify_polygon(polygon)
            new_polygon_list.append(min_polygon)

            shp.geo_json['geometry']['coordinates'] = new_polygon_list

        shp_obj = \
            MinGeo(**{'location_id':shp.location_id,'geo_json':shp.geo_json})
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

    shape_df = DataFrame(polygon[0], columns=['lat','lon'])

    shape_df['index_col'] = shape_df.index
    shape_df['to_take'] = shape_df['index_col'].map(lambda x: x % 5)
    filtered_df = shape_df[shape_df['to_take'] == 0][['lat','lon']]

    return filtered_df.values.tolist()


def cache_all_meta():

    location_tree_cache_data = LocationTreeCache()
    location_tree_cache_data.main()

    indicator_cache_data = IndicatorCache()
    indicator_cache_data.main()

    source_object_cache = update_source_object_names()

    # minify_geo_json()

