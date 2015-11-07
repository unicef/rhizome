import traceback
import json
from django.conf import settings

import pandas as pd
from pandas import DataFrame, read_sql
from pandas.tools.pivot import pivot_table

from django.contrib.auth.models import User
from datapoints.models import *
from source_data.models import SourceObjectMap

class AggRefresh(object):
    '''
    Any time a user wants to refresh the cache, that is make any changes in the
    datapoint table avalaible to the API and the platform as a whole, the
    AggRefresh object is instatiated.  The flow of data is as follows:
        - Create a row in the ETL Job table.  This record will track the
          time each tasks takes, and in addition this ID is used as a key
          in the datapoints table so we can see when and why the cache was
          updated for this datapoint.
        - If the datapoint_id list is empty get the default (limit to 1000)
          list of datapoint_ids to process.
        - Find the indicator_ids (both computed and raw) that need to be
          processed.
        - Executes stored pSQL stored procedures to first aggregate, then
          calculate information.
    '''


    def __init__(self,datapoint_id_list=None):
        '''
        If there is a job running, return to with a status code of
        "cache_running".

        If passed an explicit list of datapoints ids, then we process those
        other wise the datapoint IDs to process are handled in the set_up()
        method.

        By initializing this class we run the set_up() method followed my the
        main method. We capture and store any errors returned in the etljob
        table as well as the start / end time.
        '''

        if CacheJob.objects.filter(date_completed=None):
            return

        self.datapoint_id_list = datapoint_id_list

        # set up and run the cache job
        response_msg = self.set_up()

        if response_msg != 'NOTHING_TO_PROCESS':
            response_msg = self.main()

            if response_msg == 'ERROR':
                self.cache_job.response_msg = str(self.err)[:254]
                self.cache_job.date_completed = datetime.now()
                self.is_error = True
                self.cache_job.save()
                return

        # mark job as completed and save
        self.cache_job.date_completed = datetime.now()
        self.cache_job.response_msg = response_msg
        self.cache_job.save()

    def set_up(self):
        '''
        First reate a row in the ``source_data_etl_job`` table.  This table
        will store when the cache_task was created, when it was complete, and
        what the status of the job is.

        Next, this method finds the datapoint ids that it will use to run the
        cache job using ``AggRefresh.get_datapoints_to_cache()``.  Only data that is relevenat to these datapoint ids should be
        altered.  That includes any data for parents of the associated datapoints
        as well as any indicators that are stored as the result of the
        calculation on the underlying datapoints.

        Finally this method calls ``AggRefresh.get_indicator_ids()`` to get
        indicators needed to loop through ( both raw and computed ) that will
        need to be refreshed.

        TO DO
        -----
        Every datapoint should have a cache_job_id so we can see when and why
        a particular datapoint was cached.

        '''

        self.cache_job = CacheJob.objects.create(
            is_error = False,
            response_msg = 'PENDING'
        )

        if self.datapoint_id_list is None:
            self.datapoint_id_list = self.get_datapoints_to_cache()

            if len(self.datapoint_id_list) == 0:
                return 'NOTHING_TO_PROCESS'

        self.set_cache_job_id_for_raw_datapoints()

        self.campaign_id = DataPoint.objects.filter(cache_job_id = \
            self.cache_job.id)[0].value

        return 'PENDING_AGG'

    def main(self):
        '''
        '''

        try:
            cache_job_id = self.cache_job.id
        except AttributeError:
            return 'PENDING'

        # try:
        self.agg_datapoints()
        self.calc_dp_ids = self.calc_datapoints()
        # except Exception as err:
        #     self.err = traceback.format_exc()
        #     return 'ERROR'

        return 'SUCCESS'

    def set_cache_job_id_for_raw_datapoints(self):
        '''
        After we find what datapoint IDs need to be refreshed, we set the
        cache_job_id coorespondonding to the current job so we can find
        these datapoints easily both within this class, and for engineers /
        analysts debugging the cache process
        '''

        dp_curs = DataPoint.objects.raw('''

            UPDATE datapoint
            SET cache_job_id = %s
            WHERE id = ANY(%s);

            SELECT ID from datapoint LIMIT 1;

        ''',[self.cache_job.id,self.datapoint_id_list])

        x = [dp.id for dp in dp_curs]


    def agg_datapoints(self):
        '''
        Regional Aggregation based on the adjacency list built on top of the
        parent_location_id column.

        Data stored in the DataPoint table for a location with the same
        indicator, campaign will always override the aggregated values.
        '''

        agg_dp_batch = []

        datapoint_columns =['indicator_id','campaign_id', 'location_id',\
            'value','cache_job_id']

        location_tree_columns = ['location_id','parent_location_id']

        dp_df = DataFrame(list(DataPoint.objects\
            .filter(cache_job_id = self.cache_job.id)\
            .values_list(*datapoint_columns)),columns=datapoint_columns)

        location_id_list = list(dp_df['location_id'].unique())
        location_tree_df = DataFrame(list(LocationTree.objects\
            .filter(location_id__in=location_id_list)
            .values_list(*location_tree_columns)),columns=location_tree_columns)

        merged_df = dp_df.merge(location_tree_df)
        grouped_df = DataFrame(merged_df.groupby(['parent_location_id', 'campaign_id',\
            'indicator_id'])['value'].sum())

        # final_df = pd.concat(merged_df, grouped_df)
        # for dp in final_df:
        for ix, dp in dp_df.iterrows():
            agg_dp_batch.append(AggDataPoint(**dp.to_dict()))

        AggDataPoint.objects.filter(campaign_id = self.campaign_id).delete()
        AggDataPoint.objects.bulk_create(agg_dp_batch)

    def calc_datapoints(self):
        '''
        When the agg_datapoint method runs, it will leave the agg_datapoint table
        in a state that all of the rows that were altered, and need to be cached
        thats is the ``calc_refreshed`` column will = 'f' for all of the rows
        that this task effected.

        To find out more about how calculation works, take a look at the
        fn_calc_datapoint stored procedures

        '''

        self.calc_prep()
        self.sum_of_parts()
        self.part_over_whole()
        self.part_of_difference()
        self.upsert_computed()

        return []

    def calc_prep(self):

        raw_qs = AggDataPoint.objects.raw('''

        DROP TABLE IF EXISTS _tmp_calc_datapoint;
        CREATE TABLE _tmp_calc_datapoint AS
        SELECT DISTINCT
            ad.id
            ,ad.location_id
            ,ad.campaign_id
            ,ad.indicator_id
            ,ad.value
            ,ad.cache_job_id
        FROM agg_datapoint ad
        WHERE ad.cache_job_id = %s;

        CREATE UNIQUE INDEX uq_ix ON _tmp_calc_datapoint (location_id,
            campaign_id, indicator_id);

        -- FIX --
        DELETE FROM _tmp_calc_datapoint WHERE value = 'NaN';

        SELECT * FROM agg_datapoint
        LIMIT 1;

        ''',[self.cache_job.id])

        return [x.id for x in raw_qs]

    def sum_of_parts(self):
        '''
        For more info on this see:
        https://github.com/unicef/rhizome/blob/master/docs/spec.rst#aggregation-and-calculation

        '''

        raw_qs = AggDataPoint.objects.raw('''

        -- THIS QUERY ENSURES THAT IF DATA IS STORED AT A HIGHER lvl
        -- THEN IT's SUB COMPONENTS, DATA AT THE HIGHER LEVEL WINS
            --> for instance, if i have data stored at indicator_id 251
            --> as well as the component indicators of 251 ( 24,251,267,268,264 )
            --> we will take the data for 251 over it's sub-components

        INSERT INTO _tmp_calc_datapoint
        (indicator_id,location_id,campaign_id,value,cache_job_id)

        SELECT
        cic.indicator_id
          , dwc.location_id
          , dwc.campaign_id
          , SUM(COALESCE(dwc.value,0.00)) as agg_value
          , %s
        FROM calculated_indicator_component cic
        INNER JOIN _tmp_calc_datapoint dwc
        ON 1 = 1
        AND cic.indicator_component_id = dwc.indicator_id
        AND calculation = 'PART_TO_BE_SUMMED'
        AND NOT EXISTS (
          SELECT 1 FROM _tmp_calc_datapoint tcd
          WHERE dwc.location_id = tcd.location_id
          AND dwc.campaign_id = tcd.campaign_id
          AND cic.indicator_id = tcd.indicator_id
        )

        GROUP BY cic.indicator_id, dwc.location_id, dwc.campaign_id;

        -- THIS HANDLES INDICATORS WHERE THE SUM IS MULTI LAYERED see:
        -- http://rhizome.work/ufadmin/manage/indicator/21
        -- http://rhizome.work/ufadmin/manage/indicator/251

        WITH RECURSIVE ind_graph AS
        (
        -- non-recursive term ( rows where the components aren't
        -- master_indicators in another calculation )

      	SELECT
        		 cic.id
      		,cic.indicator_id
      		,cic.indicator_component_id
      		--,0 as lvl
      	FROM calculated_indicator_component cic
      	WHERE NOT EXISTS (
      		SELECT 1 FROM calculated_indicator_component cic_leaf
      		WHERE cic.indicator_component_id = cic_leaf.indicator_id
      	)
      	AND calculation = 'PART_TO_BE_SUMMED'

      	UNION ALL

      	-- recursive term --
      	SELECT
      		cic_recurs.id
      		,cic_recurs.indicator_id
      		,ig.indicator_component_id
      		--,ig.lvl + 1
      	FROM calculated_indicator_component AS cic_recurs
      	INNER JOIN ind_graph AS ig
      	ON (cic_recurs.indicator_component_id = ig.indicator_id)
      	AND calculation = 'PART_TO_BE_SUMMED'

        )

        INSERT INTO _tmp_calc_datapoint
        (indicator_id,location_id,campaign_id,value,cache_job_id)

        SELECT
            ig.indicator_id
          , dwc.location_id
          , dwc.campaign_id
          , SUM(COALESCE(dwc.value,0.00)) as agg_value
          , %s
        FROM ind_graph ig
        INNER JOIN _tmp_calc_datapoint dwc
            ON 1 = 1
            AND ig.indicator_component_id = dwc.indicator_id
        AND NOT EXISTS (
          SELECT 1 FROM _tmp_calc_datapoint tcd
          WHERE dwc.location_id = tcd.location_id
          AND dwc.campaign_id = tcd.campaign_id
          AND ig.indicator_id = tcd.indicator_id
        )
        GROUP BY ig.indicator_id, dwc.location_id, dwc.campaign_id;

    	SELECT ad.id FROM agg_datapoint ad
    	LIMIT 1;'''
        , [self.cache_job.id,self.cache_job.id])

        return [x.id for x in raw_qs]

    def part_over_whole(self):

        raw_qs = AggDataPoint.objects.raw('''
        INSERT INTO _tmp_calc_datapoint
        (indicator_id,location_id,campaign_id,value,cache_job_id)

        SELECT DISTINCT
            part.indicator_id as master_id
            ,d_part.location_id
            ,d_part.campaign_id
            ,d_part.value / NULLIF(d_whole.value,0) as value
            ,d_part.cache_job_id
        FROM calculated_indicator_component part
        INNER JOIN calculated_indicator_component whole
            ON part.indicator_id = whole.indicator_id
            AND whole.calculation = 'WHOLE'
            AND part.calculation = 'PART'
        INNER JOIN _tmp_calc_datapoint d_part
            ON part.indicator_component_id = d_part.indicator_id
        INNER JOIN _tmp_calc_datapoint d_whole
            ON whole.indicator_component_id = d_whole.indicator_id
            AND d_part.campaign_id = d_whole.campaign_id
            AND d_part.location_id = d_whole.location_id
        WHERE NOT EXISTS (
            SELECT 1 FROM _tmp_calc_datapoint tcd
            WHERE tcd.campaign_id = d_part.campaign_id
            AND tcd.location_id = d_part.location_id
            AND tcd.indicator_id = part.indicator_id
        );

        SELECT id FROM agg_datapoint limit 1;

        ''')

        return [x.id for x in raw_qs]

    def part_of_difference(self):

        raw_qs = AggDataPoint.objects.raw('''

        INSERT INTO _tmp_calc_datapoint
        (indicator_id,location_id,campaign_id,value,cache_job_id)

          SELECT x.indicator_id,x.location_id,x.campaign_id, x.calculated_value, %s
          FROM (
          SELECT DISTINCT
        		denom.master_id as indicator_id
        		,denom.location_id
        		,denom.campaign_id
        		,(CAST(num_whole.value as FLOAT) - CAST(num_part.value as FLOAT)) / NULLIF(CAST(denom.value AS FLOAT),0) as calculated_value
                  FROM (
                  	SELECT
                  		cic.indicator_id as master_id
                  		,ad.location_id
                  		,ad.indicator_id
                  		,ad.campaign_id
                  		,ad.value
                  	FROM _tmp_calc_datapoint ad
                  	INNER JOIN calculated_indicator_component cic
                  	ON cic.indicator_component_id = ad.indicator_id
                  	AND calculation = 'PART_OF_DIFFERENCE'
                  )num_part

              INNER JOIN (
              	SELECT
              		cic.indicator_id as master_id
              		,ad.location_id
              		,ad.indicator_id
              		,ad.campaign_id
              		,ad.value
              	FROM  _tmp_calc_datapoint ad
              	INNER JOIN calculated_indicator_component cic
              	ON cic.indicator_component_id = ad.indicator_id
              	AND calculation = 'WHOLE_OF_DIFFERENCE'
              )num_whole
              ON num_part.master_id = num_whole.master_id
              AND num_part.location_id = num_whole.location_id
              AND num_part.campaign_id = num_whole.campaign_id

              INNER JOIN
              (
              	SELECT
              		cic.indicator_id as master_id
              		,ad.location_id
              		,ad.indicator_id
              		,ad.campaign_id
              		,ad.value
              	FROM _tmp_calc_datapoint ad
              	INNER JOIN calculated_indicator_component cic
              	ON cic.indicator_component_id = ad.indicator_id
              	AND calculation = 'WHOLE_OF_DIFFERENCE_DENOMINATOR'
              )denom
              ON num_whole.location_id = denom.location_id
              AND num_whole.master_id = denom.master_id
              AND num_whole.campaign_id = denom.campaign_id
        )x
        WHERE NOT EXISTS (

        SELECT 1 FROM _tmp_calc_datapoint t
        WHERE x.location_id = t.location_id
        AND x.campaign_id = t.campaign_id
        AND x.indicator_id = t.indicator_id
        );

        SELECT id from agg_datapoint limit 1;

        ''',[self.cache_job.id])

        return [x.id for x in raw_qs]

    def upsert_computed(self):

        raw_qs = DataPointComputed.objects.raw('''

    	UPDATE datapoint_with_computed dwc
    		SET value = tcd.value
    			, cache_job_id = tcd.cache_job_id
    	FROM _tmp_calc_datapoint tcd
    	WHERE dwc.location_id = tcd.location_id
    	AND dwc.indicator_id = tcd.indicator_id
    	AND dwc.campaign_id = tcd.campaign_id
    	AND tcd.value IS NOT NULL ; -- FIXME

    	INSERT INTO datapoint_with_computed
    	(location_id, campaign_id, indicator_id, value, cache_job_id)

    	SELECT location_id, campaign_id, indicator_id, value, cache_job_id
    	FROM _tmp_calc_datapoint tcd
    	WHERE NOT EXISTS (
    		SELECT 1 FROM datapoint_with_computed dwc
    		WHERE tcd.location_id = dwc.location_id
    		AND tcd.campaign_id = dwc.campaign_id
    	 	AND tcd.indicator_id = dwc.indicator_id
    	)
    	AND tcd.value IS NOT NULL; -- FIXME

    	SELECT ad.id FROM datapoint_with_computed ad
    	WHERE ad.cache_job_id = %s
    	LIMIT 1;
        ''',[self.cache_job.id])

        return [x.id for x in raw_qs]


    def get_datapoints_to_cache(self,limit=None):
        '''
        Since there are complicated dependencies for location aggregation, as
        well as the interrationship between indicators, processing one campaign
        at a time makes our code much simpler.
        '''

        dps = DataPoint.objects.raw('''
            SELECT id from datapoint d
            WHERE cache_job_id = -1
            AND campaign_id in ( -- one campaign at a time
                SELECT campaign_id FROM datapoint d2
                WHERE cache_job_id = -1
                LIMIT 1
            )
        ''')

        dp_ids = [row.id for row in dps]

        return dp_ids

    def get_location_ids_to_process(self):

        location_cursor = location.objects.raw('''
            SELECT DISTINCT
                location_id as id
            FROM datapoint d
            WHERE cache_job_id = %s''',[self.cache_job.id])

        location_ids = [r.id for r in location_cursor]

        return location_ids


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


