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
    yield put({type: 'GET_INITIAL_DATA_SUCCESS', payload: response})
    yield put({type: 'GET_ALL_CAMPAIGNS_SUCCESS', payload: response.data.objects[0].campaigns})
  } catch (error) {
    yield put({type: 'GET_INITIAL_DATA_FAILURE', error})
  }
}
