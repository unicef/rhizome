import { createAction } from 'redux-actions'
import { takeEvery } from 'redux-saga'
import { call, put } from 'redux-saga/effects'
import RhizomeAPI from 'utilities/api'

export const getAllCampaigns = createAction('GET_ALL_CAMPAIGNS')
export const getAllCampaignsFailure = createAction('GET_ALL_CAMPAIGNS_FAILURE')
export const getAllCampaignsSuccess = createAction('GET_ALL_CAMPAIGNS_SUCCESS')

// ===========================================================================//
// 																	 SAGAS																	 //
// ===========================================================================//
export const watchGetAllCampaigns = function * () {
  yield * takeEvery('GET_ALL_CAMPAIGNS', fetchAllCampaigns)
}

export const fetchAllCampaigns = function * (action) {
  try {
    const response = yield call(() => RhizomeAPI.get('campaign/'))
    yield put({type: 'GET_ALL_CAMPAIGNS_SUCCESS', payload: response.data.objects})
  } catch (error) {
    yield put({type: 'GET_ALL_CAMPAIGNS_FAILURE', error})
  }
}

