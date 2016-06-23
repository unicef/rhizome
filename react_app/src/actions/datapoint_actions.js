import _ from 'lodash'
import { createAction } from 'redux-actions'
import { takeEvery } from 'redux-saga'
import { call, put } from 'redux-saga/effects'
import RhizomeAPI from 'utilities/api'

export const getDatapoints = createAction('GET_DATAPOINTS')
export const getDatapointsFailure = createAction('GET_DATAPOINTS_FAILURE')
export const getDatapointsSuccess = createAction('GET_DATAPOINTS_SUCCESS')
export const updateDatapoint = createAction('UPDATE_DATAPOINT')
export const updateDatapointFailure = createAction('UPDATE_DATAPOINT_FAILURE')
export const updateDatapointSuccess = createAction('UPDATE_DATAPOINT_SUCCESS')
export const removeDatapoint = createAction('REMOVE_DATAPOINT')
export const removeDatapointFailure = createAction('REMOVE_DATAPOINT_FAILURE')
export const removeDatapointSuccess = createAction('REMOVE_DATAPOINT_SUCCESS')

// ===========================================================================//
//                                   SAGAS                                    //
// ===========================================================================//

export const watchGetDatapoints = function * () {
  yield * takeEvery('GET_DATAPOINTS', fetchDatapoints)
}

export const watchRemoveDatapoint = function * () {
  yield * takeEvery('REMOVE_DATAPOINT', deleteDatapoint)
}

export const watchUpdateDatapoint = function * () {
  yield * takeEvery('UPDATE_DATAPOINT', saveDatapoint)
}

export const fetchDatapoints = function * (action) {
  yield put({type: 'CLEAR_DATAPOINTS'})
  const query = _prepDatapointsQuery(action.payload)
  if (!query) return
  try {
    const campaignDatapoint = action.payload['data_type'] === 'campaign'
    const path = campaignDatapoint ? '/campaign_datapoint/' : '/date_datapoint/'
    const response = yield call(() => RhizomeAPI.get(path, {params: query}))
    yield put({type: 'GET_DATAPOINTS_SUCCESS', payload: response})
  } catch (error) {
    yield put({type: 'GET_DATAPOINTS_FAILURE', error})
  }
}

export const saveDatapoint = function * (action) {
  const datapoint = {
    value: action.payload.value,
    indicator_id: action.payload.indicator.id,
    location_id: action.payload.location.id,
    campaign_id: action.payload.campaign.id
  }
  try {
    let path = datapoint.campaign_id ? '/campaign_datapoint/' : '/date_datapoint/'
    let response
    if (!action.payload.id) {
      response = yield call(() => RhizomeAPI.post(path, datapoint))
    } else {
      path += action.payload.id
      response = yield call(() => RhizomeAPI.patch(path, {value: datapoint.value}))
    }
    if (response.status !== 500) {
      yield put({type: 'UPDATE_DATAPOINT_SUCCESS', payload: response})
    } else {
      throw response
    }
  } catch (error) {
    yield put({type: 'UPDATE_DATAPOINT_FAILURE', error})
  }
}

export const deleteDatapoint = function * (action) {
  console.log(action)
  try {
    const path = action.payload.campaign.id ? '/campaign_datapoint/' : '/date_datapoint/'
    const response = yield call(() => RhizomeAPI.delete(path + action.payload.id))
    if (response.status !== 500) {
      yield put({type: 'REMOVE_DATAPOINT_SUCCESS', payload: response})
    } else {
      throw response
    }
  } catch (error) {
    yield put({type: 'REMOVE_DATAPOINT_FAILURE', error})
  }
}

// ===========================================================================//
//                                  UTILITIES                                 //
// ===========================================================================//
const _prepDatapointsQuery = (params) => {
  let query = {
    indicator__in: params.selected_indicators.map(indicator => indicator.id).join(),
    chart_type: params.type,
    chart_uuid: params.uuid,
    source_name: params.source_name,
    location_level: params.type === 'TableChart' ? 'District' : null
    // location_depth: params.location_depth <= 0 ? null : params.location_depth,
  }
  let queryReady = !_.isEmpty(params.selected_locations) && !_.isEmpty(params.selected_indicators)
  if (!queryReady) {
    return false
  }
  if (params.indicator_filter && parseInt(params.indicator_filter.value) !== 0) {
    query.filter_indicator = params.indicator_filter.type
    query.filter_value = params.indicator_filter.value
  }
  if (params.data_type === 'campaign') {
    query.location_id = params.selected_locations[0].id
    query.campaign__in = params.selected_campaign.id
    queryReady = queryReady && query.campaign__in
  } else {
    query.location_id__in = params.selected_locations.map(location => location.id).join()
    query.start_date = params.start_date
    query.end_date = params.end_date
  }
  if (!queryReady) {
    return false
  }
  return query
}

