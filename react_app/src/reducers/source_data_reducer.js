import _ from 'lodash'
import { handleActions } from 'redux-actions'

const initial_state = {raw: null, index: null}

export const source_docs = handleActions({
  GET_ALL_SOURCE_DOCS_SUCCESS: (state, action) => ({
    raw: action.payload,
    index: _.keyBy(action.payload, 'id')
  })
}, initial_state)

