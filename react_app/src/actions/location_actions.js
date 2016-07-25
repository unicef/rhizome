import { createAction } from 'redux-actions'
import { takeEvery } from 'redux-saga'
import { call, put } from 'redux-saga/effects'
import RhizomeAPI from 'utilities/api'

export const getAllLocations = createAction('GET_ALL_LOCATIONS')
export const getAllLocationsFailure = createAction('GET_ALL_LOCATIONS_FAILURE')
export const getAllLocationsSuccess = createAction('GET_ALL_LOCATIONS_SUCCESS')

export const getAllLocationTypes = createAction('GET_ALL_LOCATION_TYPES')
export const getAllLocationTypesFailure = createAction('GET_ALL_LOCATIONS_FAILURE')
export const getAllLocationTypesSuccess = createAction('GET_ALL_LOCATIONS_SUCCESS')

export const updateLocation = createAction('UPDATE_LOCATION')
export const updateLocationFailure = createAction('UPDATE_LOCATION_FAILURE')
export const updateLocationSuccess = createAction('UPDATE_LOCATION_SUCCESS')

// ===========================================================================//
// 																	 SAGAS														 			  //
// ===========================================================================//
export const watchGetAllLocations = function * () {
  yield * takeEvery('GET_ALL_LOCATIONS', fetchAllLocations)
}

export const watchGetAllLocationTypes = function * () {
  yield * takeEvery('GET_ALL_LOCATION_TYPES', fetchAllLocationTypes)
}

export const watchUpdateLocation = function * () {
  yield * takeEvery('UPDATE_LOCATION', patchLocation)
}

export const patchLocation = function * (action) {
  const location = action.payload
  try {
    const response = yield call(() => RhizomeAPI.patch('location/' + location.id, location))
    yield put({type: 'UPDATE_LOCATION_SUCCESS', payload: response.data.objects})
  } catch (error) {
    yield put({type: 'UPDATE_LOCATION_FAILURE', error})
  }
}

export const fetchAllLocations = function * (action) {
  try {
    const response = yield call(() => RhizomeAPI.get('location/'))
    yield put({type: 'GET_ALL_LOCATIONS_SUCCESS', payload: response.data.objects})
  } catch (error) {
    yield put({type: 'GET_ALL_LOCATIONS_FAILURE', error})
  }
}

export const fetchAllLocationTypes = function * (action) {
  try {
    const response = yield call(() => RhizomeAPI.get('location_type/'))
    yield put({type: 'GET_ALL_LOCATION_TYPES_SUCCESS', payload: response.data.objects})
  } catch (error) {
    yield put({type: 'GET_ALL_LOCATION_TYPES_FAILURE', error})
  }
}
