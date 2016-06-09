import { createAction } from 'redux-actions'
import { takeEvery } from 'redux-saga'
import { call, put } from 'redux-saga/effects'
import RhizomeAPI from 'utilities/api'

export const getAllUsers = createAction('GET_ALL_USERS')
export const getAllUsersFailure = createAction('GET_ALL_USERS_FAILURE')
export const getAllUsersSuccess = createAction('GET_ALL_USERS_SUCCESS')

// ===========================================================================//
// 																	 SAGAS														 			  //
// ===========================================================================//
export const watchGetAllUsers = function * () {
  yield * takeEvery('GET_ALL_USERS', fetchAllUsers)
}

export const fetchAllUsers = function * (action) {
  try {
    const response = yield call(() => RhizomeAPI.get('user/'))
    yield put({type: 'GET_ALL_USERS_SUCCESS', payload: response.data.objects})
  } catch (error) {
    yield put({type: 'GET_ALL_USERS_FAILURE', error})
  }
}
