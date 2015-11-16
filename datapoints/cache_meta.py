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

def cache_location_tree():

    location_tree_batch,location_df_list = [],[]

    ## process locations from the lowest admin level and work up to country ##
    location_type_loop_order = LocationType.objects.all()\
        .values_list('id',flat=True).order_by('-admin_level')

    for i,(lt_id) in enumerate(location_type_loop_order):

        lt_df = process_location_tree_lvl(lt_id)
        lt_df['lvl'] = i
        location_df_list.append(lt_df)

    all_lvl_location_tree_df =  concat(location_df_list)

    location_df_unique = DataFrame(all_lvl_location_tree_df\
        .groupby(['location_id','parent_location_id'])['lvl'].min())

    location_df_unique.reset_index(level=[0,1], inplace=True)

    for ix, location_tree in location_df_unique.iterrows():

        lt_dict = {
            'location_id':location_tree.location_id,
            'immediate_parent_id':location_tree.parent_location_id,
            'parent_location_id':location_tree.parent_location_id,
            'lvl':location_tree.lvl
        }

        location_tree_batch.append(LocationTree(**lt_dict))

    LocationTree.objects.all().delete()
    LocationTree.objects.bulk_create(location_tree_batch)

def process_location_tree_lvl(location_type_id):

    location_tree_columns = ['location_id','parent_location_id']

    ## get the locations to process ##
    location_id_list = Location.objects\
        .filter(location_type_id = location_type_id)\
        .values_list('id',flat=True)

    ## build the direct parent location heirarchy ##
    this_lvl_df = DataFrame(list(Location.objects\
        .filter(id__in=location_id_list)\
        .values_list('id','parent_location_id')),columns=location_tree_columns)

    ## build the level up location heirarchy ##
    next_lvl_df = DataFrame(list(Location.objects\
        .filter(id__in=this_lvl_df['parent_location_id'].unique())\
        .values_list('id','parent_location_id')),\
            columns=location_tree_columns)

    ## ultimate parent has parent_location_id = location_id ##
    this_lvl_df.parent_location_id.fillna(this_lvl_df\
        .location_id, inplace=True)
    next_lvl_df.parent_location_id.fillna(next_lvl_df\
        .location_id, inplace=True)

    ## merge this level, and next level
    merged_df = this_lvl_df.merge(next_lvl_df,left_on='parent_location_id',\
        right_on='location_id')

    ## clean up the merged df and return the concatenation of all 3 ##
    cleaned_merge_df = merged_df[['location_id_x','parent_location_id_y']]
    cleaned_merge_df.columns = location_tree_columns

    final_df = concat([next_lvl_df,this_lvl_df,cleaned_merge_df])

    return final_df


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
