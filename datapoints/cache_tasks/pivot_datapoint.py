from pprint import pprint
import pandas as pd
from pandas import DataFrame, read_sql, concat
import numpy as np

from django.db import connection as con
from django.conf import settings
from datapoints.models import *


def full_cache_refresh():

    indicator_ids = list(set(DataPoint.objects.all()\
        .values_list('indicator_id',flat=True)))

    calc_indicator_ids = list(Indicator.objects.filter(is_reported=\
        False).values_list('id',flat=True))

    all_indicator_ids = indicator_ids + calc_indicator_ids

    indicator_df = DataFrame(columns = all_indicator_ids)

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

    # raw_indicator_df = DataFrame(list(DataPoint.objects\
    #     .filter(indicator_id = i_id)\
    #     .values_list('region_id','campaign_id','value')),columns = column_header)

    sql = """
    SELECT
    	COALESCE(x.region_id, y.region_id) as region_id
    	,COALESCE(x.campaign_id, y.campaign_id) as campaign_id
        ,COALESCE(x.value, y.value) as "%s"
    FROM (
    	SELECT
    		d.region_id
        	,d.campaign_id
        	,d.indicator_id
    		,value
            ,'f' as is_agg
    	FROM datapoint_with_computed d
    	)x

    	FULL JOIN (

    	SELECT
    		r.parent_region_id as region_id
    		,d.campaign_id
    		,d.indicator_id
    		,SUM(d.value) AS value
            ,'t' as is_agg
    	FROM datapoint_with_computed d
    	INNER JOIN  region r
    	ON d.region_id = r.id
    	GROUP BY r.parent_region_id, d.campaign_id, d.indicator_id
    	) y
    	ON x.campaign_id = y.campaign_id
     	AND x.indicator_id = y.indicator_id
	AND x.region_id = y.region_id
    WHERE x.indicator_id = %s
    """ % (i_id,i_id)


    indicator_df = read_sql(sql,con,columns=column_header)

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
