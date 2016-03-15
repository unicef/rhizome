import Reflux from 'reflux'
import api from 'data/api'

const LocationActions = Reflux.createActions({
  'fetchLocations': { children: ['completed', 'failed'], asyncResult: true },
  'selectLocation': 'selectLocation',
  'deselectLocation': 'deselectLocation',
  'clearSelectedLocations': 'clearSelectedLocations'
})

LocationActions.fetchLocations.listenAndPromise(() => {
  return api.locations(null, null, {'cache-control': 'max-age=604800, public'}).then(response => response)
})

export default LocationActions
