import { createAction } from 'redux-actions'
import { takeLatest } from 'redux-saga'
import { call, put } from 'redux-saga/effects'
import RhizomeAPI from 'utilities/api'

export const getAllIndicators = createAction('GET_ALL_INDICATORS')
export const getAllIndicatorsFailure = createAction('GET_ALL_INDICATORS_FAILURE')
export const getAllIndicatorsSuccess = createAction('GET_ALL_INDICATORS_SUCCESS')

export const getAllIndicatorTags = createAction('GET_ALL_INDICATOR_TAGS')
export const getAllIndicatorTagsSuccess = createAction('GET_ALL_INDICATOR_TAGS_SUCCESS')

export const getAllIndicatorsToTags = createAction('GET_ALL_INDICATORS_TO_TAGS')
export const getAllIndicatorsToTagsSuccess = createAction('GET_ALL_INDICATORS_TO_TAGS_SUCCESS')

// ===========================================================================//
// 																	 SAGAS														 			  //
// ===========================================================================//
export const watchGetAllIndicators = function * () {
  yield * takeLatest('GET_ALL_INDICATORS', fetchAllIndicators)
}

export const fetchAllIndicators = function * (action) {
  try {
    const [indicators, indicator_tags, indicators_to_tags] = yield [
      call(() => RhizomeAPI.get('indicator/')),
      call(() => RhizomeAPI.get('indicator_tag/')),
      call(() => RhizomeAPI.get('indicator_to_tag/'))
    ]
    const result = {
      indicators: indicators.data.objects,
      indicator_tags: indicator_tags.data.objects,
      indicators_to_tags: indicators_to_tags.data.objects
    }
    yield put({type: 'GET_ALL_INDICATORS_SUCCESS', payload: result})
  } catch (error) {
    yield put({type: 'GET_ALL_INDICATORS_FAILURE', error})
  }
}

