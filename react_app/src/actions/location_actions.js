import { createAction } from 'redux-actions'
import { takeEvery } from 'redux-saga'
import { call, put } from 'redux-saga/effects'
import RhizomeAPI from 'utilities/api'

export const getAllLocations = createAction('GET_ALL_LOCATIONS')
export const getAllLocationsFailure = createAction('GET_ALL_LOCATIONS_FAILURE')
export const getAllLocationsSuccess = createAction('GET_ALL_LOCATIONS_SUCCESS')

// ===========================================================================//
// 																	 SAGAS														 			  //
// ===========================================================================//
export const watchGetAllLocations = function * () {
  yield * takeEvery('GET_ALL_LOCATIONS', fetchAllLocations)
}

export const fetchAllLocations = function * (action) {
  try {
    const response = yield call(() => RhizomeAPI.get('location/'))
    yield put({type: 'GET_ALL_LOCATIONS_SUCCESS', payload: response.data.objects})
  } catch (error) {
    yield put({type: 'GET_ALL_LOCATIONS_FAILURE', error})
  }
}
