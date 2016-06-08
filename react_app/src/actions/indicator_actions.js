import { createAction } from 'redux-actions'
import RhizomeAPI from 'utilities/api'

export const fetchIndicators = createAction(
	'FETCH_INDICATORS', () => RhizomeAPI.get('indicator/')
)
export const fetchIndicatorsFailure = createAction('FETCH_INDICATORS_FAILURE')
export const fetchIndicatorsSuccess = createAction('FETCH_INDICATORS_SUCCESS')

