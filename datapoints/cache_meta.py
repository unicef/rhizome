from pandas import read_csv, notnull, DataFrame, concat
from numpy import sqrt, log

from datapoints.models import *
from source_data.models import SourceObjectMap

from pprint import pprint

def calculate_campaign_percentage_complete():
    '''
    Add the pct-complete to the campaign based ont he pct of management
    indiators present for that campaign for the top level locations.
    '''

    ## temporarily harcoding indicators until we get management dashboard
    ## definition loading from the api... see trello #226:
    all_indicators = [168, 431, 432, 433, 166, 164, 167, 165, 475, 187, 189, \
    27, 28, 175, 176, 177, 204, 178, 228, 179, 184, 180, 185, 230, 226, 239, \
    245, 236, 192, 193, 191, 194, 219, 173, 172, 169, 233, 158, 174, 442, 443, \
    444, 445, 446, 447, 448, 449, 450]

    for c in Campaign.objects.all():

        top_level_location_id =  Location.objects\
            .get(parent_location_id__isnull=True,office_id = c.office_id).id

        ind_count = DataPointComputed.objects.filter(
            campaign_id = c.id,
            location_id = top_level_location_id,
            indicator_id__in = all_indicators
        ).count()

        c.management_dash_pct_complete = ind_count / float(len(all_indicators))
        c.save()

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

        SELECT som.master_object_id, c.slug, som.content_type
        FROM source_object_map som
        INNER JOIN campaign c
            ON som.master_object_id = c.id
            AND som.content_type = 'campaign'

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

    # for shp in LocationPolygon.objects.filter(location_id__in=[3108,3109]):
    for shp in LocationPolygon.objects.all():

        new_polygon_list = []
        raw_polygon_list = shp.geo_json['geometry']['coordinates']

        if shp.geo_json['geometry']['type'] == 'Polygon': # MultiPolygons trip me up ##

            for polygon in raw_polygon_list:

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
    Determine based on the number of coordinates, how many vertices we want to
    take, then remove points that are closest to one another, and return a list
    of lists in coorespondance to the optimal vertex count

    a--b-------------------c-d-------e---------------------f-g-h-i-------j

    becomes

    a----------------------c---------e---------------------f-----i-------j

    first we find, based on the size of the dataframe how many rows we want to
    keep.  This is a logarithmic function so that for instance if there are 1000
    rows we take 300, but if there are 500 we take 180.
    '''

    try:
        shape_df = DataFrame(polygon, columns=['lat','lon'])
    except AssertionError:
        ## see Sindj and Punjab in pakistan.. these are MultiPolygons ##
        shape_df = DataFrame(polygon[0], columns=['lat','lon'])

    ## determine how many vertices the new shape will be ( needs better fn! ) ##
    # rows_to_take = round(len(shape_df)/log(len(shape_df)))
    rows_to_take = len(shape_df) / 2 if len(shape_df) > 100 else len(shape_df)

    ## Find the adjacent vertex, and the distance between the two points ##
    ## use pythagorean, not haverstime theroem because our map is 2d ( unlike
    ## planet earth with is 3D! )
    shape_df['ix_plus_one'] = shape_df.index + 1
    merged_df = shape_df.merge(shape_df,left_index=True, right_on = 'ix_plus_one')
    merged_df['lat_lon_dist'] = ((merged_df['lat_x'] - merged_df['lat_y']) + \
        (merged_df['lon_x'] - merged_df['lon_y']))
    merged_df['dist'] = merged_df['lat_lon_dist'].apply(lambda x: sqrt(abs(x)))

    ## remove the rows that are closest to one another  ##
    merged_df['distance_rank'] = merged_df['dist'].rank(ascending=False)
    merged_df.sort('distance_rank')
    filtered_df = merged_df[merged_df['distance_rank'] <= rows_to_take]

    return filtered_df[['lat_x','lon_x']].values.tolist()
