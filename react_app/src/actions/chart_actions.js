import { createAction } from 'redux-actions'
import { takeEvery } from 'redux-saga'
import { call, put } from 'redux-saga/effects'
import RhizomeAPI from 'utilities/api'

export const getAllCharts = createAction('GET_ALL_CHARTS')
export const getAllChartsFailure = createAction('GET_ALL_CHARTS_FAILURE')
export const getAllChartsSuccess = createAction('GET_ALL_CHARTS_SUCCESS')

// ===========================================================================//
// 																	 SAGAS														 			  //
// ===========================================================================//
export const watchGetAllCharts = function * () {
  yield * takeEvery('GET_ALL_CHARTS', fetchAllCharts)
}

export const fetchAllCharts = function * (action) {
  try {
    const response = yield call(() => RhizomeAPI.get('custom_chart/'))
    yield put({type: 'GET_ALL_CHARTS_SUCCESS', payload: response.data.objects})
  } catch (error) {
    yield put({type: 'GET_ALL_CHARTS_FAILURE', error})
  }
}

