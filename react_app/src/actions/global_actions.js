import { createAction } from 'redux-actions'
import RhizomeAPI from 'utilities/api'

export const fetchAllMeta = createAction('FETCH_ALL_META', () => RhizomeAPI.get('all_meta/'))
export const fetchAllMetaFailure = createAction('FETCH_ALL_META_FAILURE')
export const fetchAllMetaSuccess = createAction('FETCH_ALL_META_SUCCESS')
export const selectGlobalCampaign = createAction('SELECT_GLOBAL_CAMPAIGN')
export const selectGlobalLocation = createAction('SELECT_GLOBAL_LOCATION')
export const setGlobalIndicatorTag = createAction('SET_GLOBAL_INDICATOR_TAG')
export const setGlobalIndicators = createAction('SET_GLOBAL_INDICATORS')

