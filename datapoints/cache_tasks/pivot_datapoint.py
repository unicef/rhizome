import pandas as pd
from pandas import DataFrame, read_sql

from django.db import connection as con
from datapoints.models import *


def full_cache_refresh():

    indicator_raw = DataPoint.objects.raw("""
        SELECT DISTINCT 1 as id, indicator_id from datapoint_with_computed
        ORDER BY indicator_id DESC""")

    all_indicator_ids = [x.indicator_id for x in indicator_raw]

    indicator_df = DataFrame(columns = all_indicator_ids)

    print ' ... QUERYING FOR DISTINCT REGION / CAMPAIGN ... '

    distict_region_campaign_list = DataPoint.objects.raw("""
        SELECT DISTINCT
            1 as id
            , dwc.region_id
            , dwc.campaign_id
        FROM datapoint_with_computed dwc
        INNER JOIN region r
        ON dwc.region_id = r.id
        AND r.office_id = 1
        """)

    rc_tuple_list = []
    for rc in distict_region_campaign_list:
        print 'region_id ... %s' % rc.region_id

        r_c_tuple = (rc.region_id,rc.campaign_id)
        rc_tuple_list.append(r_c_tuple)


    rc_df = DataFrame(rc_tuple_list,columns=['region_id','campaign_id'])
    rc_df = rc_df.reset_index(level=[0,1])

    for i,(i_id) in enumerate(all_indicator_ids):

        print 'indicator_id.. %s' % i_id

        rc_df = add_indicator_data_to_rc_df(rc_df, i_id)

    r_c_df_to_db(rc_df)

def add_indicator_data_to_rc_df(rc_df, i_id):
    '''
    left join the region / campaign dataframe with the stored data for each
    campaign.
    '''
    column_header = ['region_id','campaign_id']
    column_header.append(i_id)

    print 'start query'

    sql = """
        SELECT
    		d.region_id
    		,d.campaign_id
    		,value as "%s"
        FROM datapoint_with_computed d
        INNER JOIN region r
        ON d.region_id = r.id
        AND r.office_id = 1
        WHERE indicator_id  = %s;
        """ % (i_id,i_id)

    indicator_df = read_sql(sql,con,columns=column_header)
    print 'done query'
    con.close()
    merged_df = rc_df.merge(indicator_df,how='left')
    merged_df = merged_df.reset_index(drop=True)

    return merged_df


def r_c_df_to_db(rc_df):

    nan_to_null_df = rc_df.where((pd.notnull(rc_df)), None)

    rc_dict = nan_to_null_df.transpose().to_dict()

    for r_no, r_data in rc_dict.iteritems():

        region_id, campaign_id = r_data['region_id'],r_data['campaign_id']

        del r_data['region_id']
        del r_data['campaign_id']
        del r_data['index']

        # first delete #
        DataPointAbstracted.objects.filter(region_id = region_id\
            ,campaign_id = campaign_id).delete()

        # and then insert #
        DataPointAbstracted.objects.create(
            region_id = region_id,\
            campaign_id = campaign_id,\
            indicator_json = r_data
        )
