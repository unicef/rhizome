import _ from 'lodash'
import { handleActions } from 'redux-actions'

const users = handleActions({
  FETCH_USERS: (state, action) => _.keyBy(action.payload.data.objects, 'id'),
  FETCH_ALL_META: (state, action) => _.keyBy(action.payload.data.objects[0].users, 'id')
}, {})

export default users
