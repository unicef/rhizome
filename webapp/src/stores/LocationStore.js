import _ from 'lodash'
import Reflux from 'reflux'
import StateMixin from'reflux-state-mixin'
import LocationActions from 'actions/LocationActions'
import ancestryString from 'data/transform/ancestryString'
import treeify from 'data/transform/treeify'

var LocationStore = Reflux.createStore({

  mixins: [StateMixin.store],

  listenables: LocationActions,

  locations: {
    meta: null,
    raw: null,
    index: null,
    filtered: [],
    list: [],
    selected: [],
    lpd_statuses: [
      {value: 'lpd-1', 'title': 'LPD 1', location_ids: []},
      {value: 'lpd-2', 'title': 'LPD 2', location_ids: []},
      {value: 'lpd-3', 'title': 'LPD 3', location_ids: []}
    ]
  },

  init () {
    LocationActions.fetchLocations()
  },

  getInitialState () {
    return this.locations
  },

  // =========================================================================== //
  //                              API CALL HANDLERS                              //
  // =========================================================================== //

  // ===============================  Fetch Locations  ============================= //
  onFetchLocations () {
    this.setState({ raw: [] })
  },
  onFetchLocationsCompleted (response) {
    this.locations.meta = response.meta
    this.locations.raw = response.objects
    this.locations.index = _.indexBy(this.locations.raw, 'id')
    this.locations.list = this.createLocationTree(this.locations.raw)
    this.locations.filtered = this.locations.list
    this.setLocationLpdStatuses(this.locations.raw)
    this.setState(this.locations)
  },
  onFetchLocationsFailed (error) {
    this.setState({ error: error })
  },

  // =========================================================================== //
  //                            REGULAR ACTION HANDLERS                          //
  // =========================================================================== //
  onSelectLocations (location_ids) {
    if (Array.isArray(location_ids)) {
      this.setState({ selected: location_ids.map(id => this.locations.index[id]) })
    } else {
      this.setState({ selected: [this.locations.index[location_ids]] })
    }
  },
  onSelectLocation (id) {
    this.locations.selected.push(this.locations.index[id])
    this.setState(this.locations)
  },
  onDeselectLocation (id) {
    _.remove(this.locations.selected, {id: id})
    this.setState(this.locations)
  },
  onClearSelectedLocations (id) {
    this.locations.selected = []
    this.setState(this.locations)
  },

  // =========================================================================== //
  //                                   UTILITIES                                 //
  // =========================================================================== //
  createLocationTree (raw_locations) {
    return _(raw_locations).map(location => {
      return {
        'title': location.name,
        'value': location.id,
        'parent': location.parent_location_id
      }
    })
    .sortBy('title')
    .reverse()
    .thru(_.curryRight(treeify)('value'))
    .map(ancestryString)
    .value()
  },

  setLocationLpdStatuses (raw_locations) {
    raw_locations.forEach(location => {
      if (location.lpd_status === 1) {
        this.locations.lpd_statuses[0].location_ids.push(location.id)
      } else if (location.lpd_status === 2) {
        this.locations.lpd_statuses[1].location_ids.push(location.id)
      } else if (location.lpd_status === 3) {
        this.locations.lpd_statuses[2].location_ids.push(location.id)
      }
    })
  }
})

export default LocationStore
