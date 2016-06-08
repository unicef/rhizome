import { createAction } from 'redux-actions'
import RhizomeAPI from 'utilities/api'

export const fetchLocations = createAction(
	'FETCH_LOCATIONS', () => RhizomeAPI.get('location/')
)
export const fetchLocationsFailure = createAction('FETCH_LOCATIONS_FAILURE')
export const fetchLocationsSuccess = createAction('FETCH_LOCATIONS_SUCCESS')

