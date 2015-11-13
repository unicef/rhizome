'use strict'

import _ from 'lodash'
import Reflux from 'reflux'
import moment from 'moment'

import api from 'data/api'

import DataActions from 'actions/DataActions'

function melt (d) {
  var base = _.omit(d, 'indicators')

  return d.indicators.map(i => {
    return _.assign({
      indicator: i.indicator,
      value: i.value
    }, base)
  })
}

var DataStore = Reflux.createStore({
  listenables: [DataActions],

  init: function () {
    this.loading = false
    this.data = []
  },

  getInitialState: function () {
    return {
      loading: this.loading,
      data: this.data
    }
  },

  onClear: function () {
    this.loading = false
    this.data = []

    this.trigger({
      loading: false,
      data: []
    })
  },

  onFetch: function (campaign, location, charts) {
    var m = moment(campaign.start_date, 'YYYY-MM-DD')
    var end = campaign.end_date

    var promises = _.map(charts, function (def) {
      var q = {
        indicator__in: def.indicators,
        campaign_end: end
      }

      // If no timeRange or startOf property is provided, the chart should fetch
      // data for all time.
      if (!_.isNull(_.get(def, 'timeRange', null)) || def.hasOwnProperty('startOf')) {
        q.campaign_start = m.clone()
          .startOf(def.startOf)
          .subtract(def.timeRange)
          .format('YYYY-MM-DD')
      }

      switch (def.locations) {
        case 'sublocations':
          q.parent_location__in = location.id
          break

        case 'type':
          var parent = _.get(location, 'parent.id')
          if (!_.isUndefined(parent)) {
            q.parent_location__in = parent
          }

          q.location_type = location.location_type
          break
        default:
          q.location__in = location.id
          break
      }

      if (def.level) {
        q.level = def.level
      }

      return api.datapoints(q)
    })

    Promise.all(promises).then(function (responses) {
      this.data = _(responses)
        .pluck('objects')
        .flatten()
        .sortBy(_.method('campaign.start_date.getTime'))
        .map(melt)
        .flatten()
        .value()

      this.loading = false

      this.trigger({
        loading: false,
        data: this.data
      })
    }.bind(this))

    this.loading = true
    this.data = []

    this.trigger({
      loading: true,
      data: []
    })
  },

  onFetchForChart: function (campaign, location, campaigns, locations, dashboard) {
    var promises = _.map(dashboard.charts, function (def) {
      if (def.campaignValue) {
        var chartCampaign = _.indexBy(campaigns, 'id')[def.campaignValue]
        if (chartCampaign) campaign = chartCampaign
      }

      if (def.locationValue) {
        var chartLocation = _.indexBy(locations, 'id')[def.locationValue]
        if (chartLocation) location = chartLocation
      }

      var m = moment(campaign.start_date, 'YYYY-MM-DD')
      var end = campaign.end_date

      var q = {
        indicator__in: def.indicators,
        campaign_end: end
      }

      // If no timeRange or startOf property is provided, the chart should fetch
      // data for all time.
      if (!_.isNull(_.get(def, 'timeRange', null)) || def.hasOwnProperty('startOf')) {
        q.campaign_start = m.clone()
          .startOf(def.startOf)
          .subtract(def.timeRange)
          .format('YYYY-MM-DD')
      }

      switch (def.locations) {
        case 'sublocations':
          q.parent_location__in = location.id
          break

        case 'type':
          var parent = _.get(location, 'parent.id')
          if (!_.isUndefined(parent)) {
            q.parent_location__in = parent
          }

          q.location_type = location.location_type
          break
        default:
          q.location__in = location.id
          break
      }

      if (def.level) {
        q.level = def.level
      }

      return api.datapoints(q)
    })

    Promise.all(promises).then(function (responses) {
      this.data = _(responses)
        .pluck('objects')
        .flatten()
        .sortBy(_.method('campaign.start_date.getTime'))
        .map(melt)
        .flatten()
        .value()

      this.loading = false

      this.trigger({
        loading: false,
        data: this.data
      })
    }.bind(this))

    this.loading = true
    this.data = []

    this.trigger({
      loading: true,
      data: []
    })
  }
})

export default DataStore
