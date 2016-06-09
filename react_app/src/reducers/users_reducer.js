import _ from 'lodash'
import { handleActions } from 'redux-actions'

const initial_state = {raw: null, index: null}

const users = handleActions({
  GET_ALL_USERS_SUCCESS: (state, action) => ({
    raw: action.payload,
    index: _.keyBy(action.payload, 'id')
  })
}, initial_state)

export default users
