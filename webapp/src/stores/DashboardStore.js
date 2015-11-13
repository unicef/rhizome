'use strict'

var _ = require('lodash')
var Reflux = require('reflux')
var moment = require('moment')

var RegionStore = require('stores/RegionStore')
var CampaignStore = require('stores/CampaignStore')

var DashboardStore = Reflux.createStore({
  listenables: [require('actions/DashboardActions')],

  init: function () {
    this.loaded = true
    this.indicators = {}
    Promise.all([
      RegionStore.getlocationsPromise(),
      RegionStore.getLocationTypesPromise(),
      CampaignStore.getCampaignsPromise()
    ])
    .then(_.spread((locations, locationsTypes, campaigns) => {
      this.locations = locations
      this.campaigns = campaigns

      var locationIdx = _.indexBy(locations, 'id')
      var types = _.indexBy(locationsTypes, 'id')

      _.each(this.locations, function (r) {
        r.location_type = _.get(types[r.location_type_id], 'name')
        r.parent = locationIdx[r.parent_location_id]
      })

      this.loaded = true

      this.trigger({
        loaded: this.loaded,
        locations: this.locations,
        campaigns: this.campaigns
      })
    }))
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
    _.each(dashboard.charts, this.addChartDefinition)

    var locations = this.locations
    var campaigns = this.campaigns

    var locationIdx = _.indexBy(locations, 'id')
    var topLevellocations = _(locations)
      .filter(function (r) {
        return !locationIdx.hasOwnProperty(r.parent_location_id)
      })
      .sortBy('name')

    var location = _.find(locations, function (r) {
      return r.name === this.location
    }.bind(this))

    if (!location) {
      location = topLevellocations.first()
    }

    var campaign = _(campaigns)
      .filter(function (c) {
        return c.office_id === location.office_id &&
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

    Promise.all([
      RegionStore.getlocationsPromise(),
      RegionStore.getLocationTypesPromise(),
      CampaignStore.getCampaignsPromise()
    ])
    .then(_.spread((locations, locationsTypes, campaigns) => {
      this.locations = locations
      this.campaigns = campaigns

      var locationIdx = _.indexBy(locations, 'id')
      var types = _.indexBy(locationsTypes, 'id')

      _.each(this.locations, function (r) {
        r.location_type = _.get(types[r.location_type_id], 'name')
        r.parent = locationIdx[r.parent_location_id]
      })

      this.setDashboardInternal(dashboard)
    }))
  },

  // helpers
  addChartDefinition: function (chart) {
    var base = _.omit(chart, 'indicators', 'title')

    _.each(chart.indicators, function (id) {
      var duration = !_.isNull(_.get(chart, 'timeRange', null)) ? moment.duration(chart.timeRange) : Infinity
      var hash = [id, chart.startOf, chart.locations].join('-')

      if (!this.indicators.hasOwnProperty(hash) || duration > this.indicators[hash].duration) {
        this.indicators[hash] = _.defaults({
          duration: duration,
          indicators: [id]
        }, base)
      }
    }.bind(this))
  }
})

module.exports = DashboardStore