def cache_user_abstracted():
    '''
    Just like indicator_abstracted, the user_abstraced table holds information
    that is keyed to the user, for instance, their groups and location permission.

    This data is cached in the cache_metadata process so the API is able to
    return data without transformation.
    '''

    u_raw = User.objects.raw(
    '''
        SELECT
		  	 au.id
   		  	,au.id as user_id
            ,au.last_login
        	,au.is_superuser
        	,au.username
        	,au.first_name
        	,au.last_name
        	,au.email
        	,au.is_staff
        	,au.is_active
        	,au.date_joined
			,gr.group_json
            ,rp.location_permission_json
        FROM auth_user au
        LEFT JOIN (
        	SELECT
        		 aug.user_id
        		,json_agg(row_to_json(aug.*)) AS group_json
        	FROM auth_user_groups aug
        	GROUP BY aug.user_id
        ) gr
        ON au.id = gr.user_id
        LEFT JOIN (
        	SELECT
        		 rp.user_id
        		,json_agg(row_to_json(rp.*)) as location_permission_json
        	FROM location_permission rp
        	GROUP BY rp.user_id
        ) rp
        ON au.id = rp.user_id
    '''
    )

    upsert_meta_data(u_raw, UserAbstracted)


def cache_campaign_abstracted():
    '''
    Add the pct-complete to the campaign based ont he pct of management
    indiators present for that campaign for the top level locations.
    '''

    ## temporarily harcoding indicators until we get management dashboard
    ## definition loading from the api... see:
    ## https://trello.com/c/nHSev5t9/226-8-front-end-api-calls-use-indicator-tag-to-populate-charts-and-dashboards

    all_indicators = [168, 431, 432, 433, 166, 164, 167, 165, 475, 187, 189, \
    27, 28, 175, 176, 177, 204, 178, 228, 179, 184, 180, 185, 230, 226, 239, \
    245, 236, 192, 193, 191, 194, 219, 173, 172, 169, 233, 158, 174, 442, 443, \
    444, 445, 446, 447, 448, 449, 450]

    # How many indicators does the ultimate parent have for each campaign #
    c_raw = Campaign.objects.raw(
        '''
        SELECT
            campaign_id as id
            ,COUNT(1) as indicator_cnt
        FROM datapoint_with_computed dwc
        WHERE indicator_id = ANY(%s)
        AND location_id IN (
            SELECT id FROM location l
            WHERE l.parent_location_id IS NULL
        )
        GROUP BY campaign_id;
        ''',[all_indicators])

    for c in c_raw:
        c_obj = Campaign.objects.get(id=c.id)
        c_obj.management_dash_pct_complete = c.indicator_cnt / \
            float(len(list(set(all_indicators))))
        c_obj.save()


def cache_location_tree():

    rt_raw = LocationTree.objects.raw(
    '''
    TRUNCATE TABLE location_tree;


    INSERT INTO location_tree
    (parent_location_id, immediate_parent_id, location_id, lvl)


    WITH RECURSIVE location_tree(parent_location_id, immediate_parent_id, location_id, lvl) AS
    (

    SELECT
    	rg.parent_location_id
    	,rg.parent_location_id as immediate_parent_id
    	,rg.id as location_id
    	,1 as lvl
    FROM location rg

    UNION ALL

    -- recursive term --
    SELECT
    	r_recurs.parent_location_id
    	,rt.parent_location_id as immediate_parent_id
    	,rt.location_id
    	,rt.lvl + 1
    FROM location AS r_recurs
    INNER JOIN location_tree AS rt
    ON (r_recurs.id = rt.parent_location_id)
    AND r_recurs.parent_location_id IS NOT NULL
    )

    SELECT
    	COALESCE(parent_location_id, location_id)  AS parent_location_id
    	,COALESCE(immediate_parent_id, location_id)  AS immediate_parent_id
    	,location_id
    	,lvl
    FROM location_tree;

    SELECT * FROM location_tree;
    ''')

    for x in rt_raw:
        pass # in order to execute raw sql


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
