import Reflux from 'reflux'
import LocationAPI from 'data/requests/LocationAPI'

const LocationActions = Reflux.createActions({
  'fetchLocations': { children: ['completed', 'failed'], asyncResult: true }
})

LocationActions.fetchLocations.listenAndPromise(() => {
  return LocationAPI.getLocations()
})

export default LocationActions
