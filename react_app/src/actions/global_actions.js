import { createAction } from 'redux-actions'
import { takeEvery } from 'redux-saga'
import { call, put } from 'redux-saga/effects'
import RhizomeAPI from 'utilities/api'

export const getInitialData = createAction('GET_INITIAL_DATA')
export const getInitialDataFailure = createAction('GET_INITIAL_DATA_FAILURE')
export const getInitialDataSuccess = createAction('GET_INITIAL_DATA_SUCCESS')
export const selectGlobalCampaign = createAction('SELECT_GLOBAL_CAMPAIGN')
export const selectGlobalLocation = createAction('SELECT_GLOBAL_LOCATION')
export const setGlobalIndicators = createAction('SET_GLOBAL_INDICATORS')
export const setGlobalIndicatorTag = createAction('SET_GLOBAL_INDICATOR_TAG')

// ===========================================================================//
// 																	 SAGAS																	 //
// ===========================================================================//

export const watchGetInitialData = function * () {
  yield* takeEvery('GET_INITIAL_DATA', fetchAllMeta)
}

export const fetchAllMeta = function * (action) {
  try {
    const response = yield call(() => RhizomeAPI.get('all_meta/'))
    const indicators_response = {
      indicators: response.data.objects[0].indicators,
      indicator_tags: response.data.objects[0].indicator_tags,
      indicators_to_tags: response.data.objects[0].indicators_to_tags
    }
    yield [
      put({type: 'GET_INITIAL_DATA_SUCCESS', payload: response}),
      put({type: 'GET_ALL_CAMPAIGNS_SUCCESS', payload: response.data.objects[0].campaigns}),
      put({type: 'GET_ALL_LOCATIONS_SUCCESS', payload: response.data.objects[0].locations}),
      put({type: 'GET_ALL_CHARTS_SUCCESS', payload: response.data.objects[0].charts}),
      put({type: 'GET_ALL_DASHBOARDS_SUCCESS', payload: response.data.objects[0].dashboards}),
      put({type: 'GET_ALL_INDICATORS_SUCCESS', payload: indicators_response})
    ]
  } catch (error) {
    yield put({type: 'GET_INITIAL_DATA_FAILURE', error})
  }
}
