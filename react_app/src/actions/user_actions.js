import { createAction } from 'redux-actions'
import RhizomeAPI from 'utilities/api'

export const fetchUsers = createAction(
	'FETCH_USERS', () => RhizomeAPI.get('user/')
)
export const fetchUsersFailure = createAction('FETCH_USERS_FAILURE')
export const fetchUsersSuccess = createAction('FETCH_USERS_SUCCESS')

