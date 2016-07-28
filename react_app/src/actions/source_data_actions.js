import { createAction } from 'redux-actions'
import { takeEvery } from 'redux-saga'
import { call, put } from 'redux-saga/effects'
import RhizomeAPI from 'utilities/api'

export const getAllSourceDocs = createAction('GET_ALL_SOURCE_DOCS')
export const getAllSourceDocsFailure = createAction('GET_ALL_SOURCE_DOCS_FAILURE')
export const getAllSourceDocsSuccess = createAction('GET_ALL_SOURCE_DOCS_SUCCESS')

// ===========================================================================//
// 																	 SAGAS														 			  //
// ===========================================================================//
export const watchGetAllSourceDocs = function * () {
  yield * takeEvery('GET_ALL_SOURCE_DOCS', fetchAllSourceDocs)
}

export const fetchAllSourceDocs = function * (action) {
  try {
    const response = yield call(() => RhizomeAPI.get('source_doc/'))
    yield put({type: 'GET_ALL_SOURCE_DOCS_SUCCESS', payload: response.data.objects})
  } catch (error) {
    yield put({type: 'GET_ALL_SOURCE_DOCS_FAILURE', error})
  }
}
