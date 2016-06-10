import { createAction } from 'redux-actions'
import { takeEvery } from 'redux-saga'
import { call, put } from 'redux-saga/effects'
import RhizomeAPI from 'utilities/api'

export const getDatapoints = createAction('GET_DATAPOINTS')
export const getDatapointsFailure = createAction('GET_DATAPOINTS_FAILURE')
export const getDatapointsSuccess = createAction('GET_DATAPOINTS_SUCCESS')

// // ===========================================================================//
// //                                   SAGAS                                    //
// // ===========================================================================//
export const watchGetDatapoints = function * () {
  yield * takeEvery('GET_DATAPOINTS', fetchDatapoints)
}

export const fetchDatapoints = function * (action) {
  const query = _prepDatapointsQuery(action.payload)
  if (!query) return
  try {
    const groupByCampaign = action.payload['time_grouping'] === 'campaign'
    const path = groupByCampaign ? '/campaign_datapoint/' : '/date_datapoint/'
    const response = yield call(() => RhizomeAPI.get(path, {params: query}))
    yield put({type: 'GET_DATAPOINTS_SUCCESS', payload: response})
  } catch (error) {
    yield put({type: 'GET_DATAPOINTS_FAILURE', error})
  }
}

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
    time_grouping: params.group_by_time || 'campaign',
    source_name: params.source_name,
    filter_indicator: params.indicator_filter ? params.indicator_filter.type : null,
    filter_value: params.indicator_filter ? params.indicator_filter.value : null,
    location_level: params.type === 'TableChart' ? 'District' : null
  }
  const queryReady = query.campaign__in && query.location_id__in !== '' && query.indicator__in !== ''
  if (!queryReady) {
    return false
  }
  return query
}

