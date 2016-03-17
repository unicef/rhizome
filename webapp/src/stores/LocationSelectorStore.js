import _ from 'lodash'
import Reflux from 'reflux'
import StateMixin from'reflux-state-mixin'
import LocationSelectorActions from 'actions/LocationSelectorActions'
import LocationStore from 'stores/LocationStore'

const LocationSelectorStore = Reflux.createStore({

  mixins: [StateMixin.store],

  listenables: LocationSelectorActions,

  locations: [],

  selected_locations: [],

  getInitialState () {
    return this.selected_locations
  },

  init () {
    this.listenTo(LocationStore, this.onLocationStore)
  },

  onLocationStore (store) {
    this.locations = store
  },

  onSelectLocation (id) {
    this.selected_locations.push(this.locations.index[id])
    this.trigger(this.selected_locations)
  },

  onDeselectLocation (id) {
    _.remove(this.selected_locations, {id: id})
    this.trigger(this.selected_locations)
  },

  onSetSelectedLocations (ids) {
    if (Array.isArray(ids)) {
      this.selected_locations = ids.map(id => this.locations.index[id])
    } else {
      this.selected_locations = [this.locations.index[ids]]
    }
    this.trigger(this.selected_locations)
  },

  onClearSelectedLocations (id) {
    this.selected_locations = []
    this.trigger(this.selected_locations)
  }
})

export default LocationSelectorStore
