import pandas as pd
from pandas import DataFrame, read_sql
from pandas.tools.pivot import pivot_table

from datapoints.models import *
from source_data.models import EtlJob

class CacheRefresh(object):
    '''
    Any time a user wants to refresh the cache, that is make any changes in the
    datapoint table avalaible to the API and the platform as a whole, the
    CacheRefresh object is instatiated.  The flow of data is as follows:
     - Create a table in the ETL Job table.  This record will track the
       time each tasks takes, and in addition this ID is used as a key
       in the datapoints table so we can see when and why the cache was
       updated for this datapoint.
     - If the datapoint_id list is empty get the default (limit to 1000)
       list of datapoint_ids to process.
     - Find the indicator_ids (both computed and raw) that need to be
       processed.
     - Executes stored pSQL stored procedures to first aggregate, then
       calculat information.
     - Deletes, then re-inserts relevant rows in the datapoint_abstracted
       table.
    '''

    def __init__(self,datapoint_id_list=None):
        '''
        '''

        self.set_up()
        self.main()

        cache_job.status = task_result

    def set_up(self):
        '''
        Create a row in the etl_job table.  Find all required meta data needed
        for later in the cache process.
        '''
        cache_job = EtlJob.objects.create(
            task_name = 'cache_refresh',
            status = 'pending',
            cron_guid = 'test_cron_guid',
            success_msg = 'test',
        )

        if datapoint_id_list is None:
            self.datapoint_id_list = self.get_datapoints_to_cache()
        else:
            self.datapoint_id_list = datapoint_id_list

        self.indicator_ids = self.get_indicator_ids()

        task_result = self.main()


    def main(self):
        '''
          - execute the "agg_datapoint" sproc for the given datapoint_ids.
          - excecute the "calc_datapoint" sproc for the given datapoint_id.
          - return the result to be stored in the etl_job table.
        '''

        task_result = 'SUCCESS'

        self.agg_datapoints()
        # self.calc_datapoints()

        self.mark_datapoints_as_cached()

        return task_result

    def agg_datapoints(self):
        '''
        agg_datapoints
        '''

        init_curs = AggDataPoint.objects\
            .raw("SELECT * FROM fn_init_agg_datapoint()")

        y = [x for x in init_curs]


    def get_indicator_ids(self):
        '''
        TO DO - Make sure you get the computed indicators as well
        '''

        curs = Indicator.objects.raw('''

            SELECT distinct indicator_id as id
            FROM datapoint
            WHERE id = ANY (%s);

        ''',[self.datapoint_id_list])

        indicator_ids = [ind.id for ind in curs]

        return indicator_ids

    def mark_datapoints_as_cached(self):
        '''
        After successfully caching the changed datapoints, mark them as cached.
        '''
        dp = DataPoint.objects.raw('''

            UPDATE datapoint
            SET is_cached = 't'
            WHERE id = ANY (%s);

            SELECT id FROM datapoint limit 1;

        ''',[self.datapoint_id_list])

        x = [d.id for d in dp]


    def get_datapoints_to_cache(self,limit=None):
        '''
        Called on __init__ to find the unprocessed datapoints that need to be
        cached.  If the datapoint_id_list parameter is provided when the class
        is instantiated, this method need not be called.  If there is no
        limit provided to this method, the default limit is set to 1000.
        '''

        if limit is None:
            limit = 1000

        dps = DataPoint.objects.raw('''
            SELECT id from datapoint
            WHERE is_cached = 'f'
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
