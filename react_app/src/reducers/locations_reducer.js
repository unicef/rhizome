import _ from 'lodash'
import { handleActions } from 'redux-actions'

const locations = handleActions({
  FETCH_LOCATIONS_REQUEST: (state, action) => _.keyBy(action.payload.data.objects, 'id'),
  FETCH_ALL_META_REQUEST: (state, action) => _.keyBy(action.payload.data.objects[0].locations, 'id')
}, {})

export default locations
