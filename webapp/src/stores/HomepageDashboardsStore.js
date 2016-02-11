import _ from 'lodash'
import Reflux from 'reflux'
import moment from 'moment'

import api from 'data/api'
import DashboardInit from 'data/dashboardInit'

import Indicator from 'data/requests/Indicator'
import Location from 'data/requests/Location'
import Office from 'data/requests/Office'

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

      // console.log('1: enhanced', enhanced)

      var partialDashboardInit = _.partial((data) => {
        // console.log('3: ', data)
        var passedLocation = data.data[0].location
        // FIXME hackAlert.. this method is called twice, once the ID is passed,
        // and in the other the location Object is passed.. need to dig in more.
        if (typeof passedLocation === 'object') {
          var locationIdOfPassedData = passedLocation.id
        } else {
          locationIdOfPassedData = passedLocation
        }

        var dashboardDef = _.find(enhanced, dash => dash.location.id === locationIdOfPassedData)
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
          // console.log('2: item', item)
          var some_obj = partialDashboardInit(item)
          return some_obj
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
  }
})

export default HomepageDashboardsStore
