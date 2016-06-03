import { createAction } from 'redux-actions'
import RhizomeAPI from 'util/api'

export const fetchLocations = createAction(
	'FETCH_LOCATIONS_REQUEST', () => RhizomeAPI.get('location/')
)
export const fetchLocationsFailure = createAction('FETCH_LOCATIONS_FAILURE')
export const fetchLocationsSuccess = createAction('FETCH_LOCATIONS_SUCCESS')

