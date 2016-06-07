import _ from 'lodash'
import { handleActions } from 'redux-actions'
import ancestryString from 'utilities/transform/ancestryString'
import treeify from 'utilities/transform/treeify'

const data = {raw: null, index: null, list: null}

const locations = handleActions({
  FETCH_LOCATIONS_REQUEST: (state, action) => processLocations(action.payload.data.objects),
  FETCH_ALL_META_REQUEST: (state, action) => processLocations(action.payload.data.objects[0].locations)
}, data)

const processLocations = (locations) => {
  data.raw = locations
  data.index = _.keyBy(locations, 'id')
  data.list = createLocationTree(locations)
  return data
}

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
