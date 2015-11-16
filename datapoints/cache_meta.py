from datapoints.models import *
from source_data.models import SourceObjectMap
from pandas import read_csv, notnull, DataFrame, concat

def cache_indicator_abstracted():
    '''
    Delete indicator abstracted, then re-insert by joiniding indicator boudns
    and creatign json for the indicator_bound field.  Also create the
    necessary JSON for the indicator_tag_json.

    This is the transformation that enables the API to return all indicator
    data without any transformation on request.
    '''

    i_raw = Indicator.objects.raw("""


        SELECT
             i.id
            ,i.short_name
            ,i.name
            ,i.slug
            ,i.description
            ,CASE WHEN CAST(x.bound_json as varchar) = '[null]' then '[]' ELSE x.bound_json END AS bound_json
            ,CASE WHEN CAST(y.tag_json as varchar) = '[null]' then '[]' ELSE y.tag_json END AS tag_json
        FROM (
            SELECT
            	i.id
            	,json_agg(row_to_json(ib.*)) as bound_json
            FROM indicator i
            LEFT JOIN indicator_bound ib
            ON i.id = ib.indicator_id
            GROUP BY i.id
        )x
		INNER JOIN (
            SELECT
            	i.id
            	,json_agg(itt.indicator_tag_id) as tag_json
            FROM indicator i
            LEFT JOIN indicator_to_tag itt
            ON i.id = itt.indicator_id

            GROUP BY i.id
		) y
		ON y.id = x.id
        INNER JOIN indicator i
        ON x.id = i.id

    """)

    upsert_meta_data(i_raw, IndicatorAbstracted)


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

def upsert_meta_data(qset, abstract_model):
    '''
    Given a raw queryset, and the model of the table to be upserted into,
    iterate through each resutl, clean the dictionary and batch delete and
    insert the data.
    '''

    batch = []

    for row in qset:

        row_data = dict(row.__dict__)
        del row_data['_state']

        object_instance = abstract_model(**row_data)
        batch.append(object_instance)

    abstract_model.objects.all().delete()
    abstract_model.objects.bulk_create(batch)
