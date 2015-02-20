import pandas as pd
from pandas import DataFrame, read_sql
from pandas.tools.pivot import pivot_table

from datapoints.models import *


def full_cache_refresh():

    indicator_raw = DataPoint.objects.raw("""
        SELECT DISTINCT 1 as id, indicator_id from datapoint_with_computed
        ORDER BY indicator_id DESC""")

    # all_indicator_ids = [x.indicator_id for x in indicator_raw]
    all_indicator_ids = [348,274,5]

    indicator_df = DataFrame(columns = all_indicator_ids)


    print ' ... QUERYING FOR DISTINCT REGION / CAMPAIGN ... '

    distict_region_campaign_list = DataPoint.objects.raw("""
        SELECT DISTINCT
            1 as id
            , dwc.region_id
            , dwc.campaign_id
        FROM datapoint_with_computed dwc
        WHERE 1 = 1
        --WHERE region_id = 12907
        --AND campaign_id = 111
        AND region_id is NOT NULL;
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

        print '...trying...'

        rc_df = add_indicator_data_to_rc_df(rc_df, i_id)

    r_c_df_to_db(rc_df)

def add_indicator_data_to_rc_df(rc_df, i_id):
    '''
    left join the region / campaign dataframe with the stored data for each
    campaign.
    '''
    column_header = ['region_id','campaign_id']
    column_header.append(i_id)

    print 'indicator_id: %s' % i_id

    indicator_df = DataFrame(list(DataPointComputed.objects.filter(
        indicator_id = i_id).values()))

    pivoted_indicator_df = pivot_table(indicator_df, values='value',\
        columns=['indicator_id'],index = ['region_id','campaign_id'])

    cleaned_df = pivoted_indicator_df.reset_index(drop=True)

    print cleaned_df


    # for row in curs:
    #
    #     # print 'campaign_id: %s: ' % row.campaign_id
    #     # print 'indicator_id: %s: ' % row.indicator_id
    #     # print 'region_id: %s: ' % row.region_id
    #     # print 'value: %s: ' % row.value
    #     #
    #     # print '=====\n' * 5
    #
    #     print row.value
    #
    #     row_dict = {}
    #     row_dict['campaign_id'] = row.campaign_id
    #     row_dict['indicator_id'] = row.indicator_id
    #     row_dict['region_id'] = row.region_id
    #     row_dict['value'] = row.value
    #     indicator_data.append(row_dict)
    #
    # print indicator_data
    #
    # indicator_df = DataFrame(indicator_data)#,columns=column_header)
    # indicator_df[i_id] = indicator_df['value']

    # print indicator_df
    #
    # print 'done query'

    merged_df = rc_df.merge(indicator_df,how='left')
    merged_df = merged_df.reset_index(drop=True)

    # print 'merged_df'
    # print merged_df

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
