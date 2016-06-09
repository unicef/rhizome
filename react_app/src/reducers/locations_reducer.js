import _ from 'lodash'
import { handleActions } from 'redux-actions'
import ancestryString from 'utilities/transform/ancestryString'
import treeify from 'utilities/transform/treeify'

const initial_state = {raw: null, index: null, list: null}

const locations = handleActions({
  GET_ALL_LOCATIONS_SUCCESS: (state, action) => ({
    raw: action.payload,
    index: _.keyBy(action.payload, 'id'),
    list: createLocationTree(action.payload)
  })
}, initial_state)

const createLocationTree = (raw_locations) => {
  return _(raw_locations).map(location => ({
    'title': location.name,
    'value': location.id,
    'parent': location.parent_location_id
  }))
  .sortBy('title')
  .reverse()
  .thru(_.curryRight(treeify)('value'))
  .map(ancestryString)
  .value()
}

export default locations
