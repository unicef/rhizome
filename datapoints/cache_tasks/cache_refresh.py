
from datapoints.models import DataPoint, Indicator, AggDataPoint
from source_data.models import EtlJob

class CacheRefresh(object):

    def __init__(self,datapoint_id_list=None):
        '''
        Create a table in the ETL Job table.  If the datapoint_id list is empty
        get the default (limit to 1000) list of datapoint_ids to run through
        the cache process.
        '''

        cache_job = EtlJob.objects.create(
            task_name = 'cache_refresh',
            status = 'pending',
            cron_guid = 'test_cron_guid',
            success_msg = 'test',
        )

        if datapoint_id_list is None:
            self.datapoint_id_list = self.get_datapoints_to_cache()

        self.indicator_ids = self.get_indicator_ids()

        task_result = self.main()

        cache_job.status = task_result

    def main(self):

        task_result = 'SUCCESS'

        self.agg_datapoints()
        # self.calc_datapoints()

        self.mark_datapoints_as_cached()

        return task_result

    def agg_datapoints(self):

        init_curs = AggDataPoint.objects\
            .raw("SELECT * FROM fn_init_agg_datapoint()")

        y = [x for x in init_curs]


    def get_indicator_ids(self):

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
