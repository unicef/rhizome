import { createAction } from 'redux-actions'

export const getInitialData = createAction('GET_INITIAL_DATA')
export const getInitialDataFailure = createAction('GET_INITIAL_DATA_FAILURE')
export const getInitialDataSuccess = createAction('GET_INITIAL_DATA_SUCCESS')
export const selectGlobalCampaign = createAction('SELECT_GLOBAL_CAMPAIGN')
export const selectGlobalLocation = createAction('SELECT_GLOBAL_LOCATION')
export const setGlobalIndicatorTag = createAction('SET_GLOBAL_INDICATOR_TAG')
export const setGlobalIndicators = createAction('SET_GLOBAL_INDICATORS')

