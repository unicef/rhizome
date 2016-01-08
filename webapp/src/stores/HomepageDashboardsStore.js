import _ from 'lodash'
import Reflux from 'reflux'
import moment from 'moment'

import api from 'data/api'
import DashboardInit from 'data/dashboardInit'

import Indicator from 'requests/Indicator'
import Location from 'requests/Location'
import Office from 'requests/Office'

import CampaignStore from 'stores/CampaignStore'

var HomepageDashboardsStore = Reflux.createStore({
  listenables: [require('actions/HomepageDashboardsActions')],

  onInitialize () {
    this.onFetchDashboards()
  },

  melt: function (d) {
    var base = _.omit(d, 'indicators')

    return d.indicators.map(i => {
      return _.assign({
        indicator: i.indicator,
        value: i.value
      }, base)
    })
  },

  fetchData: function (dashboard) {
    console.log('3: fetching data for dashboard :', dashboard)
    var campaign = dashboard.campaign

    var location = dashboard.location
    var charts = dashboard.charts

    var start = moment(campaign.start_date, 'YYYY-MM-DD')
    var end = campaign.end_date

    var promises = _.map(charts, function (def) {
      var query = {
        indicator__in: def.indicators,
        campaign_end: end
      }

      if (!_.isNull(_.get(def, 'timeRange', null)) || def.hasOwnProperty('startOf')) {
        query.campaign_start = start.clone()
          .startOf(def.startOf)
          .subtract(def.timeRange)
          .format('YYYY-MM-DD')
      }

      switch (def.locations) {
        case 'sublocations':
          query.parent_location_id__in = location.id
          break

        default:
          query.location_id__in = location.id
          break
      }

      if (def.level) {
        query.level = def.level
      }

      return api.datapoints(query)
    })

    return Promise.all(promises)
  },

  prepareQuery: function (locations, campaigns, dashboard) {
    var locationIdx = _.indexBy(locations, 'id')

    _.each(this.locations, function (r) {
      r.parent = locationIdx[r.parent_location_id]
    })

    var indicators = _.reduce(dashboard.charts, this.generateIndicator, {})
    var query = this.getQueriesByIndicators(indicators)

    var topLevelLocations = _(locations)
      .filter(function (r) {
        return !locationIdx.hasOwnProperty(r.parent_location_id)
      })
      .sortBy('name')

    var location = _.find(locations, function (r) {
      return r.name === dashboard.location
    })

    if (!location) {
      location = topLevelLocations.first()
    }

    var campaign = _(campaigns)
      .filter(function (c) {
        return c.office_id === location.office_id &&
          (dashboard.latest_campaign_id === c.id)
      })
      .sortBy('start_date')
      .last()

    var hasMap = _(dashboard.charts)
      .pluck('type')
      .any(t => _.endsWith(t, 'Map'))

    return {
      campaign: campaign,
      dashboard: dashboard,
      charts: query,
      location: location,
      hasMap: hasMap
    }
  },

  countriesPromise: function (list) {
    return api.geo({ parent_location_id__in: list.join(',') }, null, { 'cache-control': 'max-age=604800, public' }).then(response => {
      var locations = _(response.objects.features).flatten().groupBy('parent_location_id').value()
      return list.map(item => locations[item])
    })
  },

  onFetchDashboards: function () {
    Promise.all([
      Location.getLocations(),
      CampaignStore.getCampaignsPromise(),
      Indicator.getIndicators(),
      Office.getHomePageCharts()
    ])
    .then(_.spread((locations, campaigns, indicators, dashboardDefs) => {
      this.indicators = indicators
      var enhanced = dashboardDefs

      console.log('1: onFetchDashboards')

      var partialDashboardInit = _.partial((data) => {
        var dashboardDef = _.find(enhanced, (item) => {
          return data
        })

        return _.extend({
          campaign: dashboardDef.campaign,
          location: dashboardDef.location,
          indicators: indicators,
          mapLoading: data.mapLoading
        },
        _.pick(dashboardDef.dashboard, ['location', 'date']), {
          data: DashboardInit.dashboardInit(
            dashboardDef.dashboard,
            data.data,
            dashboardDef.location,
            dashboardDef.campaign,
            locations,
            campaigns,
            indicators,
            data.features
          )
        })
      })
      console.log('2: right before fetch data.. should happen ')

      var queries = enhanced.map(this.fetchData)

      Promise.all(queries).then(_.spread((d1, d2, d3) => {
        let dataPoints = [d1, d2, d3].map((item) => {
          return {
            data: _(item)
            .pluck('objects')
            .flatten()
            .sortBy(_.method('campaign.start_date.getTime'))
            .map(this.melt)
            .flatten()
            .value()
          }
        })

        let dashboards = dataPoints.map(function (item) {
          item.mapLoading = true
          return partialDashboardInit(item)
        })

        this.trigger({
          dashboards: dashboards
        })

        this.countriesPromise(dashboardDefs.map(item => item.location.id)).then(countries => {
          dashboards = dataPoints.map((item, index) => {
            item.features = countries[index]
            item.mapLoading = false
            return partialDashboardInit(item)
          })
          this.trigger({
            dashboards: dashboards
          })
        })
      }))
    }))
  },

  getQueriesByIndicators: function (indicators) {
    var qs = _.groupBy(indicators, function (def) {
      return [def.duration, def.startOf, def.locations].join('-')
    })

    return _.map(qs, function (arr) {
      return _.merge.apply(null, arr.concat(function (a, b) {
        if (_.isArray(a)) {
          return a.concat(b)
        }
      }))
    })
  },

  generateIndicator: function (indicators, chart) {
    var base = _.omit(chart, 'indicators', 'title')

    _.each(chart.indicators, function (id) {
      var duration = !_.isNull(_.get(chart, 'timeRange', null)) ? moment.duration(chart.timeRange) : Infinity
      var hash = [id, chart.startOf, chart.locations].join('-')

      if (!indicators.hasOwnProperty(hash) || duration > indicators[hash].duration) {
        indicators[hash] = _.defaults({
          duration: duration,
          indicators: [id]
        }, base)
      }
    })

    return indicators
  }
})

export default HomepageDashboardsStore
