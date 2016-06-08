import { createAction } from 'redux-actions'
import RhizomeAPI from 'utilities/api'

export const fetchDatapoints = createAction(
  'FETCH_DATAPOINTS', params => {
    const path = params['group_by_time'] === 'campaign' ? '/campaign_datapoint/' : '/date_datapoint/'
    return RhizomeAPI.get(path, {params: _prepDatapointsQuery(params)})
  }
)

const _prepDatapointsQuery = (params) => {
  // const chartNeedsNullData = _.indexOf(builderDefinitions.need_missing_data_charts, params.type) !== -1
  const chartNeedsNullData = true
  let query = {
    campaign__in: params.campaign__in || params.campaign_id,
    indicator__in: params.indicator_ids.join(),
    location_id__in: params.location_ids.join(),
    location_depth: params.location_depth <= 0 ? null : params.location_depth,
    campaign_start: params.start_date,
    campaign_end: params.end_date,
    chart_type: params.type,
    chart_uuid: params.uuid,
    show_missing_data: chartNeedsNullData ? 1 : params.show_missing_data,
    group_by_time: params.group_by_time,
    source_name: params.source_name,
    filter_indicator: params.indicator_filter ? params.indicator_filter.type : null,
    filter_value: params.indicator_filter ? params.indicator_filter.value : null,
    location_level: params.type === 'TableChart' ? 'District' : null
  }
  console.log('query', query)
  return query
}

export const fetchDatapointsFailure = createAction('FETCH_DATAPOINTS_FAILURE')
export const fetchDatapointsSuccess = createAction('FETCH_DATAPOINTS_SUCCESS')

