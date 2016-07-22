import { createAction } from 'redux-actions'
import { takeEvery } from 'redux-saga'
import { call, put } from 'redux-saga/effects'
import RhizomeAPI from 'utilities/api'

export const getAllCampaigns = createAction('GET_ALL_CAMPAIGNS')
export const getAllCampaignTypes = createAction('GET_ALL_CAMPAIGN_TYPES')
export const getAllCampaignsFailure = createAction('GET_ALL_CAMPAIGNS_FAILURE')
export const getAllCampaignsSuccess = createAction('GET_ALL_CAMPAIGNS_SUCCESS')

export const updateCampaign = createAction('UPDATE_CAMPAIGN')
export const updateCampaignFailure = createAction('UPDATE_CAMPAIGN_FAILURE')
export const updateCampaignSuccess = createAction('UPDATE_CAMPAIGN_SUCCESS')

// ===========================================================================//
// 																	 SAGAS																	  //
// ===========================================================================//
export const watchGetAllCampaigns = function * () {
  yield * takeEvery('GET_ALL_CAMPAIGNS', fetchAllCampaigns)
}

export const watchUpdateCampaign = function * () {
  yield * takeEvery('UPDATE_CAMPAIGN', patchCampaign)
}

export const watchGetAllCampaignTypes = function * () {
  yield * takeEvery('GET_ALL_CAMPAIGN_TYPES', fetchAllCampaignTypes)
}

export const patchCampaign = function * (action) {
  const campaign = action.payload
  try {
    const response = yield call(() => RhizomeAPI.patch('campaign/' + campaign.id, campaign))
    yield put({type: 'UPDATE_CAMPAIGN_SUCCESS', payload: response.data.objects})
  } catch (error) {
    yield put({type: 'UPDATE_CAMPAIGN_FAILURE', error})
  }
}

export const fetchAllCampaigns = function * (action) {
  try {
    const response = yield call(() => RhizomeAPI.get('campaign/'))
    yield put({type: 'GET_ALL_CAMPAIGNS_SUCCESS', payload: response.data.objects})
  } catch (error) {
    yield put({type: 'GET_ALL_CAMPAIGNS_FAILURE', error})
  }
}

export const fetchAllCampaignTypes = function * (action) {
  try {
    const response = yield call(() => RhizomeAPI.get('campaign_type/'))
    yield put({type: 'GET_ALL_CAMPAIGN_TYPES_SUCCESS', payload: response.data.objects})
  } catch (error) {
    yield put({type: 'GET_ALL_CAMPAIGN_TYPES_FAILURE', error})
  }
}

