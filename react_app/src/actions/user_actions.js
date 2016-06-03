import { createAction } from 'redux-actions'
import RhizomeAPI from 'util/api'

export const fetchUsers = createAction(
	'FETCH_USERS_REQUEST', () => RhizomeAPI.get('user/')
)
export const fetchUsersFailure = createAction('FETCH_USERS_FAILURE')
export const fetchUsersSuccess = createAction('FETCH_USERS_SUCCESS')

