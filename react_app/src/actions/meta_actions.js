import { createAction } from 'redux-actions'
import RhizomeAPI from 'util/api'

export const fetchAllMeta = createAction(
	'FETCH_ALL_META_REQUEST', () => RhizomeAPI.get('all_meta/')
)
export const fetchAllMetaFailure = createAction('FETCH_ALL_META_FAILURE')
export const fetchAllMetaSuccess = createAction('FETCH_ALL_META_SUCCESS')

