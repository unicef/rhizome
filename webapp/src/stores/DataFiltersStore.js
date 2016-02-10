import _ from 'lodash'
import Reflux from 'reflux'
import moment from 'moment'
import api from 'data/api'

import ancestryString from 'data/transform/ancestryString'
import treeify from 'data/transform/treeify'

var DataFiltersStore = Reflux.createStore({

  listenables: [require('actions/DataFiltersActions')],

  data: {
    data: null,
    locations: [],
    locationMap: [],
    selected_locations: [],
    indicators: [],
    selected_indicators: [],
    couldLoad: false,
    hasData: false,
    campaign: {
      start: new Date(),
      end: new Date()
    }
  },

  getInitialState: function () {
    return this.data
  },

  _setCouldLoad: function () {
    this.data.couldLoad = this.data.selected_indicators.length > 0 && this.data.selected_locations.length > 0
  },

  _fetchData: function (options) {
    api.datapoints(options, null, {'cache-control': 'no-cache'})
      .then(response => {
        if (!response.objects || response.objects.length < 1) {
          this.data.data = null
        } else {
          this.data.data = response
        }
        this.trigger(this.data)
      })
  },

  onGetData: function (campaign, locations, indicators) {
    this.data.data = null
    this.trigger(this.data)

    if (!this.data.couldLoad) return

    let options = {indicator__in: []}

    if (locations.length > 0) options.location_id__in = _.map(locations, 'id')
    if (campaign.start) options.campaign_start = moment(campaign.start).format('YYYY-M-D')
    if (campaign.end) options.campaign_end = moment(campaign.end).format('YYYY-M-D')

    indicators.forEach(indicator => {
      options.indicator__in.push(indicator.id)
    })

    this._fetchData(options)
  },

// =========================================================================== //
//                                  LOCATIONS                                  //
// =========================================================================== //

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

  onAddLocation: function (id) {
    this.data.selected_locations.push(this.data.locationMap[id])
    this._setCouldLoad()
    this.trigger(this.data)
  },

  onRemoveLocation: function (id) {
    _.remove(this.data.selected_locations, {id: id})
    this._setCouldLoad()
    this.trigger(this.data)
  },

// =========================================================================== //
//                                 INDICATORS                                  //
// =========================================================================== //

  onGetIndicators: function () {
    api.indicatorsTree()
      .then(response => {
        this.data.indicators = response.objects
        this.data.indicatorMap = _.indexBy(response.flat, 'id')

        this.trigger(this.data)
      })
  },

  onAddIndicator: function (id) {
    this.data.selected_indicators.push(this.data.indicatorMap[id])
    this._setCouldLoad()
    this.trigger(this.data)
  },

  onRemoveIndicator: function (id) {
    _.remove(this.data.selected_indicators, {id: id})
    this._setCouldLoad()
    this.trigger(this.data)
  },

// =========================================================================== //
//                                 DATE RANGE                                  //
// =========================================================================== //

  onUpdateDateRangePicker: function (key, value) {
    this.data.campaign[key] = value
    this.trigger(this.data)
  }
})

export default DataFiltersStore
