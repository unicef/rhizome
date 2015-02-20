import pandas as pd
from pandas import DataFrame, read_sql

from datapoints.models import *


def full_cache_refresh():

    indicator_raw = DataPoint.objects.raw("""
        SELECT DISTINCT 1 as id, indicator_id from datapoint_with_computed
        ORDER BY indicator_id DESC""")

    # all_indicator_ids = [x.indicator_id for x in indicator_raw]
    all_indicator_ids = [414,274]

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
        INNER JOIN region_type rt
        ON r.region_type_id = rt.id
        AND lower(rt.name) in ('country','province')
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

    curs = DataPoint.objects.raw("""
        SELECT
    		d.region_id
    		,d.campaign_id
    		,value
        FROM datapoint_with_computed d
        WHERE indicator_id  = %s;

        SELECT ID FROM datapoint LIMIT 1;""",[i_id])

    indicator_data = []

    for row in curs:
        row_dict = {}
        row_dict['campaign_id'] = row.campaign_id
        row_dict['indicator_id'] = row.indicator_id
        row_dict['region_id'] = row.region_id
        indicator_data.append(row_dict)

    indicator_df = DataFrame(indicator_data,columns=column_header)
    print 'done query'

    merged_df = rc_df.merge(indicator_df,how='left')
    merged_df = merged_df.reset_index(drop=True)

    return merged_df


def r_c_df_to_db(rc_df):

    nan_to_null_df = rc_df.where((pd.notnull(rc_df)), None)

    indexed_df = nan_to_null_df.reset_index(drop=True)
    # rc_df = rc_df.reset_index(level=[0,1])

    rc_dict = indexed_df.transpose().to_dict()


    batch = []

    print nan_to_null_df

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
