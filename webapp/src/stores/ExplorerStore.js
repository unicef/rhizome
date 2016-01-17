import _ from 'lodash'
import Reflux from 'reflux'
import api from 'data/api'

import ancestryString from 'data/transform/ancestryString'
import treeify from 'data/transform/treeify'

var ExplorerStore = Reflux.createStore({
  listenables: [require('actions/ExplorerActions')],

  data: {
    locations: [],
    locationMap: [],
    locationSelected: [],
    indicators: [],
    indicatorSelected: [],
    couldLoad: false,
    hasData: false,
    campaign: {
      start: '',
      end: ''
    }
  },

  getInitialState: function () {
    return this.data
  },

  onGetLocations: function () {
    api.locations()
      .then(response => {
        this.data.locations = _(response.objects)
          .map(location => {
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

        this.data.locationMap = _.indexBy(response.objects, 'id')
        this.trigger(this.data)
      })
  },

  onGetIndicators: function () {
    api.indicatorsTree()
      .then(response => {
        this.data.indicators = response.objects
        this.data.indicatorMap = _.indexBy(response.flat, 'id')

        this.trigger(this.data)
      })
  },

  _setCouldLoad: function () {
    this.data.couldLoad = this.data.indicatorSelected.length > 0 && this.data.locationSelected.length > 0
  },

  onUpdateDateRangePicker: function (key, value) {
    this.data.campaign[key] = value
    this.trigger(this.data)
  },

  onAddLocations: function (id) {
    this.data.locationSelected.push(this.data.locationMap[id])
    this._setCouldLoad()
    this.trigger(this.data)
  },

  onRemoveLocation: function (id) {
    _.remove(this.data.locationSelected, {id: id})
    this._setCouldLoad()
    this.trigger(this.data)
  },

  onAddIndicators: function (id) {
    this.data.indicatorSelected.push(this.data.indicatorMap[id])
    this._setCouldLoad()
    this.trigger(this.data)
  },

  onRemoveIndicator: function (id) {
    _.remove(this.data.indicatorSelected, {id: id})
    this._setCouldLoad()
    this.trigger(this.data)
  }
})

export default ExplorerStore
