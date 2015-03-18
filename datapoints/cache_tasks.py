import pandas as pd
from pandas import DataFrame, read_sql
from pandas.tools.pivot import pivot_table

from datapoints.models import *

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
        '''

        self.datapoint_id_list = datapoint_id_list

        # set up and run the cache job
        self.cache_job = self.set_up()
        self.cache_job.response_msg = self.main()

        # mark job as completed and save
        self.cache_job.date_completed = datetime.now()
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

        Finall this method calls ``CacheRefresh.get_indicator_ids()`` to get
        indicators needed to loop through ( both raw and computed ) that will
        need to be refreshed.

        TO DO
        -----
        Every datapoint should have a cache_job_id so we can see when and why
        a particular datapoint was cached.

        '''
        cache_job = CacheJob.objects.create(
            is_error = False,
            response_msg = 'PENDING'
        )

        if self.datapoint_id_list is None:
            self.datapoint_id_list = self.get_datapoints_to_cache()

        self.indicator_ids = self.get_indicator_ids()

        return cache_job

    def main(self):
        '''
        For the given datapoint_ids ( self.datapoint_id_list )
          - execute the "agg_datapoint".
          - excecute the "calc_datapoint" sproc.
          - return the result to be stored in the etl_job table.
        '''

        task_result = 'SUCCESS'

        self.set_cache_job_id_for_raw_datapoints()

        agg_dp_ids = self.agg_datapoints()

        # self.calc_datapoints()

        return task_result

    def set_cache_job_id_for_raw_datapoints(self):
        '''
        After we find what datapoint IDs need to be refreshed, we set the
        cache_job_id coorespondonding to the current job so we can find
        these datapoints easily both within this class, and for engineers /
        analysts debugging the cache process
        '''

        dp_ids = DataPoint.objects.raw('''
            UPDATE datapoint
            SET cache_job_id = %s
            WHERE id = ANY(%s)
        ''',[self.cache_job.id,self.datapoint_id_list])


    def agg_datapoints(self):
        '''
        Datapoints are aggregated in two steps with two separate stored
        procedures.
          - init_agg_datapoints : save all of the raw (non aggregated) data
          - agg_datapoints_by_region_type: given

        This method first calls the ``fn_init_agg_datapoint`` and then calls ``
        agg_datapoints_by_region_type`` for each region_type starting from the
        leaf level and moving up to the country level.

        It is important that this function touches as little data as possible
        while altering exactly the data that needs to be altered for the latest
        updates to effect aggregation

        TO DO:
            - add region_type_sproc in this method
            - Add datapoint_id_list as a param to both of these sprocs
            - look into more closely why a purely recursive query wont work.
              My initial diagnosis was that there was bad parent/child data in
              the regions table but currenlty when i look at regions with parents
              of the same region_type all I see is Kirachi.
        '''

        agg_cursor = AggDataPoint.objects\
            .raw("SELECT * FROM fn_agg_datapoint(%s)",[self.cache_job.id])

        agg_dp_ids = [x.id for x in agg_cursor]

        return agg_dp_ids


    def calc_datapoints(self):
        '''
        When the agg_datapoint method runs, it will leave the agg_datapoitn table
        in a state that all of the rows that were altered, and need to be cached
        thats is the ``calc_refreshed`` column will = 'f' for all of the rows
        that this task effected.

        To find out more about how calculation works, take a look at the
        fn_calc_datapoint stored procedures

        '''

        calc_curs = AggDataPoint.objects\
            .raw("SELECT * FROM fn_init_calc_datapoint()")

        y = [x for x in calc_curs]


    def get_indicator_ids(self):
        '''
        Given the raw indicator ids for the datapoints to process, find all
        of the indicator ids that will need to be effected by the calculations.
        That includes the computed indicators that need to be effected by
        updates in the underliying data, as well as the raw indicators.
        '''


        print self.datapoint_id_list
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
            limit = 100

        dps = DataPoint.objects.raw('''
            SELECT id from datapoint
            WHERE cache_job_id = -1
            LIMIT %s
        ''',[limit])

        dp_ids = [row.id for row in dps]

        return dp_ids

    def get_abstracted_datapoint_ids(self):
        '''
        Being as that the cache table the API uses to provide data to the site
        is stored with a unique key of region_id, campaign_id we need this data
        in order to figure out what data we will need to delete from the
        datapoint_abstracted table

        This will also need to take into consideration the parent region Ids

        '''
        rc_raw = DataPoint.objects.raw('''
            SELECT
                  MIN(id) as id
                , region_id
                , campaign_id
            FROM datapoint
            WHERE id = ANY (%s)
            GROUP BY region_id, campaign_id''',[self.datapoint_id_list])

        rc_list_of_tuples = [(rc.region_id,rc.campaign_id) for rc in rc_raw]

        return rc_list_of_tuples

