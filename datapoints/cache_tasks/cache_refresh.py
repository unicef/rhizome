import traceback

# from pandas import DataFrame

from datapoints.models import DataPoint


class CacheRefresh(object):

    def __init__(self,datapoint_id_list=None):
        '''
        '''

        if datapoint_id_list is None:
            self.datapoint_id_list = self.get_datapoints_to_cache()

        self.rc_loop = self.get_rc_loop()


    def get_datapoints_to_cache(self):
        '''
        Called on __init__ to find the unprocessed datapoints that need to be
        cached.  If the datapoint_id_list parameter is provided when the class
        is instantiated, this method need not be called.
        '''

        dps = DataPoint.objects.raw('''
            SELECT id from datapoint
            WHERE is_cached = 'f'
            LIMIT 1000
        ''')

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
