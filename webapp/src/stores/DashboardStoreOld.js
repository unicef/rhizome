import _ from 'lodash'
import Reflux from 'reflux'
import moment from 'moment'
import api from 'data/api'
import StateMixin from'reflux-state-mixin'

import Location from 'data/requests/LocationAPI'
import DashboardActions from 'actions/DashboardActions'

var DashboardStore = Reflux.createStore({

  listenables: [DashboardActions],

  mixins: [StateMixin.store],

  init () {
    this.dashboards = {
      list: null,
      meta: null,
      raw: null,
      index: null
    }
    this.loaded = true
    this.indicators = {}
  },

  onInitialize () {
    return Promise.all([
      Location.getLocations(),
      Location.getLocationTypes(),
      api.campaign(null, null, {'cache-control': 'max-age=86400, public'})
    ])
    .then(([locations, locationsTypes, campaigns]) => {
      this.locations = locations
      this.campaigns = campaigns.objects

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

  getQueries () {
    var indicators = this.indicators
    var qs = _.groupBy(indicators, (definition, key) => {
      return [
        definition.duration,
        definition.startOf,
        definition.locations
      ].join('-')
    })
    return _.map(qs, arr => {
      return _.merge.apply(null, arr.concat((a, b) => {
        if (_.isArray(a)) {
          return a.concat(b)
        }
      }))
    })
  },

  setDashboardInternal (dashboard, campaign_id) {
    this.indicators = {}
    dashboard.charts.forEach(this.addChartDefinition)

    var locations = this.locations
    var campaigns = this.campaigns
    var campaignIx = _.indexBy(campaigns, 'id')

    var location = _.find(locations, location => {
      return location.name === this.location
    })

    if (!location) {
      // get the default configuration from the api //
      location = locations[0]
    }

    // if no campaign param set to the first //
    var campaign = campaignIx[campaign_id]
    if (!campaign) {
      campaign = campaigns[0]
    }

    var hasMap = _(dashboard.charts)
      .pluck('type')
      .any(t => _.endsWith(t, 'Map'))

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
  onSetDashboard (definition) {
    var dashboard = this.dashboard = definition.dashboard
    var campaign_id = definition.campaign

    this.location = definition.location || this.location

    if (this.campaigns || this.locations) {
      this.setDashboardInternal(dashboard, campaign_id)
    } else {
      this.onInitialize().then(() => {
        this.setDashboardInternal(dashboard, campaign_id)
      })
    }
  },

  // helpers
  addChartDefinition (chart) {
    const base = _.omit(chart, 'indicators', 'title')
    chart.indicators.forEach(id => {
      const duration = !_.isNull(_.get(chart, 'timeRange', null)) ? moment.duration(chart.timeRange) : Infinity
      const hash = [id, chart.type, chart.startOf, chart.locations].join('-')
      if (!this.indicators.hasOwnProperty(hash) || duration > this.indicators[hash].duration) {
        this.indicators[hash] = _.defaults({duration: duration, indicators: [id]}, base)
      }
    })
  }
})


export default DashboardStore
