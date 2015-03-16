import traceback

# from pandas import DataFrame

from datapoints.models import DataPoint


class CacheRefresh(object):

    def __init__(self,datapoint_id_list=None):

        if datapoint_id_list is None:
            self.datapoint_id_list = self.get_datapoints_to_cache(self)


        self.sdp_df = DataFrame(list(SourceDataPoint.objects\
            .filter(document_id = self.document_id).values()))



    def get_datapoints_to_cache(self):

        dps = DataPoint.objects.raw('''
            SELECT id from datapoint
            WHERE is_cached = 'f'
        ''')
