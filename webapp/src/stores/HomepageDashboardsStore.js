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
    // console.log('3: fetching data for location :', dashboard.location.name)
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

      // console.log('1: onFetchDashboards')

      var partialDashboardInit = _.partial((data) => {
        console.log('5.4.1: what is DATA here......', data)
        var locationOfPassedData = data.data[0].location
        console.log('locationOfPassedData', locationOfPassedData)

        // var dashboardDef =
        var dashboardDef = _.find(enhanced, dash => dash.location.id === locationOfPassedData)
        // var dashboardDef = _.find(enhanced, (item) => {
        //   console.log('5.5: what is item.location in partialDashboardInit', item.location)
        //   return data
        // })

        console.log('dashboardDef', dashboardDef)

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
      // console.log('2: right before fetch data.. should happen ')
      var queries = enhanced.map(this.fetchData)

      Promise.all(queries).then(_.spread((d1, d2, d3) => {
        // console.log('4: fetching datapoints data')
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

        // console.log('this here.. is dataPoints.. i need to add the location id here', dataPoints)

        let dashboards = dataPoints.map(function (item) {
          console.log('5: passing this "item" to partial dashboard inint', item)
          item.mapLoading = true
          var some_obj = partialDashboardInit(item)
          // console.log('5.6: this is some obj ( after partial dash init )', some_obj)
          return some_obj
        })

        // console.log('6: trigger the dashboards with these dashboards: ', dashboards)
        this.trigger({
          dashboards: dashboards
        })

        console.log('7: query the geo api: ')
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
