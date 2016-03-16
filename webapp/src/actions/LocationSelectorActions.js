import Reflux from 'reflux'

const LocationSelectorActions = Reflux.createActions({
  'selectLocation': 'selectLocation',
  'deselectLocation': 'deselectLocation',
  'setSelectedLocations': 'setSelectedLocations',
  'clearSelectedLocations': 'clearSelectedLocations'
})

export default LocationSelectorActions