def computed_datapoint_to_abstracted_datapoint():

    indicator_raw = DataPoint.objects.raw("""
        SELECT DISTINCT 1 as id, indicator_id from datapoint_with_computed
        ORDER BY indicator_id DESC""")

    all_indicator_ids = [x.indicator_id for x in indicator_raw]
    indicator_df = DataFrame(columns = all_indicator_ids)

    distict_region_campaign_list = DataPoint.objects.raw("""
        SELECT DISTINCT
        	1 as id
        	, dwc.region_id
        	, dwc.campaign_id
        FROM datapoint_with_computed dwc
        INNER JOIN region r
        ON dwc.region_id = r.id
        INNER JOIN campaign c
        ON dwc.campaign_id = c.id
        AND r.office_id = c.office_id
        WHERE region_id is NOT NULL;
        """)

    rc_tuple_list = []
    for rc in distict_region_campaign_list:

        r_c_tuple = (rc.region_id,rc.campaign_id)
        rc_tuple_list.append(r_c_tuple)


    rc_df = DataFrame(rc_tuple_list,columns=['region_id','campaign_id'])
    rc_df = rc_df.reset_index(level=[0,1])

    for i,(i_id) in enumerate(all_indicator_ids):

        rc_df = add_indicator_data_to_rc_df(rc_df, i_id)

    r_c_df_to_db(rc_df)

def add_indicator_data_to_rc_df(rc_df, i_id):
    '''
    left join the region / campaign dataframe with the stored data for each
    campaign.
    '''
    column_header = ['region_id','campaign_id']
    column_header.append(i_id)

    indicator_df = DataFrame(list(DataPointComputed.objects.filter(
        indicator_id = i_id).values()))

    pivoted_indicator_df = pivot_table(indicator_df, values='value',\
        columns=['indicator_id'],index = ['region_id','campaign_id'])


    cleaned_df = pivoted_indicator_df.reset_index(level=[0,1], inplace=False)

    merged_df = rc_df.merge(cleaned_df,how='left')
    merged_df = merged_df.reset_index(drop=True)

    return merged_df


def r_c_df_to_db(rc_df):

    nan_to_null_df = rc_df.where((pd.notnull(rc_df)), None)
    indexed_df = nan_to_null_df.reset_index(drop=True)
    rc_dict = indexed_df.transpose().to_dict()

    batch = []

    for r_no, r_data in rc_dict.iteritems():

        region_id, campaign_id = r_data['region_id'],r_data['campaign_id']

        del r_data["index"]
        del r_data["region_id"]
        del r_data["campaign_id"]

        dd_abstracted = {
            "region_id": region_id,
            "campaign_id":campaign_id,
            "indicator_json": r_data
        }

        dda_obj = DataPointAbstracted(**dd_abstracted)

        batch.append(dda_obj)

    DataPointAbstracted.objects.all().delete()

    DataPointAbstracted.objects.bulk_create(batch)
