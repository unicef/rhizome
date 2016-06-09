import { createAction } from 'redux-actions'
import { takeEvery } from 'redux-saga'
import { call, put } from 'redux-saga/effects'
import RhizomeAPI from 'utilities/api'

export const getAllDashboards = createAction('GET_ALL_DASHBOARDS')
export const getAllDashboardsFailure = createAction('GET_ALL_DASHBOARDS_FAILURE')
export const getAllDashboardsSuccess = createAction('GET_ALL_DASHBOARDS_SUCCESS')

// ===========================================================================//
// 																	 SAGAS																	  //
// ===========================================================================//
export const watchGetAllDashboards = function * () {
  yield * takeEvery('GET_ALL_DASHBOARDS', fetchAllDashboards)
}

export const fetchAllDashboards = function * (action) {
  try {
    const response = yield call(() => RhizomeAPI.get('custom_dashboard/'))
    yield put({type: 'GET_ALL_DASHBOARDS_SUCCESS', payload: response.data.objects})
  } catch (error) {
    yield put({type: 'GET_ALL_DASHBOARDS_FAILURE', error})
  }
}
