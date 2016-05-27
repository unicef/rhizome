
## this file is for specific requests for clients ##

def handle_polio_case_table(dp_resource_object, dp_df_columns):
    '''
    This is a very specific peice of code that allows us to generate a table
    with
        - date of latest case
        - infected district count
        - infected province count

    THis relies on certain calcluations to be made in
    caluclated_indicator_component.
    '''
    # http://localhost:8000/api/v1/datapoint/?indicator__in=37,39,82,40&location_id__in=1&campaign_start=2015-04-26&campaign_end=2016-04-26&chart_type=RawData&chart_uuid=1775de44-a727-490d-adfa-b2bc1ed19dad&group_by_time=year&format=json
    calc_indicator_data_for_polio_cases = CalculatedIndicatorComponent.\
        objects.filter(indicator__name = 'Polio Cases').values()

    if len(calc_indicator_data_for_polio_cases) > 0:
        dp_resource_object.ind_meta = {'base_indicator': \
            calc_indicator_data_for_polio_cases[0]['indicator_id']
        }
    else:
        dp_resource_object.ind_meta = {}

    for row in calc_indicator_data_for_polio_cases:
        calc = row['calculation']
        ind_id = row['indicator_component_id']
        dp_resource_object.ind_meta[calc] = ind_id

    parent_location_id = dp_resource_object.parsed_params['location_id__in']

    all_sub_locations = LocationTree.objects.filter(
        parent_location_id = parent_location_id
    ).values_list('location_id', flat=True)

    flat_df = DataFrame(list(DataPoint.objects.filter(
                    location_id__in = all_sub_locations,
                    indicator_id__in = dp_resource_object.parsed_params['indicator__in']
                ).values(*dp_df_columns)),columns=dp_df_columns)

    flat_df = dp_resource_object.get_time_group_series(flat_df)
    flat_df['parent_location_id'] = parent_location_id

    gb_df = DataFrame(flat_df\
        .groupby(['indicator_id','time_grouping','parent_location_id'])\
        ['value']\
        .sum())\
        .reset_index()

    latest_date_df = DataFrame(flat_df\
        .groupby(['indicator_id','time_grouping'])['data_date']\
        .max())\
        .reset_index()
    latest_date_df['value'] = latest_date_df['data_date']\
        .map(lambda x: x.strftime('%Y-%m-%d'))
    latest_date_df['indicator_id'] = dp_resource_object\
        .ind_meta['latest_date']

    district_count_df = DataFrame(flat_df\
        .groupby(['time_grouping']).location_id
        .nunique())\
        .reset_index()
    district_count_df['value'] = district_count_df['location_id']
    district_count_df['indicator_id'] = dp_resource_object\
        .ind_meta['district_count']

    concat_df = concat([gb_df, latest_date_df,  district_count_df])
    concat_df[['indicator_id','value','time_grouping','data_date']]
    concat_df['parent_location_id'] = parent_location_id
    concat_df = concat_df.drop('location_id', 1)
    concat_df = concat_df.rename(columns={'parent_location_id' : 'location_id'})
    return concat_df
