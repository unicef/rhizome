import pandas as pd
from pandas import DataFrame, read_sql
from pandas.tools.pivot import pivot_table

from django.contrib.auth.models import User
from datapoints.models import *
from source_data.models import SourceObjectMap

class CacheRefresh(object):
    '''
    Any time a user wants to refresh the cache, that is make any changes in the
    datapoint table avalaible to the API and the platform as a whole, the
    CacheRefresh object is instatiated.  The flow of data is as follows:
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
        - Deletes, then re-inserts relevant rows in the datapoint_abstracted
          table.
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
            print 'CACHE_RUNNING'
            return

        self.datapoint_id_list = datapoint_id_list

        # set up and run the cache job
        response_msg = self.set_up()

        if response_msg != 'NOTHING_TO_PROCESS':
            try:
                response_msg = self.main()
            ## BLINDLY CATCH AND STORE ALL ERRORS ##
            except Exception as err:

                self.cache_job.date_completed = datetime.now()
                self.cache_job.response_msg = str(err)[:254]
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
        cache job using ``CacheRefresh.get_datapoints_to_cache()``.  Only data that is relevenat to these datapoint ids should be
        altered.  That includes any data for parents of the associated datapoints
        as well as any indicators that are stored as the result of the
        calculation on the underlying datapoints.

        Finally this method calls ``CacheRefresh.get_indicator_ids()`` to get
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

        self.indicator_ids = self.get_indicator_ids()

        return 'PENDING_AGG'

    def main(self):
        '''
        For the given datapoint_ids ( self.datapoint_id_list )
          - execute the "agg_datapoint".
          - excecute the "calc_datapoint" sproc.
          - return the result to be stored in the etl_job table.
        '''

        try:
            cache_job_id = self.cache_job.id
        except AttributeError:
            return 'PENDING'

        self.agg_dp_ids = self.agg_datapoints()
        self.calc_dp_ids = self.calc_datapoints()
        self.abstract_dp_ids = self.pivot_datapoints()

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
        Datapoints are aggregated in two steps with two separate stored
        procedures.
          - init_agg_datapoints : save all of the raw (non aggregated) data
          - agg_datapoints_by_location_type: given

        This method first calls the ``fn_init_agg_datapoint`` and then calls ``
        agg_datapoints_by_location_type`` for each location_type starting from the
        leaf level and moving up to the country level.

        It is important that this function touches as little data as possible
        while altering exactly the data that needs to be altered for the latest
        updates to effect aggregation

        TO DO:
            - add location_type_sproc in this method
            - Add datapoint_id_list as a param to both of these sprocs
            - look into more closely why a purely recursive query wont work.
              My initial diagnosis was that there was bad parent/child data in
              the locations table but currenlty when i look at locations with parents
              of the same location_type all I see is Kirachi.
        '''

        adp_cursor = DataPoint.objects.raw("""
            SELECT * FROM fn_agg_datapoint(%s);
            """,[self.cache_job.id])

        adps = [adp.id for adp in adp_cursor]

        return []


    def calc_datapoints(self):
        '''
        When the agg_datapoint method runs, it will leave the agg_datapoint table
        in a state that all of the rows that were altered, and need to be cached
        thats is the ``calc_refreshed`` column will = 'f' for all of the rows
        that this task effected.

        To find out more about how calculation works, take a look at the
        fn_calc_datapoint stored procedures

        '''

        calc_curs = AggDataPoint.objects\
            .raw("SELECT * FROM fn_calc_datapoint(%s)",[self.cache_job.id])

        calc_dp_ids = [x.id for x in calc_curs]

        return calc_dp_ids


    def get_indicator_ids(self):
        '''
        Given the raw indicator ids for the datapoints to process, find all
        of the indicator ids that will need to be effected by the calculations.
        That includes the computed indicators that need to be effected by
        updates in the underliying data, as well as the raw indicators.
        '''

        curs = Indicator.objects.raw('''

        DROP TABLE IF EXISTS _raw_indicators;
        CREATE TEMP TABLE _raw_indicators
        AS
        SELECT distinct indicator_id
        FROM datapoint
        WHERE id = ANY (%s);

        SELECT x.indicator_id as id FROM (

            SELECT cic.indicator_id
            FROM calculated_indicator_component cic
                INNER JOIN _raw_indicators ri
                ON cic.indicator_component_id = ri.indicator_id


            UNION ALL

            SELECT indicator_id from _raw_indicators
        ) x;

        ''',[self.datapoint_id_list])

        indicator_ids = [ind.id for ind in curs]

        return indicator_ids


    def get_datapoints_to_cache(self,limit=None):
        '''
        Called as a part of the ``set_up()`` method to find the unprocessed
        datapoints that need to be cached.  If the datapoint_id_list parameter
        is provided when the class is instantiated, this method need not be
        called.  If there is no limit provided to this method, the default
        limit is set to 100.
        '''

        if limit is None:
            limit = 250

        dps = DataPoint.objects.raw('''
            SELECT id from datapoint d
            WHERE cache_job_id = -1
            AND campaign_id in ( -- one campaign at a time
                SELECT campaign_id FROM datapoint d2
                WHERE cache_job_id = -1
                LIMIT 1
            )
            ORDER BY d.indicator_id
            LIMIT %s
        ''',[limit])

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


    def get_abstracted_datapoint_ids(self):
        '''
        Being as that the cache table the API uses to provide data to the site
        is stored with a unique key of location_id, campaign_id we need this data
        in order to figure out what data we will need to delete from the
        datapoint_abstracted table

        This will also need to take into consideration the parent location Ids

        '''
        rc_raw = DataPoint.objects.raw('''
            SELECT
                  MIN(id) as id
                , location_id
                , campaign_id
            FROM datapoint
            WHERE id = ANY (%s)
            GROUP BY location_id, campaign_id''',[self.datapoint_id_list])

        rc_list_of_tuples = [(rc.location_id,rc.campaign_id) for rc in rc_raw]

        return rc_list_of_tuples

    def pivot_datapoints(self):
        '''
        Once the datapoint_with_computed table is refreshed, all of the raw
        aggregated and calculated data is transformed into a format friendly
        for the api.

        location_id | campaign_id | indicator_json

        Think of the data explorer and how the campaign / location are the unique
        keys to each row, and the requested indicators are the headers.

        Unlike the other two cache methods ( agg_datapoint, and calc_datapoint)
        this transformation is dealt with in python, primary because, python
        makes it easy to serialize the JSON and stick it into the abstracted
        datapoint table.
        '''

        ## We need to get data for indicators that weren't necessarily created
        ## with thie Cache Job ID.  That is, we need to process all of the
        ## indicators that exists for the locations and campaigns that we are
        ## processing.  If we just say "give me all the indicators for this
        ## cache job id" we will end up not storing valid data stored in a prior
        ## cache.

        indicator_raw = Indicator.objects.raw("""
            SELECT DISTINCT dwc.indicator_id as id
            FROM datapoint_with_computed dwc
            WHERE EXISTS (
                SELECT 1 FROM datapoint_with_computed dwc_cache_job
                WHERE dwc_cache_job.cache_job_id = %s
                AND dwc.location_id = dwc_cache_job.location_id
                AND dwc.campaign_id = dwc_cache_job.campaign_id
            )
            """,[self.cache_job.id])

        all_indicator_ids = [x.id for x in indicator_raw]
        indicator_df = DataFrame(columns = all_indicator_ids)

        rc_curs = DataPointComputed.objects.raw("""
            SELECT DISTINCT
                MIN(dwc.id) as id
                , dwc.location_id
                , dwc.campaign_id
            FROM datapoint_with_computed dwc
            INNER JOIN location r
                ON dwc.location_id = r.id
            INNER JOIN campaign c
                ON dwc.campaign_id = c.id
                AND c.office_id = r.office_id
            WHERE dwc.cache_job_id = %s
            GROUP BY dwc.location_id, dwc.campaign_id;
            """,[self.cache_job.id])


        rc_tuple_list = [(rc.location_id,rc.campaign_id) for rc in rc_curs]

        rc_df = DataFrame(rc_tuple_list,columns=['location_id','campaign_id'])
        rc_df = rc_df.reset_index(level=[0,1])

        for i,(i_id) in enumerate(all_indicator_ids):

            rc_df = self.add_indicator_data_to_rc_df(rc_df, i_id)

        self.r_c_df_to_db(rc_df)

    def add_indicator_data_to_rc_df(self,rc_df, i_id):
        '''
        left join the location / campaign dataframe with the stored data for each
        campaign.
        '''
        column_header = ['location_id','campaign_id']
        column_header.append(i_id)

        indicator_df = DataFrame(list(DataPointComputed.objects.filter(
            indicator_id = i_id).values()))

        pivoted_indicator_df = pivot_table(indicator_df, values='value',\
            columns=['indicator_id'],index = ['location_id','campaign_id'])

        cleaned_df = pivoted_indicator_df.reset_index(level=[0,1], inplace=False)

        merged_df = rc_df.merge(cleaned_df,how='left')
        merged_df = merged_df.reset_index(drop=True)

        return merged_df


    def r_c_df_to_db(self,rc_df):
        '''
        For each row in the transformed data frame:
            - convert all NaN to NULL
            - drop the index of the dataframe
            - transorm the above dataframe and convert to a dictionary in which
              the index ( or row number ) is the key, and the data is the
              location_id, campaign_id, and indicator_json needed to create
              each row in datapoint_abstracted.

        NOTE: This is the final stage of the cache as it stands right now.
        Currently due to simplicity and the size of the data, this step uses
        Postgres as the backend for our cache.  The style however of the schema
        is very much influenced by redis/memcache and is set up so that the
        transition from postgres to a more modern data store is as simple as
        possible.
        '''

        nan_to_null_df = rc_df.where((pd.notnull(rc_df)), None)
        indexed_df = nan_to_null_df.reset_index(drop=True)
        rc_dict = indexed_df.transpose().to_dict()

        batch = []

        for r_no, r_data in rc_dict.iteritems():

            location_id, campaign_id = r_data['location_id'],r_data['campaign_id']

            del r_data["index"]
            del r_data["location_id"]
            del r_data["campaign_id"]

            dd_abstracted = {
                "location_id": location_id,
                "campaign_id":campaign_id,
                "indicator_json": r_data,
                "cache_job_id": self.cache_job.id,
            }

            dda_obj = DataPointAbstracted(**dd_abstracted)

            batch.append(dda_obj)

        da_curs = DataPoint.objects.raw('''

            DELETE FROM datapoint_abstracted da
            USING datapoint_with_computed dwc
            WHERE da.location_id = dwc.location_id
            AND da.campaign_id = dwc.campaign_id
            AND dwc.cache_job_id = %s;

            SELECT id FROM datapoint limit 1;

        ''',[self.cache_job.id])

        da_id = [x.id for x in da_curs]

        DataPointAbstracted.objects.bulk_create(batch)


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
        '''

        rs_raw = ResultStructure.objects.raw(
        '''
        DROP TABLE IF EXISTS campaign_cnt;
        CREATE TEMP TABLE campaign_cnt
        AS

    	SELECT c.id as result_structure_id, coalesce(dp_cnt, 0) as dp_cnt FROM result_structure c
    	LEFT JOIN (
    		SELECT result_structure_id, COUNT(1) as dp_cnt
    		FROM datapoint
    		GROUP BY result_structure_id
    	)x
    	ON c.id = x.result_structure_id;


        SELECT DISTINCT
            c.*
            ,COALESCE(CAST(ccnt.dp_cnt AS FLOAT) / CAST(NULLIF(x.max_dp_cnt,0) AS FLOAT),0) as pct_complete
        FROM result_structure c
        INNER JOIN campaign_cnt ccnt
            ON c.id = ccnt.result_structure_id
        INNER JOIN (
            SELECT c.office_id, max(dp_cnt) as max_dp_cnt
            FROM campaign_cnt cc
            INNER JOIN result_structure c
            ON cc.result_structure_id = c.id
            GROUP BY c.office_id
        )x
            ON c.office_id = x.office_id;
        ''')

        upsert_meta_data(rs_raw, ResultStructureAbstracted)


def cache_location_tree():

    rt_raw = locationTree.objects.raw(
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
