import { takeEvery, delay } from 'redux-saga'
import { call, put } from 'redux-saga/effects'

import RhizomeAPI from 'utilities/api'

export const rootSaga = function * () {
  yield [
    watchGetInitialData()
  ]
}

export const watchGetInitialData = function * () {
  yield* takeEvery('GET_INITIAL_DATA', fetchAllMeta)
}

export const fetchAllMeta = function * (action) {
  try {
    const response = yield call(() => RhizomeAPI.get('all_meta/'))
    yield put({type: 'GET_INITIAL_DATA_SUCCESS', payload: response})
  } catch (error) {
    yield put({type: 'GET_INITIAL_DATA_FAILURE', error})
  }
}
