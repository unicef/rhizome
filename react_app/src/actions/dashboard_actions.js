import { createAction } from 'redux-actions'
import RhizomeAPI from 'utilities/api'

export const fetchDashboards = createAction(
	'FETCH_DASHBOARDS_REQUEST', () => RhizomeAPI.get('custom_dashboard/')
)
export const fetchDashboardsFailure = createAction('FETCH_DASHBOARDS_FAILURE')
export const fetchDashboardsSuccess = createAction('FETCH_DASHBOARDS_SUCCESS')

