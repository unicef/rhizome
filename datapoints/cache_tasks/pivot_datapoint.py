from pprint import pprint
from pandas import DataFrame
import numpy as np

from django.db import connection as con
from django.conf import settings
from datapoints.models import DataPoint, DataPointAbstracted


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

    r_c_df_to_db(rc_df)

def add_indicator_data_to_rc_df(rc_df, i_id):
    '''
    left join the region / campaign dataframe with the stored data for each
    campaign.
    '''

    column_header = ['region_id','campaign_id']
    column_header.append(i_id)

    raw_indicator_df = DataFrame(list(DataPoint.objects\
        .filter(indicator_id = i_id)\
        .values_list('region_id','campaign_id','value')),columns = column_header)

    merged_df = rc_df.merge(raw_indicator_df,how='left')
    merged_df = merged_df.reset_index(drop=True)

    return merged_df


def r_c_df_to_db(rc_df):

    csv_path = settings.MEDIA_ROOT + '_rc_df.csv'

    rc_df.to_csv(csv_path)

    rc_dict = rc_df.transpose().to_dict()

    for r_no, r_data in rc_dict.iteritems():
        region_id, campaign_id = r_data['region_id'],r_data['campaign_id']

        del r_data['region_id']
        del r_data['campaign_id']
        del r_data['index']

        DataPointAbstracted.objects.create(
            region_id = region_id,\
            campaign_id = campaign_id,\
            indicator_json = r_data
        )
