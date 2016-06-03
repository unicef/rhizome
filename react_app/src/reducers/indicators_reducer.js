import _ from 'lodash'
import { handleActions } from 'redux-actions'

const indicators = handleActions({
  FETCH_INDICATORS_REQUEST: (state, action) => _.keyBy(action.payload.data.objects, 'id'),
  FETCH_ALL_META_REQUEST: (state, action) => _.keyBy(action.payload.data.objects[0].indicators, 'id')
}, {})

export default indicators
