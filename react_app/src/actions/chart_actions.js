import { createAction } from 'redux-actions'
import RhizomeAPI from 'util/api'

export const fetchCharts = createAction(
	'FETCH_CHARTS_REQUEST', () => RhizomeAPI.get('custom_chart/')
)
export const fetchChartsFailure = createAction('FETCH_CHARTS_FAILURE')
export const fetchChartsSuccess = createAction('FETCH_CHARTS_SUCCESS')

