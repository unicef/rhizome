import _ from 'lodash'
import { handleActions } from 'redux-actions'

const users = handleActions({
  FETCH_USERS_REQUEST: (state, action) => _.keyBy(action.payload.data.objects, 'id'),
  FETCH_ALL_META_REQUEST: (state, action) => _.keyBy(action.payload.data.objects[0].users, 'id')
}, {})

export default users
