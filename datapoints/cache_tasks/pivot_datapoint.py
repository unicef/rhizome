from pprint import pprint
import numpy as np
from pandas import DataFrame

from datapoints.models import DataPoint


def full_cache_refresh():

    indicator_ids = list(set(DataPoint.objects.all()\
        .values_list('indicator_id',flat=True)))


    indicator_df = DataFrame(columns = indicator_ids)

    distict_region_campaign_list = DataPoint.objects.raw("\
        SELECT \
             max(id) as id \
             ,region_id \
            ,campaign_id \
        FROM datapoint \
        GROUP BY region_id,campaign_id")


    rc_tuple_list = []
    for rc in distict_region_campaign_list:
        # print r
        r_c_tuple = (rc.region_id,rc.campaign_id)
        rc_tuple_list.append(r_c_tuple)


    rc_df = DataFrame(rc_tuple_list,columns=['region_id','campaign_id'])
    rc_df = rc_df.reset_index(level=[0,1])

    for i,(i_id) in enumerate(indicator_ids):

        rc_df = add_indicator_data_to_rc_df(rc_df, i_id)


    print rc_df[:22]



def add_indicator_data_to_rc_df(rc_df, i_id):

    column_header = ['region_id','campaign_id']
    column_header.append(i_id)

    raw_indicator_df = DataFrame(list(DataPoint.objects\
        .filter(indicator_id = i_id)\
        .values_list('region_id','campaign_id','value')),columns = column_header)
    merged_df = rc_df.merge(raw_indicator_df,how='left')

    return merged_df

    # return rc_df
