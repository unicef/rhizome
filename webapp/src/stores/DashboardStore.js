'use strict'

import _ from 'lodash'
import Reflux from 'reflux'
import moment from 'moment'

import RegionStore from 'stores/RegionStore'
import CampaignStore from 'stores/CampaignStore'

var DashboardStore = Reflux.createStore({
  listenables: [require('actions/DashboardActions')],

  init: function () {
    this.loaded = true
    this.indicators = {}
  },

  onInitialize () {
    return Promise.all([
      RegionStore.getlocationsPromise(),
      RegionStore.getLocationTypesPromise(),
      CampaignStore.getCampaignsPromise()
    ])
    .then(([locations, locationsTypes, campaigns]) => {
      this.locations = locations
      this.campaigns = campaigns

      var locationIdx = _.indexBy(locations, 'id')
      var types = _.indexBy(locationsTypes, 'id')

      this.locations.forEach(location => {
        location.location_type = _.get(types[location.location_type_id], 'name')
        location.parent = locationIdx[location.parent_location_id]
      })

      this.loaded = true

      this.trigger({
        loaded: this.loaded,
        locations: this.locations,
        campaigns: this.campaigns
      })
    })
  },

  getQueries: function () {
    var indicators = this.indicators
    var qs = _.groupBy(indicators, function (definition, key) {
      return [
        definition.duration,
        definition.startOf,
        definition.locations
      ].join('-')
    })
    return _.map(qs, function (arr) {
      return _.merge.apply(null, arr.concat(function (a, b) {
        if (_.isArray(a)) {
          return a.concat(b)
        }
      }))
    })
  },

  setDashboardInternal: function (dashboard) {
    this.indicators = {}
    dashboard.charts.forEach(this.addChartDefinition)

    var locations = this.locations
    var campaigns = this.campaigns

    var locationIdx = _.indexBy(locations, 'id')
    var topLevellocations = _(locations)
      .filter(function (r) {
        return !locationIdx.hasOwnProperty(r.parent_location_id)
      })
      .sortBy('name')

    var location = _.find(locations, location => {
      return location.name === this.location
    })

    if (!location) {
      location = topLevellocations.first()
    }

    var campaign = _(campaigns)
      .filter(function (c) {
        return c.office_id === location.office_id  &&
          (!this.date || _.startsWith(c.start_date, this.date))
      }.bind(this))
      .sortBy('start_date')
      .last()

    if (dashboard) {
      var hasMap = _(dashboard.charts)
        .pluck('type')
        .any(t => _.endsWith(t, 'Map'))
    }

    this.trigger({
      dashboard: dashboard,
      location: location,
      campaign: campaign,
      loaded: true,

      locations: locations,
      campaigns: _.filter(campaigns, function (c) {
        return c.office_id === location.office_id
      }),
      allCampaigns: campaigns,
      hasMap: hasMap
    })
  },

  // action handlers
  onSetDashboard: function (definition) {
    var dashboard = this.dashboard = definition.dashboard
    this.location = definition.location || this.location
    this.date = definition.date || this.date

    if (this.campaigns || this.locations) {
      this.setDashboardInternal(dashboard)
    } else {
      this.onInitialize().then(() => {
        this.setDashboardInternal(dashboard)
      })
    }
  },

  // helpers
  addChartDefinition: function (chart) {
    var base = _.omit(chart, 'indicators', 'title')

    chart.indicators.forEach(id => {
      var duration = !_.isNull(_.get(chart, 'timeRange', null)) ? moment.duration(chart.timeRange) : Infinity
      var hash = [id, chart.startOf, chart.locations].join('-')

      if (!this.indicators.hasOwnProperty(hash) || duration > this.indicators[hash].duration) {
        this.indicators[hash] = _.defaults({
          duration: duration,
          indicators: [id]
        }, base)
      }
    })
  }
})

export default DashboardStore
